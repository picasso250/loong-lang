from lark import Lark, Transformer, v_args

from lark import Transformer
from loongast import *

class LoongTransformer(Transformer):
    
    # Statements
    def statements(self, items):
        return Statements(items)

    # Let statement
    def let_stmt(self, items):
        target, value = items
        return Let(target, value)

    # Assign statement
    def assign_stmt(self, items):
        target, value = items
        return Assign(target, value)

    # Function Definition
    def func_stmt(self, items):
        name, params, body = items
        return FuncDef(name, params, body)
    params = list

    # Expression (conditional, binop, etc.)
    def expr(self, items):
        # Here you need to distinguish between different kinds of expressions
        if isinstance(items[0], str):  # Simple name or constant
            return Name(items[0])
        return items[0]  # Otherwise return the first item, it could be a binop or func call

    # Binary Operation (binops)
    def additive_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def mult_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def shift_expression(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def relational_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def equality_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def and_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def inclusive_or_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def exclusive_or_exp(self, items):
        left, operator, right = items
        return BinOp(operator[0], left, right)

    def logical_and_exp(self, items):
        left, right = items
        return BinOp('and', left, right)

    def logical_or_exp(self, items):
        left, right = items
        return BinOp('or', left, right)
    
    # Unary Operation
    def unaryop(self, items):
        operator, operand = items
        return UnaryOp(operator, operand)

    # Function Call
    def func_call(self, items):
        fun, args = items[0], items[1:]
        return FuncCall(fun, args)

    # Conditional Expressions (ternary operator)
    def conditional_exp(self, items):
        condition, true_expr, false_expr = items
        return IfExpr(condition, true_expr, false_expr)

    # Dict
    def dict(self, items):
        print(items)
        elements = {key: value for key, value in items}
        return Dict(elements)

    # Num (numbers)
    def NUMBER(self, items):
        return Num(items[0])

    # Name (variable name)
    def NAME(self, items):
        return Name(items[0])

    # Array (array initialization)
    def array(self, items):
        return Array(items)

    # String
    def string(self, items):
        return Str(items[0])

    # Default for other expressions or statements
    # def __default__(self, data, children_lists, meta):
    #     return data[0]  # In case of unhandled rules, return the first item


# Read the grammar from the external EBNF file
with open('grammar.ebnf', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Create the Lark parser using the external grammar
parser = Lark(grammar, start='start', parser='lalr')

# Sample input to test the grammar
sample_input = """
let a = ~3;
a>3?1:2;
{a:2}
"""

# Parsing the input
try:
    tree = parser.parse(sample_input)
    print("Parsing successful!")
    print(tree)
    print(tree.pretty())
    # ast = LoongTransformer().transform(tree)
    # print(ast)
except Exception as e:
    print(f"Error: {e}")

