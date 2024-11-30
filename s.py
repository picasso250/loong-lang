import os
import re

def count_operators_in_file(file_path, operators):
    counts = {op: 0 for op in operators}
    total_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for op in operators:
                count = len(re.findall(re.escape(op), content))
                counts[op] += count
                total_count += count
    except:
        print('error', file_path)

    return counts, total_count

def count_operators_in_directory(directory, operators):
    total_counts = {op: 0 for op in operators}
    total_files = 0

    for root, dirs, files in os.walk(directory):
        # Filter out directories that start with a dot
        # dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                continue
            if file.endswith('.py'):
                total_files += 1
                file_path = os.path.join(root, file)
                counts, _ = count_operators_in_file(file_path, operators)
                for op in total_counts:
                    total_counts[op] += counts[op]

    return total_counts, total_files

def calculate_ratios(total_counts, total_files):
    total_operators = sum(total_counts.values())
    ratios = {op: (count / total_operators * 100 if total_operators > 0 else 0) for op, count in total_counts.items()}
    return ratios

def main(directory, operators):
    total_counts, total_files = count_operators_in_directory(directory, operators)
    ratios = calculate_ratios(total_counts, total_files)

    print(f"在 {total_files} 个文件中统计到的运算符出现次数：")
    for op, count in total_counts.items():
        print(f"{op}: {count} 次，占比: {ratios[op]:.2f}%")

if __name__ == "__main__":
    # code_directory = input("请输入代码库路径：")
    code_directory = '.'
    operators = [
        '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '//=', '**='
    ]
    main(code_directory, operators)
