from lark import Lark, Transformer, v_args

# Read the grammar from the external EBNF file
with open('grammar.ebnf', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Create the Lark parser using the external grammar
parser = Lark(grammar, start='start', parser='lalr')

# Sample input to test the grammar
sample_input = """
LET x = 5;
FUNC foo(x, y): 
  LET z = x + y;
  END
"""

# Parsing the input
try:
    tree = parser.parse(sample_input)
    print("Parsing successful!")
    print(tree.pretty())
except Exception as e:
    print(f"Error: {e}")
