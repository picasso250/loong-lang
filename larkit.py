from lark import Lark, Transformer, v_args

# Simplified Lark grammar
grammar = """
start: statements

statements: [statement]
statement: "let" NAME "=" expr ";"
         | unary_exp "=" expr ";"
         | "fun" NAME "(" (NAME ("," NAME)*)? ")" ":" statements "END"
         | expr ";"

expr: "[" "]"
    | "[" arg_list "]"
    | "{" dict_entries "}"
    | "{" "}"
    | NAME ":" expr
    | expr "+" expr
    | expr "-" expr
    | expr "*" expr
    | expr "/" expr
    | expr "%" expr
    | expr "==" expr
    | expr "//" expr
    | expr ">" expr
    | expr "<" expr
    | expr "==" expr
    | expr ">=" expr
    | expr "<=" expr
    | expr "and" expr
    | expr "or" expr
    | expr "?" expr ":" expr
    | unary_exp
    | postfix_exp

dict_entries: dict_entry ("," dict_entry)*

dict_entry: NAME ":" expr

unary_exp: "NOT" expr
         | "-" unary_exp
         | "+" unary_exp
         | "~" unary_exp
         | postfix_exp

postfix_exp: primary_exp
           | postfix_exp "(" arg_list ")"
           | postfix_exp "(" ")"
           | postfix_exp "[" expr "]"
           | postfix_exp "." NAME

primary_exp: "(" expr ")"
           | STRING
           | NAME
           | const

arg_list: expr ("," expr)*

const: NUMBER

NAME: /[a-zA-Z_][a-zA-Z_0-9]*/
%import common.ESCAPED_STRING   -> STRING
%import common.SIGNED_NUMBER    -> NUMBER
"""

# Create the Lark parser
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
