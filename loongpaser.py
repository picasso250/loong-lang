from sly import Lexer, Parser

# 词法分析器
class LoongLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, ASSIGN, EQUALS, GE, LE, COMMA, FUNC, END, AND, OR, XOR, NOT }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', '>', '<', '?', ':', ';', ',', '[', ']' }

    FUNC = r'func'
    END = r'end'
    AND = r'and'
    OR = r'or'
    XOR = r'xor'
    NOT = r'not'

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
        ('right', 'UMINUS'),           # Unary minus
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
    @_('NAME ASSIGN expr')
    def statement(self, p):
        return ('assign', p.NAME, p.expr)

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

    @_('NOT expr')
    def expr(self, p):
        return ('unaryop', 'not', p.expr)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('unaryop', '-', p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    # 三元运算符
    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('ternary', p.expr0, p.expr1, p.expr2)

    # 数字
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    # 字符串
    @_('STRING')
    def expr(self, p):
        return ('str', p.STRING)

    # 变量名
    @_('NAME')
    def expr(self, p):
        return ('name', p.NAME)

    # 函数调用
    @_('NAME "(" arg_list ")"')
    def expr(self, p):
        return ('func_call', ('name', p.NAME), p.arg_list)

    @_('"(" expr ")" "(" arg_list ")"')
    def expr(self, p):
        return ('func_call', p.expr, p.arg_list)

    # 参数列表
    @_('NAME')
    def param_list(self, p):
        return [p.NAME]

    @_('param_list COMMA NAME')
    def param_list(self, p):
        return p.param_list + [p.NAME]

    # 参数列表
    @_('expr')
    def arg_list(self, p):
        return [p.expr]

    @_('arg_list COMMA expr')
    def arg_list(self, p):
        return p.arg_list + [p.expr]

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}({p.value}) in line {p.lineno}")
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    lexer = LoongLexer()
    parser = LoongParser()

    text = '''# 测试逻辑运算符
        a = 1 and 0 or 1 xor 0;
        b = not (1 and 0)
    '''
    toks = lexer.tokenize(text)
    ast = parser.parse(toks)
    from pretty_dump_json import pretty_dump_json
    print(pretty_dump_json(ast, indent=2, max_length=44))
