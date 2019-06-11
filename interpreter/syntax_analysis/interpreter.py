class AST(object):
    def __init__(self, line_counter):
        self.line_counter = line_counter

class Null(AST):
    pass

class Program(AST):
    def __init__(self, declarations, line_counter):
        super().__init__(line_counter)
        self.children = declarations

    def __repr__(self):
        return str(self.children)

class BuiltInFunction(AST):
    def __init__(self, function, line_counter):
        super().__init__(line_counter)
        self.function = function

    def __repr__(self):
        return "BuiltInFunction node: {}".format(self.function)

class FunDecl(AST):
    def __init__(self, type_node, fun_name, args_node, stmts_node, line_counter=0):
        super().__init__(line_counter)
        self.type_node = type_node
        self.fun_name = fun_name
        self.args_node = args_node
        self.stmts_node = stmts_node

class Return(AST):
    def __init__(self, var, line_counter):
        super().__init__(line_counter)
        self.var = var

class Type(AST):
    def __init__(self, type, line_counter=0):
        super().__init__(line_counter)
        self.type = type

class Var(AST):
    def __init__(self, var, line_counter=0):
        super().__init__(line_counter)
        self.var = var

class FunctionCall(AST):
    def __init__(self, fun_name, arg_vars, line_counter):
        super().__init__(line_counter)
        self.fun_name = fun_name
        self.arg_vars = arg_vars

class VarDecl(AST):
    def __init__(self, type_node, var_node, line_counter=0):
        super().__init__(line_counter)
        self.type_node = type_node
        self.var_node = var_node

class Assign(AST):
    def __init__(self, var_node, expr, line_counter):
        super().__init__(line_counter)
        self.var_node = var_node
        self.expr = expr

class Args(AST):
    def __init__(self, args, line_counter=0):
        super().__init__(line_counter)
        self.args = args

class Stmts(AST):
    def __init__(self, stmts, line_counter=0):
        super().__init__(line_counter)
        self.stmts = stmts

class BinOp(AST):
    def __init__(self, left, op, right, line_counter):
        super().__init__(line_counter)
        self.left = left
        self.token = self.op = op
        self.right = right

class ComparationOp(BinOp):
    pass

class LogicOp(BinOp):
    pass

class UnOp(AST):
    def __init__(self, token, bool_expr, line_counter):
        super().__init__(line_counter)
        self.token = token
        self.bool_expr = bool_expr

class Condition(AST):
    def __init__(self, condition_bool, stmts_node, line_counter):
        super().__init__(line_counter)
        self.condition_bool = condition_bool
        self.stmts_node = stmts_node

class LoopCondition(Condition):
    pass

class Num(AST):
    def __init__(self, token, line_counter):
        super().__init__(line_counter)
        self.token = token
        self.value = token.value

class ConcatStr(AST):
    def __init__(self, left, right, line_counter):
        super().__init__(line_counter)
        self.left = left
        self.right = right

class String(AST):
    def __init__(self, token, line_counter):
        super().__init__(line_counter)
        self.token = token
        self.value = token.value

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.error)
        return visitor(node)

    def error(self, node):
        raise Exception('Not found {}'.format(type(node).__name__))
