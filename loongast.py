

class FuncCall:
    def __init__(self, fun, args: list):
        """
        表示函数调用的抽象语法树节点。

        :param fun: 被调用的函数或表达式。
        :param args: 参数列表。
        """
        self.fun = fun
        self.args = args

    def __repr__(self):
        return f"FuncCall(fun={self.fun}, args={self.args})"


class FuncDef:
    def __init__(self, params, statements, env):
        """
        表示函数定义的抽象语法树节点。
        
        :param params: 参数列表。
        :param statements: 函数体语句列表。
        """
        self.params = params
        self.statements = statements
        self.env = env

    def __repr__(self):
        return f"FuncDef(\n\tname={self.name}, \n\tparam_list={self.param_list}, \n\tstatements={self.statements}\n)"

