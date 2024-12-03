# a calc

class Env:
    def __init__(self, parent=None):
        self.var_dict = {}
        self.parent = parent
    
    def lookup(self, name):
        if name in self.var_dict:
            return self.var_dict[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Undefined variable '{name}'")


def eval(ast, env):
    op = ast[0]
    if op == '+':
        return eval(ast[1], env) + eval(ast[2], env)
    elif op == '-':
        return eval(ast[1], env) - eval(ast[2], env)
    elif op == '*':
        return eval(ast[1], env) * eval(ast[2], env)
    elif op == '/':
        return eval(ast[1], env) / eval(ast[2], env)
    elif op == '%':
        return eval(ast[1], env) % eval(ast[2], env)
    else:
        raise Exception('Invalid operator')



