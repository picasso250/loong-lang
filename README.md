# Loong Language

This program implements a simple interpreter capable of parsing and executing basic mathematical expressions, variable assignments, ternary operators, function definitions, and calls.

[中文版 读我](README.zh.md)

## Philosophy

We aim to provide a more intuitive (and thus more powerful) programming language for both humans and generative AI (e.g., ChatGPT). Our design principles are:

1. **Familiar Syntax**:
   - The syntax is similar to Python and JavaScript, and it can leverage all Python libraries. This allows users to get started quickly, utilize a wealth of existing resources, and benefit from community support for rapid development.
   - Syntax tree parsing does not rely on indentation, making it easy to copy code from ChatGPT.

2. **Lexical Closures** (A "fix" for Python):
   - Lexical closures are adopted to make code easier to understand for both humans and machines. This feature enhances code flexibility, maintainability, and execution efficiency.

3. **Intuitive Syntax Order**:
   - Our syntax structure is closer to actual execution order rather than traditional English grammar. This design helps developers better understand program execution flow, reducing abstraction layers, improving readability and maintainability, and aligning better with AI attention mechanisms.

These principles make Loong both powerful and easy to use, providing an enhanced development experience for generative AI applications.

## Features

This interpreter uses the `lark` library for lexical and syntax analysis, supporting the following features:

- **Basic Features**: Arithmetic operations, comparison operators, logical operators, bitwise operators.
- **Variable Assignment**: Support for variable definition and reference.
- **Ternary Operators**: Supports conditional operations in the form `condition ? expr1 : expr2`.
- **Data Types**: Strings (enclosed in double quotes), floats, integers, arrays, dictionaries, and their access.
- **Functions**: Supports function definition and calls, including anonymous functions (closures).
- **Statement Blocks**: Multiple statements separated by semicolons.
- **Mapping and Filtering**: Supports `@` and `>?` operators for collection mapping and filtering operations.

## Syntax Examples

```
# Variable Assignment
let a = 10;
let b = 3.14;

# Strings
let c = "Hello, " + "world!";

# Conditional Operator
let result = (a + b > 12 ? "Yes" : "No") + ", " + c;

# Arrays and Dictionaries
let arr = [1, 2, 3];
let dict = { key1: 10, key2: 20 };
let val = dict["key1"];

# Function Definition
fun sum(x, y):
    x + y
end

# Function Call
let result = sum(a, b);

# Short Function Expression
let double = a => a * 2;
let doubled = double(5);

# Complete Example
(a + b > 12 ? "Yes" : "No") + ", " + c
```

## Installation and Usage

1. Install dependencies:
    ```bash
    pip install lark colorama termcolor
    ```

2. Run the interpreter:
    ```bash
    python loong.py
    ```

## Testing

Run the test cases to ensure the interpreter's correctness:

```bash
python test_loong.py
```

## Contribution

If you are interested in contributing to this project, please submit an issue report or a pull request.

## License

This project is licensed under the GPL license.

