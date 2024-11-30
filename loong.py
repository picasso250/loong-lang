import argparse
from loonglexer import LoongLexer
from loongpaser import LoongParser
from colorama import init
from termcolor import colored
from loongast import *

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

    def has(self, name):
        if name in self.variables:
            return True
        elif self.parent:
            return self.parent.has(name)
        else:
            return False

# Virtual Machine
class VirtualMachine:
    def __init__(self):
        self.global_env = Env()  # Global environment
    def add_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left + right
        elif isinstance(left, str):
            result = left + str(right)
        elif isinstance(left, list):
            if isinstance(right, list):
                result = left + right
            else:
                raise TypeError("Cannot add non-list to a list")
        elif isinstance(left, dict):
            if '__add__' in left:
                result = self.handle_function_call(left['__add__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be added directly unless they implement __add__")
        else:
            raise TypeError("Unsupported operand type(s) for +")
        return result
    def sub_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left - right
        elif isinstance(left, dict):
            if '__sub__' in left:
                result = self.handle_function_call(left['__sub__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be subtracted directly unless they implement __sub__")
        else:
            raise TypeError("Unsupported operand type(s) for -")
        return result

    def mul_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left * right
        elif isinstance(left, str):
            result = left * right
        elif isinstance(left, list):
            result = left * right
        elif isinstance(left, dict):
            if '__mul__' in left:
                result = self.handle_function_call(left['__mul__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be added directly unless they implement __mul__")
        else:
            raise TypeError("Unsupported operand type(s) for *")
        return result

    def div_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left / right
        elif isinstance(left, dict):
            if '__div__' in left:
                result = self.handle_function_call(left['__div__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be divided directly unless they implement __div__")
        else:
            raise TypeError("Unsupported operand type(s) for /")
        return result

    def floordiv_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left // right
        elif isinstance(left, dict):
            if '__floordiv__' in left:
                result = self.handle_function_call(left['__floordiv__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be floor divided directly unless they implement __floordiv__")
        else:
            raise TypeError("Unsupported operand type(s) for //")
        return result

    def pow_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left ** right
        elif isinstance(left, dict):
            if '__pow__' in left:
                result = self.handle_function_call(left['__pow__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be powered directly unless they implement __pow__")
        else:
            raise TypeError("Unsupported operand type(s) for **")
        return result

    def mod_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            result = left % right
        elif isinstance(left, dict):
            if '__mod__' in left:
                result = self.handle_function_call(left['__mod__'], [left, right], env)
            else:
                raise TypeError("Dictionaries cannot be modulo divided directly unless they implement __mod__")
        else:
            raise TypeError("Unsupported operand type(s) for %")
        return result

    def handle_function_call(self, func_def, arg_values, env):
        local_env = Env(parent=func_def.env)
        for i in range(len(func_def.param_list)):
            local_env.set(func_def.param_list[i], arg_values[i])

        result = None
        for stmt in func_def.statements:
            result = self.eval(stmt, local_env)
        print("return", result)
        return result
    def eval(self, node, env=None):
        if env is None:
            env = self.global_env  # Default to global environment

        if node is None:
            return None

        if isinstance(node, Num):
            return node.value
        elif isinstance(node, Str):
            return node.value
        elif isinstance(node, Name):
            return env.lookup(node.name, 0)
        elif isinstance(node, BinOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            
            if node.operator == '+':
                result = self.add_operator(left, right, env)
            elif node.operator == '-':
                result = self.sub_operator(left, right, env)
            elif node.operator == '*':
                result = self.mul_operator(left, right, env)
            elif node.operator == '/':
                result = self.div_operator(left, right, env)
            elif node.operator == '//':
                result = self.floordiv_operator(left, right, env)
            elif node.operator == '%':
                result = self.mod_operator(left, right, env)
            elif node.operator == '>':
                result = left > right
            elif node.operator == '<':
                result = left < right
            elif node.operator == '>=':
                result = left >= right
            elif node.operator == '<=':
                result = left <= right
            elif node.operator == '!=':
                result = left != right
            elif node.operator == '==':
                result = left == right
            return result

        elif isinstance(node, LogicOp):
            left = self.eval(node.left, env)
            if node.operator == 'and':
                return left and self.eval(node.right, env)
            elif node.operator == 'or':
                return left or self.eval(node.right, env)
        elif isinstance(node, UnaryOp):
            if node.operator == 'not':
                return not self.eval(node.operand, env)
            elif node.operator == '-':
                return -self.eval(node.operand, env)
        elif isinstance(node, Let):
            value = self.eval(node.value, env)
            target = node.target
            if env.has(target):
                raise Exception(f"Variable '{target}' is already defined")
            print("let", target, "=", value)
            env.set(target, value)

        elif isinstance(node, Assign):
            value = self.eval(node.value, env)
            target = node.target
            if isinstance(target, Name):
                if not env.has(target.name):
                    raise Exception(f"Variable '{target.name}' is not defined")
                print("set", target.name, "=", value)
                env.set(target.name, value)
            elif isinstance(target, ArrayAccess):
                array = self.eval(target.array, env)
                index = self.eval(target.index, env)
                array[index] = value
            elif isinstance(target, PropAccess):
                obj = self.eval(target.obj, env)
                obj[target.prop] = value

        elif isinstance(node, IfExpr):
            cond = self.eval(node.condition, env)
            return self.eval(node.true_expr, env) if cond else self.eval(node.false_expr, env)
        elif isinstance(node, Statements):
            result = None
            for statement in node.statements:
                result = self.eval(statement, env)
            return result
        elif isinstance(node, FuncDef):
            node.env = env
            env.set(node.name, node)
        elif isinstance(node, FuncCall):
            func_def = self.eval(node.fun, env)
            arg_values = [self.eval(arg, env) for arg in node.args]
            return self.handle_function_call(func_def, arg_values, env)
        elif isinstance(node, ArrayAccess):
            array = self.eval(node.array, env)
            index = self.eval(node.index, env)
            return array[index]
        elif isinstance(node, PropAccess):
            obj = self.eval(node.obj, env)
            return obj[node.property_name]
        elif isinstance(node, Array):
            return [self.eval(item, env) for item in node.elements]
        elif isinstance(node, Dict):
            d = {k: self.eval(v, env) for k, v in node.elements.items()}
            return d

def main():
    # Set up argparse
    parser = argparse.ArgumentParser(description="Run LoongVM with optional debugging.")
    parser.add_argument('filename', nargs='?', help="The filename of the source code to execute.")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode for detailed AST output.")
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Initialize components
    init()
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()
    
    if args.filename:
        # Read the file if a filename is provided
        with open(args.filename, 'r', encoding='utf-8') as file:
            code = file.read()
        toks = lexer.tokenize(code)
        ast = parser.parse(toks)
        if args.debug:
            print(colored(str(ast), 'grey'))
        result = vm.eval(ast)
        print(result)
    else:
        # Interactive mode if no filename is provided
        while True:
            try:
                text = input('loong > ')
            except EOFError:
                break
            if text:
                ast = parser.parse(lexer.tokenize(text))
                if args.debug:
                    print(colored(str(ast), 'grey'))
                result = vm.eval(ast)
                print(result)

if __name__ == '__main__':
    main()
