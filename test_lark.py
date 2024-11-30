from lark import Lark
from larkit import LoongTransformer

# Read the grammar from the external EBNF file
with open('grammar.ebnf', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Create the Lark parser using the external grammar
parser = Lark(grammar, start='start', parser='lalr')

# Test cases for all binary operators
test_cases = [
    "let a = 10; a + 5",        # ADD
    "let a = 10; a - 5",        # SUB
    "let a = 10; a * 5",        # MUL
    "let a = 10; a / 5",        # DIV
    "let a = 10; a % 5",        # MOD
    "let a = 10; a == 5",       # EQ
    "let a = 10; a != 5",       # NE
    "let a = 10; a < 5",        # LT
    "let a = 10; a > 5",        # GT
    "let a = 10; a <= 5",       # LE
    "let a = 10; a >= 5",       # GE
    "let a = 10; a << 5",       # SHL
    "let a = 10; a >> 5",       # SHR
    "let a = 10; a & 5",        # AND
    "let a = 10; a | 5",        # OR
    "let a = 10; a ^ 5",        # XOR
    "let a = 10; a and 5",      # AND (logical)
    "let a = 10; a or 5",       # OR (logical)
]

# Parsing and transforming each test case
for idx, test in enumerate(test_cases, 1):
    try:
        tree = parser.parse(test)
        print(f"Test case {idx}: Parsing successful!")
        ast = LoongTransformer().transform(tree)
        print(ast)
    except Exception as e:
        print(f"Test case {idx}: Error - {e}")
