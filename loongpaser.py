# 解释器 - Loong
# 该程序实现了一个简单的解释器，能够解析和执行基本的数学表达式、变量赋值、三元运算符、字符串、小数、函数定义与调用等功能。
# 使用 sly 库进行词法分析与语法分析，支持以下功能：
# - 基本的算术运算：加法、减法、乘法、除法
# - 比较运算符：大于、小于、等于
# - 变量赋值与引用
# - 支持三元运算符
# - 支持字符串（双引号括起来）
# - 支持小数
# - 支持函数定义和调用
# - 支持单行注释（以井号 # 开头）

from sly import Lexer, Parser

# 词法分析器
class LoongLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, ASSIGN, ARROW, COMMA }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', '>', '<', '?', ':', ':=', '=>', ';', ',' }

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ASSIGN = ':='
    ARROW = '=>'
    COMMA = r','  # 支持逗号

    @_(r'\d+\.\d+|\d+')
    def NUMBER(self, t):
        if '.' in t.value:
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
        ('left', '>', '<', '='),       # Comparison operators
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

    @_('statement')
    def statements(self, p):
        return ('statements', [p.statement])

    # 语句
    @_('NAME ASSIGN expr')
    def statement(self, p):
        return ('assign', p.NAME, p.expr)

    @_('expr')
    def statement(self, p):
        return p.expr

    # 运算符
    @_('expr "+" expr')
    def expr(self, p):
        return ('binop', '+', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('binop', '-', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('binop', '*', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('binop', '/', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('unaryop', '-', p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    # 比较运算符
    @_('expr ">" expr')
    def expr(self, p):
        return ('binop', '>', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ('binop', '<', p.expr0, p.expr1)

    @_('expr "=" expr')
    def expr(self, p):
        return ('binop', '=', p.expr0, p.expr1)

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

    # 函数定义
    @_(' "("  ")" ARROW expr')
    def expr(self, p):
        return ('func_def', [], p.expr)
    @_(' "(" NAME ")" ARROW expr') # 不知道为何需要这个，但确实需要这个
    def expr(self, p):
        return ('func_def', [p.NAME], p.expr)
    @_(' "(" param_list ")" ARROW expr')
    def expr(self, p):
        return ('func_def', p.param_list, p.expr)

    # 参数列表
    @_('NAME')
    def param_list(self, p):
        return [p.NAME]

    @_('param_list COMMA NAME')
    def param_list(self, p):
        return p.param_list + [p.NAME]

    # 函数调用
    @_('expr "("  ")"')
    def expr(self, p):
        return ('func_call', p.expr, [])
    @_('expr "(" arg_list ")"')
    def expr(self, p):
        return ('func_call', p.expr, p.arg_list)

    # 参数列表
    @_('expr')
    def arg_list(self, p):
        return [p.expr]

    @_('arg_list COMMA expr')
    def arg_list(self, p):
        return p.arg_list + [p.expr]

if __name__ == '__main__':
    lexer = LoongLexer()
    parser = LoongParser()

    text = '# This is a comment\n"Hello, " + "world!"'
    ast = parser.parse(lexer.tokenize(text))
    print(ast)
