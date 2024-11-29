from loongpaser import LoongLexer, LoongParser
from loong import VirtualMachine
from colorama import init, Fore, Style
from termcolor import colored

def parse_test_cases(file_path):
    """解析纯文本格式的测试用例"""
    test_cases = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(colored(f"Failed to load test cases file: {e}", 'red'))
        exit(-1)

    code = None
    for line in lines:
        # 忽略注释行和空行
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        
        if code is None:
            # 第一行：代码
            code = stripped_line
        else:
            # 第二行：期望结果
            try:
                # 使用 eval 将结果字符串解析为 Python 对象
                expected = eval(stripped_line)
            except Exception as e:
                print(colored(f"Failed to parse expected result: {stripped_line}", 'red'))
                exit(-1)
            
            # 保存测试用例
            test_cases.append({"input": code, "expected": expected})
            code = None  # 重置，准备下一组测试用例

    if code is not None:
        print(colored("Test cases file is malformed: unmatched code/result pair", 'red'))
        exit(-1)

    return test_cases

def test_loong():
    init()  # 初始化 colorama
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    # 从纯文本文件加载测试用例
    test_cases = parse_test_cases("test_cases.txt")

    for i, test in enumerate(test_cases):
        try:
            ast = parser.parse(lexer.tokenize(test["input"]))
            result = vm.eval(ast)
            print(colored(test["input"], 'grey'), "==>", colored(result, 'grey'))
            assert result == test["expected"], f"Test case {i+1} {test['input']} failed: expected {test['expected']}, got {result}"
        except Exception as e:
            print(colored(f"Test case {i+1} failed with exception: {e}", 'red'))
            print(colored(f"Input: {test['input']}", 'red'))
            exit(-1)

    print(colored("OK", 'green'))

if __name__ == "__main__":
    test_loong()