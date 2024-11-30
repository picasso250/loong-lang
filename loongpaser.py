from sly import Parser
from loonglexer import LoongLexer
from loongast import *


# 定义一个函数来处理公共的设置node属性操作
def set_node_attrs(node, p):
    node.index = p.index
    node.end = p.end
    return node


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
        return set_node_attrs(node, p)

    @_('statement_with_end statements')
    def statements(self, p):
        node = Statements([p.statement_with_end] + p.statements.statements)
        return set_node_attrs(node, p)

    @_('statement')
    def statements(self, p):
        node = Statements([p.statement])
        return set_node_attrs(node, p)

    @_('statement_with_end')
    def statements(self, p):
        node = Statements([p.statement_with_end])
        return set_node_attrs(node, p)

    # 语句
    @_('LET NAME "=" expr')
    def statement(self, p):
        node = Let(p.NAME, p.expr)
        return set_node_attrs(node, p)

    @_('unary_exp "=" expr')
    def statement(self, p):
        node = Assign(p.unary_exp, p.expr)
        return set_node_attrs(node, p)

    # 函数定义语句
    @_('FUNC NAME "(" param_list ")" ":" statements END')
    def statement_with_end(self, p):
        node = FuncDef(p.NAME, p.param_list, p.statements.statements)
        return set_node_attrs(node, p)

    # 变量赋值
    @_('expr')
    def statement(self, p):
        node = p.expr
        return set_node_attrs(node, p)

    # 数组语法
    @_('"[" "]"')
    def expr(self, p):
        node = Array([])
        return set_node_attrs(node, p)

    @_('"[" arg_list "]"')
    def expr(self, p):
        node = Array(p.arg_list)
        return set_node_attrs(node, p)

    # 字典创建
    @_('"{" dict_entries "}"')
    def expr(self, p):
        node = Dict(dict(p.dict_entries))
        return set_node_attrs(node, p)

    @_('"{"  "}"')
    def expr(self, p):
        node = Dict({})
        return set_node_attrs(node, p)

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
       'expr "%" expr',
       'expr INT_DIV expr',
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
        return set_node_attrs(node, p)

    # 参数列表
    @_('NAME')
    def param_list(self, p):
        return [p.NAME]

    @_('param_list COMMA NAME')
    def param_list(self, p):
        return p.param_list + [p.NAME]

    @_('unary_exp')
    def expr(self, p):
        node = p.unary_exp
        return set_node_attrs(node, p)

    @_('postfix_exp')
    def unary_exp(self, p):
        node = p.postfix_exp
        return set_node_attrs(node, p)

    @_('NOT expr')
    def unary_exp(self, p):
        node = UnaryOp('not', p.unary_exp)
        return set_node_attrs(node, p)

    @_('"-" unary_exp %prec UMINUS')
    def unary_exp(self, p):
        node = UnaryOp('-', p.unary_exp)
        return set_node_attrs(node, p)

    @_('"+" unary_exp %prec UADD')
    def unary_exp(self, p):
        node = UnaryOp('+', p.unary_exp)
        return set_node_attrs(node, p)

    @_('"~" unary_exp')
    def unary_exp(self, p):
        node = UnaryOp('~', p.unary_exp)
        return set_node_attrs(node, p)

    @_('primary_exp')
    def postfix_exp(self, p):
        node = p.primary_exp
        return set_node_attrs(node, p)

    # 函数调用
    @_('postfix_exp "(" arg_list ")"')
    def postfix_exp(self, p):
        node = FuncCall(p.postfix_exp, p.arg_list)
        return set_node_attrs(node, p)

    @_('postfix_exp "(" ")"')
    def postfix_exp(self, p):
        node = FuncCall(p.postfix_exp, [])
        return set_node_attrs(node, p)

    # 数组访问
    @_('postfix_exp "[" expr "]"')
    def postfix_exp(self, p):
        node = ArrayAccess(p.postfix_exp, p.expr)
        return set_node_attrs(node, p)

    # 属性访问
    @_('postfix_exp "." NAME')
    def postfix_exp(self, p):
        node = PropAccess(p.postfix_exp, p.NAME)
        return set_node_attrs(node, p)

    @_('"(" expr ")"')
    def primary_exp(self, p):
        node = p.expr
        return set_node_attrs(node, p)

    # 字符串
    @_('STRING')
    def primary_exp(self, p):
        node = Str(p.STRING)
        return set_node_attrs(node, p)

    # 变量名
    @_('NAME')
    def primary_exp(self, p):
        node = Name(p.NAME)
        return set_node_attrs(node, p)

    @_('const')
    def primary_exp(self, p):
        node = p.const
        return set_node_attrs(node, p)

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
        node = Num(p.NUMBER)
        return set_node_attrs(node, p)

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
    print(ast)