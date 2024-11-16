from sly import Lexer, Parser

# 词法分析器
class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, ASSIGN }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', '>', '<', '?', ':', ':=' }

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ASSIGN = ':='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

# 语法分析器
class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('right', '?', ':'),           # Ternary operator (lowest precedence)
        ('left', '>', '<', '='),     # Comparison operators
        ('left', '+', '-'),           # Addition and subtraction
        ('left', '*', '/'),           # Multiplication and division
        ('right', 'UMINUS'),          # Unary minus
    )

    def __init__(self):
        self.names = {}

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

    # 变量名
    @_('NAME')
    def expr(self, p):
        return ('name', p.NAME)

# 虚拟机
class VirtualMachine:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name, default=None):
        return self.variables.get(name, default)

    def eval(self, node):
        if node[0] == 'num':
            return node[1]
        elif node[0] == 'name':
            return self.get(node[1], 0)
        elif node[0] == 'binop':
            left = self.eval(node[2])
            right = self.eval(node[3])
            if node[1] == '+':
                return left + right
            elif node[1] == '-':
                return left - right
            elif node[1] == '*':
                return left * right
            elif node[1] == '/':
                return left / right
            elif node[1] == '>':
                return left > right
            elif node[1] == '<':
                return left < right
            elif node[1] == '=':
                return left == right
        elif node[0] == 'unaryop':
            return -self.eval(node[2])
        elif node[0] == 'assign':
            self.set(node[1], self.eval(node[2]))
        elif node[0] == 'ternary':
            cond = self.eval(node[1])
            return self.eval(node[2]) if cond else self.eval(node[3])

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    vm = VirtualMachine()

    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            ast = parser.parse(lexer.tokenize(text))
            print(ast)
            print(vm.eval(ast))
