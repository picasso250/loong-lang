from sly import Lexer, Parser

# 定义词法分析器
class CalcLexer(Lexer):
    tokens = { NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN }
    ignore = ' \t'

    # Token正则表达式规则
    NUMBER = r'\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    # 行号跟踪
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


# 定义语法解析器
class CalcParser(Parser):
    tokens = CalcLexer.tokens

    # 定义优先级 (越下面优先级越高)
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('nonassoc', 'UMINUS'),  # 一元负号优先级
    )

    # 定义语法规则
    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            if text.lower() in {'quit', 'exit'}:
                break
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except Exception as e:
            print(f"Error: {e}")
