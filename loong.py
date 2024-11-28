import sys
from loongpaser import LoongLexer, LoongParser
from pretty_dump_json import pretty_dump_json
from colorama import init, Fore, Style
from termcolor import colored

# 环境类
class Env:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def set(self, name, value):
        self.variables[name] = value

    def lookup(self, name, default=None):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.lookup(name, default)
        else:
            return default

# 虚拟机
class VirtualMachine:
    def __init__(self):
        self.global_env = Env()  # 全局环境

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env  # 默认使用全局环境

        if node is None:
            return None

        if node[0] == 'num' or node[0] == 'str':
            return node[1]
        elif node[0] == 'name':
            return env.lookup(node[1], 0)
        elif node[0] == 'binop':
            left = self.eval(node[2], env)
            right = self.eval(node[3], env)
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
            elif node[1] == '==':
                return left == right
            elif node[1] == '>=':
                return left >= right
            elif node[1] == '<=':
                return left <= right
        elif node[0] == 'unaryop':
            return -self.eval(node[2], env)
        elif node[0] == 'assign':
            env.set(node[1], self.eval(node[2], env))
        elif node[0] == 'ternary':
            cond = self.eval(node[1], env)
            return self.eval(node[2], env) if cond else self.eval(node[3], env)
        elif node[0] == 'func_def':
            _, name, params, body = node  # Function name, parameters, body
            env.set(name, ('func', params, body, env))
        elif node[0] == 'func_call':
            # Function call processing:
            func_def = self.eval(node[1], env)  # This retrieves the function definition
            arg_values = [self.eval(arg, env) for arg in node[2]]  # Evaluate arguments

            if func_def:
                _, params, body, func_env = func_def  # Function name, parameters, body
                # Create a new environment for the function call, using the closure environment
                local_env = Env(parent=func_env)  # Parent environment is the function's environment
                for i in range(len(params)):
                    local_env.set(params[i], arg_values[i])  # Bind arguments to parameters
                
                # Evaluate the function body in this new local environment
                result = self.eval(body, local_env)
                return result
        elif node[0] == 'statements':
            result = None
            for statement in node[1]:
                result = self.eval(statement, env)
            return result

if __name__ == '__main__':
    init()  # 初始化 colorama
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    debug_mode = '-d' in sys.argv

    if len(sys.argv) > 1:
        # 从文件中读取代码
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        toks = lexer.tokenize(code)
        ast = parser.parse(toks)
        if debug_mode:
            # 将 ast 转换为 JSON 并打印
            print(colored(pretty_dump_json(ast, indent=2, max_length=44), 'grey'))
        result = vm.eval(ast)
        print(result)
    else:
        # 从标准输入读取代码
        while True:
            try:
                text = input('loong > ')
            except EOFError:
                break
            if text:
                ast = parser.parse(lexer.tokenize(text))
                if debug_mode:
                    # 将 ast 转换为 JSON 并打印
                    print(colored(pretty_dump_json(ast, indent=2, max_length=44), 'grey'))
                result = vm.eval(ast)
                print(result)
