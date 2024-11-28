from loongpaser import LoongLexer, LoongParser
from loong import VirtualMachine
from colorama import init, Fore, Style
from termcolor import colored

def test_loong():
    init()  # 初始化 colorama
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    test_cases = [
        # 基本功能
        {"input": "a = 10", "expected": None},
        {"input": "a + 5", "expected": 15},
        {"input": "10 > 5 ? 1 : 0", "expected": 1},
        {"input": "10 < 5 ? 1 : 0", "expected": 0},

        # 新增测试
        {"input": "(1 + 2) * (3 + 4)", "expected": 21},  # 嵌套表达式
        {"input": "10 == 5", "expected": False},  # 相等比较

        # 字符串测试
        {"input": 'x = "Hello, world!"', "expected": None},
        {"input": 'y = "Goodbye"', "expected": None},
        {"input": '"Hello, " + "world!"', "expected": "Hello, world!"},

        # 小数测试
        {"input": "a = 3.14", "expected": None},
        {"input": "a + 2.71", "expected": 5.85},
        {"input": "b = 2.0", "expected": None},
        {"input": "b * 3.5", "expected": 7.0},
        {"input": "c = 1.5", "expected": None},
        {"input": "c / 0.5", "expected": 3.0},

        # 函数定义与调用测试
        {"input": "func add(a, b): a + b end", "expected": None},
        {"input": "add(2, 3)", "expected": 5},  # 测试函数调用
        {"input": "func mul(a, b): a * b end", "expected": None},
        {"input": "mul(4, 5)", "expected": 20},  # 测试另一个函数
        {"input": "func square(x): x * x end", "expected": None},
        {"input": "square(6)", "expected": 36},  # 测试单参数函数
        {"input": "func identity(x): x end", "expected": None},
        {"input": "identity(42)", "expected": 42},  # 测试返回参数的函数

        # 数组测试
        {"input": "arr = [1, 2, 3]", "expected": None},  # 数组赋值
        {"input": "arr[0]", "expected": 1},  # 获取第一个元素
        {"input": "arr[1]", "expected": 2},  # 获取第二个元素
        {"input": "arr[2]", "expected": 3},  # 获取第三个元素
        {"input": "arr[0] + arr[1]", "expected": 3},  # 数组元素求和
        {"input": "arr[1] * arr[2]", "expected": 6},  # 数组元素相乘
        {"input": "arr = [10, 20, 30]", "expected": None},  # 重新赋值数组
        {"input": "arr[0] + arr[2]", "expected": 40},  # 新数组的元素求和
        {"input": "b = [1, 2] + [3, 4]", "expected": None},  # 数组拼接
        {"input": "b[3]", "expected": 4},  # 获取拼接后的元素
    ]

    for i, test in enumerate(test_cases):
        try:
            print(colored(test["input"], 'grey'))
            ast = parser.parse(lexer.tokenize(test["input"]))
            result = vm.eval(ast)
            assert result == test["expected"], f"Test case {i+1} {test['input']} failed: expected {test['expected']}, got {result}"
        except Exception as e:
            print(colored(f"Test case {i+1} failed with exception: {e}", 'red'))
            print(colored(f"Input: {test['input']}", 'red'))
            exit(-1)

    print(colored("OK", 'green'))

if __name__ == "__main__":
    test_loong()
