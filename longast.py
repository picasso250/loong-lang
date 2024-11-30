class Let:
    def __init__(self, target, value):
        """
        表示赋值语句的抽象语法树节点。

        :param target: 赋值的目标（如变量名或属性）。
        :param value: 被赋的值。
        """
        self.target = target
        self.value = value

    def __str__(self):
        return f"Let(target={self.target}, value={self.value})"
class Assign:
    def __init__(self, target, value):
        """
        表示赋值语句的抽象语法树节点。

        :param target: 赋值的目标（如变量名或属性）。
        :param value: 被赋的值。
        """
        self.target = target
        self.value = value

    def __str__(self):
        return f"Assign(target={self.target}, value={self.value})"


class Statements:
    def __init__(self, statements: list):
        """
        表示语句列表的抽象语法树节点。

        :param statements: 语句的列表。
        """
        self.statements = statements

    def __str__(self):
        return f"Statements({self.statements})"


class BinOp:
    def __init__(self, operator: str, left, right):
        """
        表示二元操作的抽象语法树节点。

        :param operator: 操作符（如 '+', '-', '*' 等）。
        :param left: 左操作数。
        :param right: 右操作数。
        """
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"BinOp(operator={self.operator}, left={self.left}, right={self.right})"


class UnaryOp:
    def __init__(self, operator: str, operand):
        """
        表示一元操作的抽象语法树节点。

        :param operator: 操作符（如 '-', '+' 等）。
        :param operand: 操作数。
        """
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"UnaryOp(operator={self.operator}, operand={self.operand})"


class LogicOp:
    def __init__(self, operator: str, left, right):
        """
        表示逻辑操作的抽象语法树节点。

        :param operator: 逻辑操作符（如 'and', 'or', 'xor'）。
        :param left: 左操作数。
        :param right: 右操作数。
        """
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"LogicOp(operator={self.operator}, left={self.left}, right={self.right})"


class IfExpr:
    def __init__(self, condition, true_expr, false_expr):
        """
        表示三元操作符的抽象语法树节点。

        :param condition: 条件表达式。
        :param true_expr: 条件为真时的表达式。
        :param false_expr: 条件为假时的表达式。
        """
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __str__(self):
        return f"IfExpr(condition={self.condition}, true_expr={self.true_expr}, false_expr={self.false_expr})"


class FuncCall:
    def __init__(self, fun, args: list):
        """
        表示函数调用的抽象语法树节点。

        :param fun: 被调用的函数或表达式。
        :param args: 参数列表。
        """
        self.fun = fun
        self.args = args

    def __str__(self):
        return f"FuncCall(fun={self.fun}, args={self.args})"


class FuncDef:
    def __init__(self, name: str, param_list: list, statements: list):
        """
        表示函数定义的抽象语法树节点。
        
        :param name: 函数名。
        :param param_list: 参数列表（每个元素为字符串）。
        :param statements: 函数体语句列表。
        """
        self.name = name
        self.param_list = param_list
        self.statements = statements

    def __str__(self):
        return f"FuncDef(\n\tname={self.name}, \n\tparam_list={self.param_list}, \n\tstatements={self.statements})"


class ArrayAccess:
    def __init__(self, array, index):
        """
        表示数组访问的抽象语法树节点。

        :param array: 数组对象。
        :param index: 索引表达式。
        """
        self.array = array
        self.index = index

    def __str__(self):
        return f"ArrayAccess(array={self.array}, index={self.index})"


class PropAccess:
    def __init__(self, obj, property_name: str):
        """
        表示属性访问的抽象语法树节点。

        :param obj: 对象表达式。
        :param property_name: 属性名。
        """
        self.obj = obj
        self.property_name = property_name

    def __str__(self):
        return f"PropAccess(obj={self.obj}, property_name={self.property_name})"


class Num:
    def __init__(self, value):
        """
        表示数字常量的抽象语法树节点。

        :param value: 数字的值（整数或浮点数）。
        """
        self.value = value

    def __str__(self):
        return f"Num(value={self.value})"


class Name:
    def __init__(self, name: str):
        """
        表示变量名的抽象语法树节点。

        :param name: 变量名字符串。
        """
        self.name = name

    def __str__(self):
        return f"Name(name={self.name})"


class Str:
    def __init__(self, value: str):
        """
        表示字符串常量的抽象语法树节点。

        :param value: 字符串的内容。
        """
        self.value = value

    def __str__(self):
        return f"Str(value={self.value})"


class Dict:
    def __init__(self, elements: dict):
        """
        表示字典（映射）的抽象语法树节点。

        :param elements: 字典的键值对。
        """
        self.elements = elements

    def __str__(self):
        lines = []
        for key, value in self.elements.items():
            if key.startswith("__") and key.endswith("__"):
                value_repr = "..."
            else:
                value_repr = repr(value)
            lines.append(f"  {repr(key)}: {value_repr}")
        return "Dict(\n" + ",\n".join(lines) + "\n)"

class Array:
    def __init__(self, elements: list):
        """
        表示数组（列表）的抽象语法树节点。

        :param elements: 数组的元素。
        """
        self.elements = elements

    def __str__(self):
        return f"Array({self.elements})"
