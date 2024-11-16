

from loongpaser import LoongLexer , LoongParser
# 虚拟机
class VirtualMachine:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name, default=None):
        return self.variables.get(name, default)

    def eval(self, node):
        if node is None:
            return None

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
        elif node[0] == 'func_def':
            return node
        elif node[0] == 'func_call':
            # Call the function with the argument
            func_name = self.eval(node[1])
            arg_value = self.eval(node[2])
            # Create a temporary environment for the function call
            self.set(func_name[1], arg_value)
            return self.eval(func_name[2])

if __name__ == '__main__':
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            ast = parser.parse(lexer.tokenize(text))
            print(ast)
            result = vm.eval(ast)
            print(result)
