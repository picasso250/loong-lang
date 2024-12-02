import argparse
from colorama import init
from termcolor import colored
from loongast import *

from lark import Lark
from lark.lexer import Token
from lark.tree import Tree

from pretty import pretty_var

# Read the grammar from the external EBNF file
with open('grammar.ebnf', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Create the Lark parser using the external grammar
parser = Lark(grammar, start='start', parser='lalr')

class Env:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def set(self, name, value):
        self.variables[name] = value

    def lookup(self, name):
        if name in self.variables:
            return True, self.variables[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            return False, None

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
        for i in range(len(func_def.params)):
            local_env.set(func_def.params[i].value, arg_values[i])

        result = None
        for stmt in func_def.statements:
            result = self.eval(stmt, local_env)
        # print("return", result)
        return result
    def eval(self, node, env=None):
        if env is None:
            env = self.global_env  # Default to global environment

        if node is None:
            return None

        if isinstance(node, Tree):
            if node.data == 'statements':
                result = None
                for statement in node.children:
                    result = self.eval(statement, env)
                return result
            elif node.data== 'let_stmt':
                value = self.eval(node.children[1], env)
                target = node.children[0].value
                exists, _ = env.lookup(target)
                if exists:
                    raise Exception(f"Variable '{target}' is already defined")
                # print("let", target, "=", value)
                env.set(target, value)
            elif node.data == 'let_multi_stmt':
                expr = node.children[-1]
                names = node.children[:-1]
                value = self.eval(expr, env)
                if not isinstance(value, list):
                    raise TypeError(f"Expected list, got {type(value).__name__}")
                if len(names) != len(value):  # 检测数组长度是否匹配
                    raise ValueError(f"Number of names ({len(names)}) does not match number of values ({len(value)})")
                for index, name in enumerate(names):
                    exists, _ = env.lookup(name.value)
                    if exists:
                        raise Exception(f"Variable '{name.value}' is already defined")
                    env.set(name.value, value[index])

            elif node.data== 'assign_stmt':
                value = self.eval(node.children[1], env)
                target = node.children[0]
                if isinstance(target, Token): # name
                    exists,_ = env.lookup(target.value)
                    if not exists:
                        raise Exception(f"Variable '{target.value}' is not defined")
                    print("set", target.value, "=", value)
                    env.set(target.value, value)
                elif isinstance(target, Tree):
                    if target.data== 'array_access':
                        array = self.eval(target.children[0], env)
                        index = self.eval(target.children[1], env)
                        array[index] = value
                    elif target.data== 'prop_access':
                        obj = self.eval(target.children[0], env)
                        obj[target.children[1].value] = value

            elif node.data== 'func_def':
                env.set(node.children[0].value, FuncDef(node.children[1].children, node.children[2].children, env))
            elif node.data== 'func_expr':
                return FuncDef(node.children[0].children, node.children[1].children, env)
            elif node.data== 'short_func_expr':
                return FuncDef([node.children[0]], [node.children[1]], env)
            elif node.data== 'func_call':
                func_def = self.eval(node.children[0], env)
                arg_names = node.children[1].children
                arg_values = [self.eval(arg, env) for arg in arg_names]
                return self.handle_function_call(func_def, arg_values, env)
            elif node.data== 'array_access':
                array = self.eval(node.children[0], env)
                index = self.eval(node.children[1], env)
                return array[index]
            elif node.data== 'prop_access':
                obj = self.eval(node.children[0], env)
                return obj[node.children[1].value]
            elif node.data== 'list':
                return [self.eval(item, env) for item in node.children]
            elif node.data== 'dict':
                d = {pair.children[0].value: self.eval(pair.children[1], env) for pair in node.children}
                return d
            
            elif node.data== 'map_expr':
                operator = node.children[1].type
                if operator == 'MAP_AT':
                    lst = self.eval(node.children[0], env)
                    lmd = self.eval(node.children[2], env)
                    return [self.handle_function_call(lmd, [x], env) for x in lst]
                elif operator == 'FILTER_IF':
                    lst = self.eval(node.children[0], env)
                    lmd = self.eval(node.children[2], env)
                    return [x for x in lst if self.handle_function_call(lmd, [x], env)]
        
            elif node.data== 'conditional_exp':
                cond = self.eval(node.children[0], env)
                return self.eval(node.children[1], env) if cond else self.eval(node.children[2], env)
            
            elif node.data == 'additive_exp':  # 加法表达式
                left = self.eval(node.children[0], env)  # 左操作数
                operator = node.children[1].value  # 操作符在第二个子节点
                right = self.eval(node.children[2], env)  # 右操作数
                if operator == '+':
                    result = self.add_operator(left, right, env)
                elif operator == '-':
                    result = self.sub_operator(left, right, env)
                return result
            elif node.data == 'mult_exp':  # 乘法表达式
                left = self.eval(node.children[0], env)
                operator = node.children[1].value  # 操作符在第二个子节点
                right = self.eval(node.children[2], env)
                if operator == '*':
                    result = self.mul_operator(left, right, env)
                elif operator == '/':
                    result = self.div_operator(left, right, env)
                elif operator == '//':
                    result = self.floordiv_operator(left, right, env)
                elif operator == '%':
                    result = self.mod_operator(left, right, env)
                return result
            elif node.data == 'bitwise_exp':  # 位运算表达式
                left = self.eval(node.children[0], env)
                operator = node.children[1].value  # 操作符在第二个子节点
                right = self.eval(node.children[2], env)
                if operator == '&':
                    result = left & right
                elif operator == '|':
                    result = left | right
                elif operator == '^':
                    result = left ^ right
                return result
            elif node.data == 'equality_exp':  # 等式表达式
                left = self.eval(node.children[0], env)
                operator = node.children[1].value  # 操作符在第二个子节点
                right = self.eval(node.children[2], env)
                if operator == '==':
                    result = left == right
                elif operator == '!=':
                    result = left != right
                return result
            elif node.data == 'relational_exp':  # 关系表达式
                left = self.eval(node.children[0], env)
                operator = node.children[1].value  # 操作符在第二个子节点
                right = self.eval(node.children[2], env)
                if operator == '<':
                    result = left < right
                elif operator == '>':
                    result = left > right
                elif operator == '<=':
                    result = left <= right
                elif operator == '>=':
                    result = left >= right
                return result
            elif node.data == 'shift_expression':  # 移位表达式
                left = self.eval(node.children[0], env)
                operator = node.children[1].value  # 操作符在第二个子节点
                right = self.eval(node.children[2], env)
                if operator == '<<':
                    result = left << right
                elif operator == '>>':
                    result = left >> right
                return result
            elif node.data == 'logical_or_exp':  # 逻辑或表达式
                left = self.eval(node.children[0], env)
                if left:
                    return left
                return self.eval(node.children[2], env)
            elif node.data == 'logical_and_exp':  # 逻辑与表达式
                left = self.eval(node.children[0], env)
                if not left:
                    return left
                return self.eval(node.children[2], env)
            elif node.data == 'unary_exp':  # 一元运算符表达式
                operator = node.children[0].value  # 操作符在第一个子节点
                operand = self.eval(node.children[1], env)  # 操作数在第二个子节点
                if operator == 'not':
                    return not operand
                elif operator == '-':
                    return -operand
                elif operator == '+':
                    return +operand
                elif operator == '~':
                    return ~operand
                return operand
            elif node.data == 'postfix_exp':  # 后缀表达式
                return self.eval(node.children[0], env)
            elif node.data == 'primary_exp':  # 基础表达式
                return self.eval(node.children[0], env)
            elif node.data == 'func_call':  # 函数调用
                func = self.eval(node.children[0], env)  # 函数名
                args = [self.eval(arg, env) for arg in node.children[1].children]  # 函数参数
                return func(*args)
            elif node.data == 'array_access':  # 数组访问
                array = self.eval(node.children[0], env)
                index = self.eval(node.children[1], env)
                return array[index]
            elif node.data == 'prop_access':  # 属性访问
                obj = self.eval(node.children[0], env)
                property_name = node.children[1].value  # 属性名在第二个子节点
                return obj[property_name]
            elif node.data == 'dict':  # 字典
                return {self.eval(k, env): self.eval(v, env) for k, v in zip(node.children[0::2], node.children[1::2])}
            elif node.data == 'list':  # 列表
                return [self.eval(item, env) for item in node.children]
            elif node.data == 'let_stmt':  # 变量声明
                target = node.children[0].value  # 目标变量
                value = self.eval(node.children[1], env)  # 赋值表达式
                env.set(target, value)
                return value
            elif node.data == 'assign_stmt':  # 变量赋值
                target = self.eval(node.children[0], env)
                value = self.eval(node.children[2], env)
                if isinstance(target, list):
                    target[node.children[1].value] = value  # 数组访问赋值
                else:
                    env.set(target, value)  # 普通赋值
                return value
            elif node.data == 'func_stmt':  # 函数定义
                func_name = node.children[0].value
                params = [param.value for param in node.children[1].children]
                body = node.children[2]
                env.set(func_name, (params, body))
                return None
        elif isinstance(node, Token):
            if node.type == 'NUMBER':
                if '.' in node.value or 'e' in node.value or 'E' in node.value:
                    return float(node.value)
                else:
                    return int(node.value)
            elif node.type == 'STRING':
                return node.value[1:-1]
            elif node.type == 'NAME':
                exists,value = env.lookup(node.value)
                if not exists:
                    raise NameError(f"Variable '{node.value}' not defined in the environment.")
                return value


def main():
    # Set up argparse
    argparser = argparse.ArgumentParser(description="Run LoongVM with optional debugging.")
    argparser.add_argument('filename', nargs='?', help="The filename of the source code to execute.")
    argparser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode for detailed AST output.")
    
    # Parse command-line arguments
    args = argparser.parse_args()
    
    # Initialize components
    init()
    vm = VirtualMachine()
    
    if args.filename:
        # Read the file if a filename is provided
        with open(args.filename, 'r', encoding='utf-8') as file:
            code = file.read()
        ast = parser.parse(code)
        if args.debug:
            print(colored(ast.pretty(), 'grey'))
        result = vm.eval(ast)
        print(pretty_var(result))
    else:
        # Interactive mode if no filename is provided
        while True:
            try:
                text = input('loong > ')
                # text = ' [1,2,3] @[ x=>x+1 ] >? ( x=>x%2==0 ) @[ x=>x*2 ]  '
                # text = ' [1,2,3] @ (x=>x+1) >? (x=>x%2==0)  @ x=>x*2 '
                # text = ' [["a",1]] @ {k,v=>k,v} '
                # text = 'a=>b=>a+b'
                # text = 'a@f@g'
                # text = 'let [a,b]=[2,3];a+b'
                # text = 'let 中=1;中'
            except EOFError:
                break
            if text:
                ast = parser.parse(text)
                if args.debug:
                    print(colored(ast.pretty(), 'grey'))
                result = vm.eval(ast)
                print(pretty_var(result))
                # break

if __name__ == '__main__':
    main()
