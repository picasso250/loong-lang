from sly import Lexer

# 词法分析器
class LoongLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, ASSIGN, EQUALS, GE, LE, COMMA, LET, FUNC, END, AND, OR, XOR, NOT, LBRACE, RBRACE, INT_DIV }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '%', '(', ')', '>', '<', '?', ':', ';', '.', ',', '[', ']' }

    FUNC = r'func'
    END = r'end'
    LET = r'let'
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
    INT_DIV = '//'
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
