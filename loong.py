# -----------------------------------------------------------------------------
# loong.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, ASSIGN }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', '>', '<', '?', ':', ':=' }

    # Tokens
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

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    # Arithmetic operators
    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    # Unary minus
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    # Parentheses
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    # Comparison operators
    @_('expr ">" expr')
    def expr(self, p):
        return p.expr0 > p.expr1

    @_('expr "<" expr')
    def expr(self, p):
        return p.expr0 < p.expr1

    @_('expr "=" expr')
    def expr(self, p):
        return p.expr0 == p.expr1

    # Ternary operator
    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return p.expr1 if p.expr0 else p.expr2

    # Numbers and names
    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
