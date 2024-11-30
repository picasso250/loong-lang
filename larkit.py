from lark import Lark, Transformer, v_args

from lark import Transformer
from loongast import *

# Read the grammar from the external EBNF file
with open('grammar.ebnf', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Create the Lark parser using the external grammar
parser = Lark(grammar, start='start', parser='lalr')

# Sample input to test the grammar
sample_input = """
let a = 3.1;
a>3?1:2;
{a:2};
foo(bar);
f();
1+1
"""

# Parsing the input
try:
    tree = parser.parse(sample_input)
    print("Parsing successful!")
    print(tree)
    a=tree.children[0].children[1]
    print(a,a.__class__,a.type,a.value)
    # print(tree.pretty())
    # ast = LoongTransformer().transform(tree)
    # print(ast)
except Exception as e:
    print(f"Error: {e}")

