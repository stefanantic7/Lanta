import argparse
import textwrap

from interpreter.lexical_analysis.lexer import Lexer
from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import NodeVisitor, VarDecl, Assign, Stmts
from interpreter.syntax_analysis.parser import Parser
from built_in_fun_generator import built_in_impl_map


class ASTVisualizer(NodeVisitor):

    def __init__(self, parser):
        self.num_tabs = 0

        self.parser = parser
        self.nodecount = 1
        self.dot_heder = [textwrap.dedent("""
            ## Coded by Antole.
        """)]
        self.dot_body = []
        self.dot_footer = ['']

        self.py_built_in_fun_map = {
            'cput': 'print',
            'cget': 'input'
        }
        self.comparison_op_map = {
            '&&': 'and',
            '||': 'or'
        }
    def increment_tabs(self):
        self.num_tabs += 1

    def decrement_tabs(self):
        self.num_tabs -= 1

    def generate_tabs(self):
        tabs = ''
        for i in range(self.num_tabs):
            tabs = tabs + '\t'
        return tabs

    def visit_Program(self, node):
        node.num = self.nodecount
        self.nodecount += 1

        for child in node.children:
            self.visit(child)

    def visit_BuiltInFunction(self, node):
        if node.function in built_in_impl_map:
            s = built_in_impl_map[node.function]
            self.dot_heder.append(s)


    def visit_VarDecl(self, node):
        node.num = self.nodecount
        self.nodecount += 1

        self.visit(node.type_node)

        self.visit(node.var_node)

    def visit_Assign(self, node):
        node.num = self.nodecount
        self.nodecount += 1

        s = '='
        self.dot_body.append(s)

        self.visit(node.expr)

    def visit_FunDecl(self, node):
        s = 'def {}('.format(node.fun_name)
        self.dot_body.append(s)
        self.visit(node.args_node)

        s = '):\n'
        self.dot_body.append(s)
        self.increment_tabs()

        self.visit(node.stmts_node)

        self.decrement_tabs()


    def visit_Return(self, node):
        s = 'return '.format(self.nodecount)
        self.dot_body.append(s)

        self.visit(node.var)

    def visit_Args(self, node):
        for child in node.args:
            self.visit(child)
            if child != node.args[-1]:
                self.dot_body.append(', ')

    def visit_Stmts(self, node):
        for child in node.stmts:
            if not isinstance(child, Assign) and not isinstance(child, Stmts):
                self.dot_body.append(self.generate_tabs())

            self.visit(child)

            if not isinstance(child, VarDecl) and not isinstance(child, Stmts):
                self.dot_body.append('\n')

    def visit_Type(self, node):
        node.num = self.nodecount
        self.nodecount += 1

    def visit_Var(self, node):
        s = node.var[1:]
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_FunctionCall(self, node):

        fun_name = node.fun_name[1:]
        if fun_name in self.py_built_in_fun_map:
            fun_name = self.py_built_in_fun_map[fun_name]

        s = '{}('.format(fun_name)
        self.dot_body.append(s)

        for child in node.arg_vars:
            self.visit(child)
            if child != node.arg_vars[-1]:
                s = ', '
                self.dot_body.append(s)

        s = ')'
        self.dot_body.append(s)


    def visit_BinOp(self, node):
        node.num = self.nodecount
        self.nodecount += 1

        self.dot_body.append('(')

        self.visit(node.left)

        s = node.op.value
        if s in self.comparison_op_map:
            s = self.comparison_op_map[s]
        self.dot_body.append(s)

        self.visit(node.right)

        self.dot_body.append(')')


    def visit_UnOp(self, node):
        s = 'not' #TODO: get from map
        self.dot_body.append(s)
        self.visit(node.bool_expr)

    def visit_Condition(self, node):
        s = 'if '
        self.dot_body.append(s)

        self.visit(node.condition_bool)

        s = ':\n'
        self.dot_body.append(s)
        self.increment_tabs()

        self.visit(node.stmts_node)

        self.decrement_tabs()

    def visit_LoopCondition(self, node):
        s = 'while '
        self.dot_body.append(s)

        self.visit(node.condition_bool)

        s = ':\n'
        self.dot_body.append(s)
        self.increment_tabs()

        self.visit(node.stmts_node)

        self.decrement_tabs()

    def visit_ComparationOp(self, node):
        self.dot_body.append('(')

        self.visit(node.left)

        s = node.op.value
        self.dot_body.append(s)

        self.visit(node.right)

        self.dot_body.append(')')


    def visit_Num(self, node):
        s = str(node.value)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_String(self, node):
        s = node.value
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_ConcatStr(self, node):
        node.num = self.nodecount
        self.nodecount += 1

        self.visit(node.left)

        s = '+'
        self.dot_body.append(s)

        self.visit(node.right)

    def genDot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_heder + self.dot_body + self.dot_footer)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fname')
    args = argparser.parse_args()
    fname = args.fname

    # fname = './examples/test1.txt'

    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.genDot()

    print(content)


if __name__ == '__main__':
    main()
