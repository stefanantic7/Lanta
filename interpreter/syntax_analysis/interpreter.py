class AST(object):
    pass

class Program(AST):
    def __init__(self, declarations):
        self.children = declarations

    def __repr__(self):
        return str(self.children)

class BuiltInFunction(AST):
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return "BuiltInFunction node: {}".format(self.function)

class FunDecl(AST):
    def __init__(self, type_node, fun_name, args_node, stmts_node):
        self.type_node = type_node
        self.fun_name = fun_name
        self.args_node = args_node
        self.stmts_node = stmts_node

class Return(AST):
    def __init__(self, var):
        self.var = var

class Type(AST):
    def __init__(self, type):
        self.type = type

class Var(AST):
    def __init__(self, var):
        self.var = var

class VarDecl(AST):
    def __init__(self, type_node, var_node):
        self.type_node = type_node
        self.var_node = var_node

    def __repr__(self):
        return "VarDecl node: type({}), var({})".format(self.type_node, self.var_node)

class Assign(AST):
    def __init__(self, var_node, expr):
        self.var_node = var_node
        self.expr = expr

class Args(AST):
    def __init__(self, args):
        self.args = args

class Stmts(AST):
    def __init__(self, stmts):
        self.stmts = stmts

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class ComparationOp(BinOp):
    pass

class LogicOp(BinOp):
    pass

class UnOp(AST):
    def __init__(self, token, bool_expr):
        self.token = token
        self.bool_expr = bool_expr

class Condition(AST):
    def __init__(self, condition_bool, stmts_node):
        self.condition_bool = condition_bool
        self.stmts_node = stmts_node

class LoopCondition(Condition):
    pass

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class ConcatStr(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.error)
        return visitor(node)

    def error(self, node):
        raise Exception('Not found {}'.format(type(node).__name__))
