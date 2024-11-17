from loongpaser import LoongLexer, LoongParser
from loong import VirtualMachine

def test_loong():
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    test_cases = [
        {"input": "((a) => a)(1)", "expected": 1},
        {"input": "((a, b) => a + b)(2, 3)", "expected": 5},
        {"input": "a := 10", "expected": None},
        {"input": "a + 5", "expected": 15},
        {"input": "10 > 5 ? 1 : 0", "expected": 1},
        {"input": "10 < 5 ? 1 : 0", "expected": 0},
        {"input": "((x) => x * x)(4)", "expected": 16},
        {"input": "f := (x) => x + 2", "expected": None},
        {"input": "f(3)", "expected": 5},
        {"input": "((x, y) => x > y ? x : y)(7, 3)", "expected": 7},
        {"input": "((a)=>(b)=>a+b)(3)(4)", "expected": 7},
    ]

    for i, test in enumerate(test_cases):
        try:
            ast = parser.parse(lexer.tokenize(test["input"]))
            result = vm.eval(ast)
            assert result == test["expected"], f"Test case {i+1} failed: expected {test['expected']}, got {result}"
        except Exception as e:
            print(f"Test case {i+1} failed with exception: {e}")
            print(f"Input: {test['input']}")
            exit(-1)

    print("OK")

if __name__ == "__main__":
    test_loong()
