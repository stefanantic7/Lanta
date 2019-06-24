class Node(object):
    def __init__(self, line_counter):
        self.line_counter = line_counter


class Null(Node):
    pass


class Program(Node):
    def __init__(self, declarations, line_counter):
        super().__init__(line_counter)
        self.children = declarations

    def __repr__(self):
        return str(self.children)


class BuiltInFunction(Node):
    def __init__(self, function, line_counter):
        super().__init__(line_counter)
        self.function = function

    def __repr__(self):
        return "BuiltInFunction node: {}".format(self.function)


class FunDecl(Node):
    def __init__(self, type_node, fun_name, args_node, stmts_node, line_counter=0):
        super().__init__(line_counter)
        self.type_node = type_node
        self.fun_name = fun_name
        self.args_node = args_node
        self.stmts_node = stmts_node


class Return(Node):
    def __init__(self, var, line_counter):
        super().__init__(line_counter)
        self.var = var


class Type(Node):
    def __init__(self, var_type, line_counter=0):
        super().__init__(line_counter)
        self.type = var_type


class Var(Node):
    def __init__(self, var, line_counter=0):
        super().__init__(line_counter)
        self.var = var


class FunctionCall(Node):
    def __init__(self, fun_name, arg_vars, line_counter):
        super().__init__(line_counter)
        self.fun_name = fun_name
        self.arg_vars = arg_vars


class VarDecl(Node):
    def __init__(self, type_node, var_node, line_counter=0):
        super().__init__(line_counter)
        self.type_node = type_node
        self.var_node = var_node


class Assign(Node):
    def __init__(self, var_node, expr, line_counter):
        super().__init__(line_counter)
        self.var_node = var_node
        self.expr = expr


class Args(Node):
    def __init__(self, args, line_counter=0):
        super().__init__(line_counter)
        self.args = args


class Stmts(Node):
    def __init__(self, stmts, line_counter=0):
        super().__init__(line_counter)
        self.stmts = stmts


class BinOp(Node):
    def __init__(self, left, op, right, line_counter):
        super().__init__(line_counter)
        self.left = left
        self.token = self.op = op
        self.right = right


class ComparisonOp(BinOp):
    pass


class LogicOp(BinOp):
    pass


class UnOp(Node):
    def __init__(self, token, bool_expr, line_counter):
        super().__init__(line_counter)
        self.token = token
        self.bool_expr = bool_expr


class Condition(Node):
    def __init__(self, condition_bool, stmts_node, line_counter):
        super().__init__(line_counter)
        self.condition_bool = condition_bool
        self.stmts_node = stmts_node


class LoopCondition(Condition):
    pass


class Num(Node):
    def __init__(self, token, line_counter):
        super().__init__(line_counter)
        self.token = token
        self.value = token.value


class ConcatStr(Node):
    def __init__(self, left, right, line_counter):
        super().__init__(line_counter)
        self.left = left
        self.right = right


class String(Node):
    def __init__(self, token, line_counter):
        super().__init__(line_counter)
        self.token = token
        self.value = token.value


class NodeVisitor(object):
    def visit(self, node):
        """
        Dynamically call method based on node type.
        Example: For type Condition, call method visit_Condition
        :param node: Node that will be visited.
        :return:
        """
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.error)
        return visitor(node)

    def error(self, node):
        raise Exception('Not found {}'.format(type(node).__name__))
