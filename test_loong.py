import csv
from loongpaser import LoongLexer, LoongParser
from loong import VirtualMachine
from colorama import init, Fore, Style
from termcolor import colored

def parse_test_cases(file_path):
    """解析CSV格式的测试用例"""
    test_cases = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t",quotechar="'")
            next(reader)  # 跳过表头
            
            for line_number, row in enumerate(reader, start=2):  # start=2 to account for the header
                if len(row) == 0:
                    continue
                if len(row) < 2:
                    print(colored(f"Malformed row in test cases file at line {line_number}: {row}", 'red'))
                    continue

                code = row[0].strip()
                expected_str = row[1].strip()
                comment = row[2].strip() if len(row) > 2 else ""

                try:
                    expected = eval(expected_str)  # 解析期望结果字符串为Python对象
                except Exception as e:
                    print(colored(f"Failed to parse expected result at line {line_number}: {expected_str}, error: {e}", 'red'))
                    continue

                # 保存测试用例
                test_cases.append({"input": code, "expected": expected, "comment": comment})

    except Exception as e:
        print(colored(f"Failed to load test cases file: {e}", 'red'))
        exit(-1)

    return test_cases

def test_loong():
    init()  # 初始化 colorama
    lexer = LoongLexer()
    parser = LoongParser()
    vm = VirtualMachine()

    # 从CSV文件加载测试用例
    test_cases = parse_test_cases("test_cases.csv")

    for i, test in enumerate(test_cases):
        try:
            ast = parser.parse(lexer.tokenize(test["input"]))
            result = vm.eval(ast)
            print(colored(test["input"], 'grey'), "==>", colored(result, 'grey'))
            assert result == test["expected"], f"Test case {i+1} {test['input']} failed: expected {test['expected']}, got {result}"

            # 如果有注释，打印注释
            if test["comment"]:
                print(colored(f"Comment: {test['comment']}", 'blue'))

        except Exception as e:
            print(colored(f"Test case {i+1} failed with exception: {e}", 'red'))
            print(colored(f"Input: {test['input']}", 'red'))
            exit(-1)

    print(colored("All test cases passed!", 'green'))

if __name__ == "__main__":
    test_loong()