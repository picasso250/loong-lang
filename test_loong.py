from loongpaser import LoongLexer, LoongParser
from loong import VirtualMachine

def test_loong():
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    test_cases = [
        # 基本功能
        {"input": "((a) => a)(1)", "expected": 1},
        {"input": "((a, b) => a + b)(2, 3)", "expected": 5},
        {"input": "a = 10", "expected": None},
        {"input": "a + 5", "expected": 15},
        {"input": "10 > 5 ? 1 : 0", "expected": 1},
        {"input": "10 < 5 ? 1 : 0", "expected": 0},
        {"input": "((a)=>(b)=>a+b)(3)(4)", "expected": 7},

        # 新增测试
        {"input": "(()=> 42)()", "expected": 42},  # 无参数函数
        {"input": "((a, b, c) => a + b + c)(1, 2, 3)", "expected": 6},  # 多参数
        {"input": "((a) => (b) => a + b)(1)(2)", "expected": 3},  # 嵌套函数调用
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
        {"input": "c / 0.5", "expected": 3.0}
    ]

    for i, test in enumerate(test_cases):
        try:
            ast = parser.parse(lexer.tokenize(test["input"]))
            result = vm.eval(ast)
            assert result == test["expected"], f"Test case {i+1} {test['input']} failed: expected {test['expected']}, got {result}"
        except Exception as e:
            print(f"Test case {i+1} failed with exception: {e}")
            print(f"Input: {test['input']}")
            exit(-1)

    print("OK")

if __name__ == "__main__":
    test_loong()
