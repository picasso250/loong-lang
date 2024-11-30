from sly import Lexer

# 词法分析器
class LoongLexer(Lexer):
    tokens = {
        NAME, NUMBER, STRING, EQUALS, GE, LE, COMMA, LET, FUNC, END, AND, OR, XOR, NOT, INT_DIV,
        ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN, MOD_ASSIGN, AND_ASSIGN, OR_ASSIGN, XOR_ASSIGN, SHR_ASSIGN, SHL_ASSIGN, INT_DIV_ASSIGN, POW_ASSIGN,
        LSHIFT, RSHIFT
    }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '%', '(', ')', '>', '<', '?', ':', ';', '.', ',', '[', ']', '{', '}', '&', '|', '^' }

    FUNC = r'fun'
    END = r'end'
    LET = r'let'
    AND = r'and'
    OR = r'or'
    XOR = r'xor'
    NOT = r'not'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUALS = '=='
    GE = '>='
    LE = '<='
    INT_DIV = '//'
    COMMA = r','

    ADD_ASSIGN = r'\+='
    SUB_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    DIV_ASSIGN = r'/='
    MOD_ASSIGN = r'%='
    AND_ASSIGN = r'&='
    OR_ASSIGN = r'\|='
    XOR_ASSIGN = r'\^='
    SHR_ASSIGN = r'>>='
    SHL_ASSIGN = r'<<='
    INT_DIV_ASSIGN = r'//='
    POW_ASSIGN = r'\*\*='
    LSHIFT = r'<<'
    RSHIFT = r'>>'

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
