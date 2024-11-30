class Environment:
    def __init__(self, parent=None):
        self.env = {}
        self.parent = parent

    def lookup(self, symbol):
        if symbol in self.env:
            return self.env[symbol]
        elif self.parent:
            return self.parent.lookup(symbol)
        else:
            raise NameError(f"Undefined symbol: {symbol}")

    def extend(self, symbols, values):
        new_env = Environment(self)
        new_env.env.update(zip(symbols, values))
        return new_env

    def define(self, symbol, value):
        self.env[symbol] = value

def eval_expr(expr, env):
    if isinstance(expr, (int, float)):  # number
        return expr
    elif isinstance(expr, str):  # symbol
        return env.lookup(expr)
    elif isinstance(expr, list):  # list (compound expression)
        proc = eval_expr(expr[0], env)
        args = [eval_expr(arg, env) for arg in expr[1:]]
        return apply_proc(proc, args)
    else:
        raise TypeError(f"Unknown expression type: {expr}")

def apply_proc(proc, args):
    if callable(proc):  # primitive procedure
        return proc(*args)
    elif isinstance(proc, list):  # user-defined procedure
        params, body, proc_env = proc
        extended_env = proc_env.extend(params, args)
        return eval_expr(body, extended_env)
    else:
        raise TypeError(f"Unknown procedure type: {proc}")

def primitive_add(*args):
    return sum(args)

# Setup initial environment
global_env = Environment()
global_env.define('+', primitive_add)

# Example usage
expr = ['+', 2, 3]
result = eval_expr(expr, global_env)
print(result)  # Output should be 5
