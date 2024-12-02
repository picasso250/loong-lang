import csv
from loong import VirtualMachine, parser
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
                if len(row)==1 and row[0] == '-':
                    test_cases.append({"input": '-', "expected": "clear machine"})
                    continue
                if len(row) < 2:
                    print(colored(f"Malformed row in test cases file at line {line_number}: {row}", 'red'))
                    continue

                code = row[0].strip()
                expected_str = row[1].strip()

                if code == '-':
                    test_cases.append({"input": '-', "expected": expected_str})
                    continue

                try:
                    expected = eval(expected_str)  # 解析期望结果字符串为Python对象
                except Exception as e:
                    print(colored(f"Failed to parse expected result at line {line_number}: {expected_str}, error: {e}", 'red'))
                    continue

                # 保存测试用例
                test_cases.append({"input": code, "expected": expected})

    except Exception as e:
        print(colored(f"Failed to load test cases file: {e}", 'red'))
        exit(-1)

    return test_cases

def test_loong():
    init()  # 初始化 colorama
    vm = VirtualMachine()

    # 从CSV文件加载测试用例
    test_cases = parse_test_cases("test_cases.csv")

    for i, test in enumerate(test_cases):
        try:
            if test["input"] == '-':
                vm = VirtualMachine()
                print(colored(f"### {test['expected']} ###", 'cyan'))
                continue

            ast = parser.parse(test["input"])
            result = vm.eval(ast)
            print(colored(test["input"], 'grey'), "==>", colored(result, 'grey'))
            assert result == test["expected"], f"{test['input']} failed: expected {test['expected']}, got {result}"

        except Exception as e:
            print(colored(f"Test case {i+1} failed: {e}", 'red'))
            print(colored(f"Input: {test['input']}", 'red'))
            exit(-1)

    print(colored("All test cases passed!", 'green'))

if __name__ == "__main__":
    test_loong()