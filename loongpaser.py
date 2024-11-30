from sly import Lexer, Parser
from longlexer import LoongLexer
from longast import *

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
        ('left', '*', '/', '%'),            # Multiplication and division
        ('right', 'UMINUS', 'UADD'),           # Unary minus
    )

    # 语句组
    @_('statement ";" statements')
    def statements(self, p):
        node = Statements([p.statement] + p.statements.statements)
        node.index = p.index
        node.end = p.end
        return node
    
    @_('statement_with_end statements')
    def statements(self, p):
        node = Statements([p.statement_with_end] + p.statements.statements)
        node.index = p.index
        node.end = p.end
        return node
    
    @_('statement')
    def statements(self, p):
        node = Statements([p.statement])
        node.index = p.index
        node.end = p.end
        return node
    
    @_('statement_with_end')
    def statements(self, p):
        node = Statements([p.statement_with_end])
        node.index = p.index
        node.end = p.end
        return node
    
    # 语句
    @_('unary_exp ASSIGN expr')
    def statement(self, p):
        node = Assign(p.unary_exp, p.expr)
        node.index = p.index
        node.end = p.end
        return node

    # 函数定义语句
    @_('FUNC NAME "(" param_list ")" ":" statements END')
    def statement_with_end(self, p):
        node = FuncDef(p.NAME, p.param_list, p.statements.statements)
        node.index = p.index
        node.end = p.end
        return node

    # 变量赋值
    @_('expr')
    def statement(self, p):
        node = p.expr
        node.index = p.index
        node.end = p.end
        return node
    
    # 数组语法
    @_('"[" "]"')
    def expr(self, p):
        node = Array([])
        node.index = p.index
        node.end = p.end
        return node
    
    @_('"[" arg_list "]"')
    def expr(self, p):
        node = Array(p.arg_list)
        node.index = p.index
        node.end = p.end
        return node
    
    # 字典创建
    @_('LBRACE dict_entries RBRACE')
    def expr(self, p):
        node = Dict(dict(p.dict_entries))
        node.index = p.index
        node.end = p.end
        return node
    
    @_('LBRACE  RBRACE')
    def expr(self, p):
        node = Dict({})
        node.index = p.index
        node.end = p.end
        return node
    
    @_('dict_entry')
    def dict_entries(self, p):
        node = [p.dict_entry]
        return node
    
    @_('dict_entries COMMA dict_entry')
    def dict_entries(self, p):
        node = p.dict_entries + [p.dict_entry]
        return node
    
    @_('NAME ":" expr')
    def dict_entry(self, p):
        node = (p.NAME, p.expr)
        return node

    # 运算符
    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr "%" expr',
       'expr ">" expr',
       'expr "<" expr',
       'expr EQUALS expr',
       'expr GE expr',
       'expr LE expr')
    def expr(self, p):
        node = BinOp(p[1], p.expr0, p.expr1)
        node.index = p.index
        node.end = p.end
        return node

    @_('expr AND expr',
       'expr OR expr',
       'expr XOR expr')
    def expr(self, p):
        node = LogicOp(p[1], p.expr0, p.expr1)
        node.index = p.index
        node.end = p.end
        return node

    # 三元运算符
    @_('expr "?" expr ":" expr')
    def expr(self, p):
        node = IfExpr(p.expr0, p.expr1, p.expr2)
        node.index = p.index
        node.end = p.end
        return node

    # 参数列表
    @_('NAME')
    def param_list(self, p):
        node = [p.NAME]
        node.index = p.index
        node.end = p.end
        return node

    @_('param_list COMMA NAME')
    def param_list(self, p):
        node = p.param_list + [p.NAME]
        node.index = p.index
        node.end = p.end
        return node

    @_('unary_exp')
    def expr(self, p):
        node = p.unary_exp
        node.index = p.index
        node.end = p.end
        return node

    @_('postfix_exp')
    def unary_exp(self, p):
        node = p.postfix_exp
        node.index = p.index
        node.end = p.end
        return node

    @_('NOT expr')
    def unary_exp(self, p):
        node = UnaryOp('not', p.unary_exp)
        node.index = p.index
        node.end = p.end
        return node

    @_('"-" unary_exp %prec UMINUS')
    def unary_exp(self, p):
        node = UnaryOp('-', p.unary_exp)
        node.index = p.index
        node.end = p.end
        return node

    @_('"+" unary_exp %prec UADD')
    def unary_exp(self, p):
        node = UnaryOp('+', p.unary_exp)
        node.index = p.index
        node.end = p.end
        return node

    @_('"~" unary_exp')
    def unary_exp(self, p):
        node = UnaryOp('~', p.unary_exp)
        node.index = p.index
        node.end = p.end
        return node

    @_('primary_exp')
    def postfix_exp(self, p):
        node = p.primary_exp
        node.index = p.index
        node.end = p.end
        return node

    # 函数调用
    @_('postfix_exp "(" arg_list ")"')
    def postfix_exp(self, p):
        node = FuncCall(p.postfix_exp, p.arg_list)
        node.index = p.index
        node.end = p.end
        return node

    @_('postfix_exp "(" ")"')
    def postfix_exp(self, p):
        node = FuncCall(p.postfix_exp, [])
        node.index = p.index
        node.end = p.end
        return node

    # 数组访问
    @_('postfix_exp "[" expr "]"')
    def postfix_exp(self, p):
        node = ArrayAccess(p.postfix_exp, p.expr)
        node.index = p.index
        node.end = p.end
        return node

    # 属性访问
    @_('postfix_exp "." NAME')
    def postfix_exp(self, p):
        node = PropAccess(p.postfix_exp, p.NAME)
        node.index = p.index
        node.end = p.end
        return node
    
    @_('"(" expr ")"')
    def primary_exp(self, p):
        node = p.expr
        node.index = p.index
        node.end = p.end
        return node

    # 字符串
    @_('STRING')
    def primary_exp(self, p):
        node = Str(p.STRING)
        node.index = p.index
        node.end = p.end
        return node

    # 变量名
    @_('NAME')
    def primary_exp(self, p):
        node = Name(p.NAME)
        node.index = p.index
        node.end = p.end
        return node

    @_('const')
    def primary_exp(self, p):
        node = p.const
        node.index = p.index
        node.end = p.end
        return node

    # 参数列表
    @_('expr')
    def arg_list(self, p):
        node = [p.expr]
        node.index = p.index
        node.end = p.end
        return node

    @_('arg_list COMMA expr')
    def arg_list(self, p):
        node = p.arg_list + [p.expr]
        node.index = p.index
        node.end = p.end
        return node

    # 数字
    @_('NUMBER')
    def const(self, p):
        node = Num(p.NUMBER)
        node.index = p.index
        node.end = p.end
        return node

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}({p.value}) in line {p.lineno}")
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    lexer = LoongLexer()
    parser = LoongParser()

    text = '''# 测试
        a={a:1,b:2}
    '''
    toks = lexer.tokenize(text)
    ast = parser.parse(toks)
    print(str(ast))
