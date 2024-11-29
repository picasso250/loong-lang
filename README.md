# Loong Interpreter

This program implements a simple interpreter capable of parsing and executing basic mathematical expressions, variable assignments, if_expr operators, function definitions, and calls.

## Features

The interpreter supports the following features using the `sly` library for lexical and syntax analysis:

- Basic arithmetic operations: addition, subtraction, multiplication, division.
- Comparison operators: greater than, less than, equal to.
- Variable assignment and reference.
- Support for if_expr operators.
- Support for function definitions and calls.

## Syntax Examples

1. **Variable Assignment**: `a := 10`
2. **Arithmetic Expressions**: `a + b * 2`
3. **Conditional Operator**: `a > 10 ? "Yes" : "No"`
4. **Function Definition and Call**:
    - Function definition: `(a,b) => a+b`
    - Function call: `f(a,b)`
