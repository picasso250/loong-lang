
class Operators:
    """处理所有运算符操作的类"""
    
    def __init__(self, vm):
        self.vm = vm  # 保留对虚拟机实例的引用，用于函数调用等操作
    
    def add_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left + right
        elif isinstance(left, str):
            return left + str(right)
        elif isinstance(left, list):
            if isinstance(right, list):
                return left + right
            raise TypeError("Cannot add non-list to a list")
        elif isinstance(left, dict):
            if '__add__' in left:
                return self.vm.handle_function_call(left['__add__'], [left, right], env)
            raise TypeError("Dictionaries cannot be added directly unless they implement __add__")
        raise TypeError("Unsupported operand type(s) for +")

    def sub_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left - right
        elif isinstance(left, dict):
            if '__sub__' in left:
                return self.vm.handle_function_call(left['__sub__'], [left, right], env)
            raise TypeError("Dictionaries cannot be subtracted directly unless they implement __sub__")
        raise TypeError("Unsupported operand type(s) for -")

    def mul_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left * right
        elif isinstance(left, str):
            return left * right
        elif isinstance(left, list):
            return left * right
        elif isinstance(left, dict):
            if '__mul__' in left:
                return self.vm.handle_function_call(left['__mul__'], [left, right], env)
            raise TypeError("Dictionaries cannot be multiplied directly unless they implement __mul__")
        raise TypeError("Unsupported operand type(s) for *")

    def div_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left / right
        elif isinstance(left, dict):
            if '__div__' in left:
                return self.vm.handle_function_call(left['__div__'], [left, right], env)
            raise TypeError("Dictionaries cannot be divided directly unless they implement __div__")
        raise TypeError("Unsupported operand type(s) for /")

    def floordiv_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left // right
        elif isinstance(left, dict):
            if '__floordiv__' in left:
                return self.vm.handle_function_call(left['__floordiv__'], [left, right], env)
            raise TypeError("Dictionaries cannot be floor divided directly unless they implement __floordiv__")
        raise TypeError("Unsupported operand type(s) for //")

    def mod_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left % right
        elif isinstance(left, dict):
            if '__mod__' in left:
                return self.vm.handle_function_call(left['__mod__'], [left, right], env)
            raise TypeError("Dictionaries cannot be modulo divided directly unless they implement __mod__")
        raise TypeError("Unsupported operand type(s) for %")

    def pow_operator(self, left, right, env):
        if isinstance(left, (int, float)):
            return left ** right
        elif isinstance(left, dict):
            if '__pow__' in left:
                return self.vm.handle_function_call(left['__pow__'], [left, right], env)
            raise TypeError("Dictionaries cannot be exponentiated directly unless they implement __pow__")
        raise TypeError("Unsupported operand type(s) for **")
