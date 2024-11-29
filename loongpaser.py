from sly import Lexer, Parser

# 词法分析器
class LoongLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, ASSIGN, EQUALS, GE, LE, COMMA, FUNC, END, AND, OR, XOR, NOT, LBRACE, RBRACE }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', '>', '<', '?', ':', ';', '.', ',', '[', ']' }

    FUNC = r'func'
    END = r'end'
    AND = r'and'
    OR = r'or'
    XOR = r'xor'
    NOT = r'not'
    LBRACE = r'{'
    RBRACE = r'}'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUALS = '=='
    ASSIGN = '='
    GE = '>='
    LE = '<='
    COMMA = r','

    @_(r'(\d+\.\d*|\d+)([eE][+-]?\d+)?')
    def NUMBER(self, t):
        if '.' in t.value or 'e' in t.value or 'E' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    @_(r'"[^"\n]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]  # 去掉双引号
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass  # 忽略注释内容

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

# 语法分析器
class LoongParser(Parser):
    tokens = LoongLexer.tokens

    precedence = (
        ('right', '?', ':'),           # Ternary operator (lowest precedence)
        ('left', 'OR'),               # Logical OR
        ('left', 'XOR'),              # Logical XOR
        ('left', 'AND'),              # Logical AND
        ('right', 'NOT'),             # Logical NOT
        ('left', '>', '<', 'EQUALS', 'GE', 'LE'),  # Comparison operators
        ('left', '+', '-'),            # Addition and subtraction
        ('left', '*', '/'),            # Multiplication and division
        ('right', 'UMINUS', 'UADD'),           # Unary minus
    )

    def __init__(self):
        self.names = {}

    # 语句组
    @_('statement ";" statements')
    def statements(self, p):
        return ('statements', [p.statement] + p.statements[1])
    @_('statement_with_end statements')
    def statements(self, p):
        return ('statements', [p.statement_with_end] + p.statements[1])
    @_('statement')
    def statements(self, p):
        return ('statements', [p.statement])
    @_('statement_with_end')
    def statements(self, p):
        return ('statements', [p.statement_with_end])
    
    # 语句
    @_('unary_exp ASSIGN expr')
    def statement(self, p):
        return ('assign', p.unary_exp, p.expr)

    # 函数定义语句
    @_('FUNC NAME "(" param_list ")" ":" expr END')
    def statement_with_end(self, p):
        return ('func_def', p.NAME, p.param_list, p.expr)

    # 变量赋值
    @_('expr')
    def statement(self, p):
        return p.expr
    
    # 数组语法
    @_('"[" "]"')
    def expr(self, p):
        return ('array', [])

    @_('"[" arg_list "]"')
    def expr(self, p):
        return ('array', p.arg_list)
    
    # 字典创建
    @_('LBRACE dict_entries RBRACE')
    def expr(self, p):
        return ('dict', p.dict_entries)
    @_('LBRACE  RBRACE')
    def expr(self, p):
        return ('dict', [])
    @_('dict_entry')
    def dict_entries(self, p):
        return [p.dict_entry]

    @_('dict_entries COMMA dict_entry')
    def dict_entries(self, p):
        return p.dict_entries + [p.dict_entry]

    @_('NAME ":" expr')
    def dict_entry(self, p):
        return (p.NAME, p.expr)

    # 运算符
    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr ">" expr',
       'expr "<" expr',
       'expr EQUALS expr',
       'expr GE expr',
       'expr LE expr')
    def expr(self, p):
        return ('binop', p[1], p.expr0, p.expr1)

    @_('expr AND expr',
       'expr OR expr',
       'expr XOR expr')
    def expr(self, p):
        return ('logicop', p[1], p.expr0, p.expr1)

    # 三元运算符
    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('if_expr', p.expr0, p.expr1, p.expr2)

    # 参数列表
    @_('NAME')
    def param_list(self, p):
        return [p.NAME]

    @_('param_list COMMA NAME')
    def param_list(self, p):
        return p.param_list + [p.NAME]

    @_('unary_exp')
    def expr (self, p):
        return p.unary_exp

    @_('postfix_exp')
    def unary_exp (self, p):
        return p.postfix_exp
    @_('NOT expr')
    def unary_exp (self, p):
        return ('unaryop', 'not', p.unary_exp )
    @_('"-" unary_exp %prec UMINUS')
    def unary_exp (self, p):
        return ('unaryop', '-', p.unary_exp )
    @_('"+" unary_exp %prec UADD')
    def unary_exp (self, p):
        return ('unaryop', '+', p.unary_exp )
    @_('"~" unary_exp')
    def unary_exp (self, p):
        return ('unaryop', '~', p.unary_exp )

    @_('primary_exp ')
    def postfix_exp(self, p):
        return p.primary_exp
    # 函数调用
    @_('postfix_exp "(" arg_list ")"')
    def postfix_exp(self, p):
        return ('func_call', p.postfix_exp, p.arg_list)
    @_('postfix_exp "(" ")"')
    def postfix_exp(self, p):
        return ('func_call', p.postfix_exp, [])
    # 数组访问
    @_('postfix_exp "[" expr "]"')
    def postfix_exp(self, p):
        return ('array_access', p.postfix_exp, p.expr)
    # 属性访问
    @_('postfix_exp "." NAME')
    def postfix_exp(self, p):
        return ('prop_access', p.postfix_exp, p.NAME)
    
    @_('"(" expr ")"')
    def primary_exp(self, p):
        return p.expr
    # 字符串
    @_('STRING')
    def primary_exp(self, p):
        return ('str', p.STRING)
    # 变量名
    @_('NAME')
    def primary_exp(self, p):
        return ('name', p.NAME)
    @_('const')
    def primary_exp(self, p):
        return p.const
    
    # 参数列表
    @_('expr')
    def arg_list(self, p):
        return [p.expr]

    @_('arg_list COMMA expr')
    def arg_list(self, p):
        return p.arg_list + [p.expr]
    # 数字
    @_('NUMBER')
    def const(self, p):
        return ('num', p.NUMBER)

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}({p.value}) in line {p.lineno}")
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    lexer = LoongLexer()
    parser = LoongParser()

    text = '''# 测试逻辑运算符
        obj.name
    '''
    toks = lexer.tokenize(text)
    ast = parser.parse(toks)
    from pretty_dump_json import pretty_dump_json
    print(pretty_dump_json(ast, indent=2, max_length=44))
