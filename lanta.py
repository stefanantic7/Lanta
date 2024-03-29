import argparse
import textwrap

from exceptions import CompileException
from interpreter.lexical_analysis.lexer import Lexer
from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import NodeVisitor, VarDecl, Assign, Stmts, Return, LoopCondition, Condition
from interpreter.syntax_analysis.parser import Parser
from built_in_fun_generator import built_in_impl_map, built_in_metadata_map


class PythonGenerator(NodeVisitor):

    def __init__(self, parser):
        self.num_tabs = 0

        self.parser = parser
        self.dot_heder = [textwrap.dedent("""
            ## Coded by Antole.
        """)]
        self.dot_body = []
        self.dot_footer = ['']

        self.comparison_op_map = {
            '&&': 'and',
            '||': 'or'
        }
        self.current_scope = 'main'
        self.var_memory = {}
        self.function_memory = {}

    def error_message(self, line, message):
        raise CompileException(f"[Line: {line}] {message}")

    def add_var_to_memory(self, var_name, var_type):
        if self.current_scope in self.var_memory:
            self.var_memory[self.current_scope].append({'name': var_name, 'type': var_type})
        else:
            self.var_memory[self.current_scope] = [{'name': var_name, 'type': var_type}]

    def is_var_visible(self, var_name, given_scope):
        if given_scope in self.var_memory:
            for var in self.var_memory[given_scope]:
                if var['name'] == var_name:
                    return True

        return False

    def get_var_type(self, var_name, scope):
        for variable in self.var_memory[scope]:
            if var_name == variable['name']:
                return variable['type']
        return None

    def get_func_type(self, fun_name):
        for fun in self.function_memory:
            if fun == fun_name:
                return self.function_memory[fun]['return_type']
        return None

    def add_func_to_memory(self, fun_name, args_node, return_type):
        parameter_names = []
        parameter_types = []
        for arg in args_node.args:
            parameter_names.append(arg.var_node.var)
            parameter_types.append(arg.type_node.type)

        self.function_memory[fun_name] = {
            'parameter_names': parameter_names,
            'parameter_types': parameter_types,
            'return_type': return_type
        }

    def check_func_visibility(self, fun_name):
        if fun_name in self.function_memory:
            return True

        return False

    def check_func_parameters_count(self, fun_name, parameters):
        return len(self.function_memory[fun_name]['parameter_names']) == len(parameters)

    def check_func_parameter_types(self, fun_name, parameter_types):
        for i in range(len(self.function_memory[fun_name]['parameter_types'])):
            if self.function_memory[fun_name]['parameter_types'][i] == 'any':
                continue
            if self.function_memory[fun_name]['parameter_types'][i] != self.get_var_type(parameter_types[i].var, self.current_scope):
                return False
        return True

    def check_if_func_has_return(self, stmts_node):
        has_return = False
        for statement in stmts_node.stmts:
            if isinstance(statement, Stmts):
                if self.check_if_func_has_return(statement):
                    has_return = True
            elif isinstance(statement, Return):
                has_return = True
        return has_return

    def get_func_parameters_count(self, fun_name):
        return len(self.function_memory[fun_name]['parameter_names'])

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
        for child in node.children:
            self.visit(child)

    def visit_BuiltInFunction(self, node):
        s = '# imported {}\n'.format(node.function)
        self.dot_heder.append(s)
        if node.function not in built_in_metadata_map:
            self.error_message(node.line_counter, "Function {} does not exist in built in functions".format(node.function))
        fun_declaration = built_in_metadata_map[node.function]
        self.add_func_to_memory(fun_declaration.fun_name, fun_declaration.args_node, fun_declaration.type_node.type)

        if node.function in built_in_impl_map:
            s = built_in_impl_map[node.function]
            self.dot_heder.append(s)

    def visit_VarDecl(self, node):
        if not self.is_var_visible(node.var_node.var, self.current_scope):
            self.add_var_to_memory(node.var_node.var, node.type_node.type)

        self.visit(node.type_node)

        self.visit(node.var_node)

    def visit_Assign(self, node):
        s = '='
        self.dot_body.append(s)

        self.visit(node.expr)

    def visit_Null(self, node):
        s = 'None'
        self.dot_body.append(s)

    def visit_FunDecl(self, node):
        if node.type_node.type != 'do' and not self.check_if_func_has_return(node.stmts_node):
            self.error_message(node.line_counter,
                               "Function {} does not have return statement". format(node.fun_name))

        self.add_func_to_memory(node.fun_name, node.args_node, node.type_node.type)

        self.current_scope = node.fun_name

        s = 'def {}('.format(node.fun_name)
        self.dot_body.append(s)
        self.visit(node.args_node)

        s = '):\n'

        self.dot_body.append(s)
        self.increment_tabs()

        self.visit(node.stmts_node)

        self.decrement_tabs()
        self.current_scope = 'main'


    def visit_Return(self, node):
        if self.current_scope == 'main':
            self.error_message(node.line_counter, 'Only functions should have return statement')
        if self.get_func_type(self.current_scope) != self.get_var_type(node.var.var, self.current_scope):
            self.error_message(node.line_counter,
                               "Return type should be {}, {} returned"
                               .format(self.get_func_type(self.current_scope), self.get_var_type(node.var.var, self.current_scope)))

        s = 'return '
        self.dot_body.append(s)

        self.visit(node.var)

    def visit_Args(self, node):
        for child in node.args:
            self.visit(child)
            if child != node.args[-1]:
                self.dot_body.append(', ')

    def visit_Stmts(self, node):
        if len(node.stmts) == 0:
            self.dot_body.append(self.generate_tabs())
            self.dot_body.append('pass\n')
            self.decrement_tabs()

        for child in node.stmts:
            if not isinstance(child, Assign) and not isinstance(child, Stmts):
                self.dot_body.append(self.generate_tabs())

            self.visit(child)

            if not isinstance(child, VarDecl) and not isinstance(child, Stmts):
                self.dot_body.append('\n')

    def visit_Type(self, node):
        pass

    def visit_Var(self, node):
        if not self.is_var_visible(node.var, self.current_scope):
            self.error_message(node.line_counter, 'Variable {} is not defined'.format(node.var))

        s = node.var[1:]
        self.dot_body.append(s)

    def visit_FunctionCall(self, node):
        if not self.check_func_visibility(node.fun_name[1:]):
            self.error_message(node.line_counter, 'Function {} is not defined'.format(node.fun_name))
        if not self.check_func_parameters_count(node.fun_name[1:], node.arg_vars):
            self.error_message(node.line_counter,
                               'Function {} expect {} parameter(s), {} given.'
                               .format(node.fun_name, self.get_func_parameters_count(node.fun_name[1:]), len(node.arg_vars)))
        if not self.check_func_parameter_types(node.fun_name[1:], node.arg_vars):
            self.error_message(node.line_counter,
                               "The arguments type does not match with arguments of function {}".format(node.fun_name[1:]))

        fun_name = node.fun_name[1:]

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
        self.dot_body.append('(')

        self.visit(node.left)

        s = node.op.value
        if s in self.comparison_op_map:
            s = self.comparison_op_map[s]
        self.dot_body.append(s)

        self.visit(node.right)

        self.dot_body.append(')')

    def visit_UnOp(self, node):
        if node.token.type == NOT:
            s = 'not'
        else:
            s = '-'
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

    def visit_ComparisonOp(self, node):
        self.dot_body.append('(')

        self.visit(node.left)

        s = node.op.value
        self.dot_body.append(s)

        self.visit(node.right)

        self.dot_body.append(')')

    def visit_Num(self, node):
        s = str(node.value)
        self.dot_body.append(s)

    def visit_String(self, node):
        s = node.value
        self.dot_body.append(s)

    def visit_ConcatStr(self, node):
        self.visit(node.left)

        s = '+'
        self.dot_body.append(s)

        self.visit(node.right)

    def generate_python(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_heder + self.dot_body + self.dot_footer)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file_name')
    args = arg_parser.parse_args()
    file_name = args.file_name

    text = open(file_name, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    python_generator = PythonGenerator(parser)
    content = python_generator.generate_python()

    print(content)


if __name__ == '__main__':
    main()
