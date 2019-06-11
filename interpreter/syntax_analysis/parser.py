from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected_token):
        raise Exception('[Line: {}] Parsing error. Current token ({}) is not valid. Expected token should be: {} '
                        .format(self.lexer.line_counter, self.current_token, expected_token))

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(type)

    def program(self):
        """
        program                     : declarations

        declarations                : (import_function | function_declaration | statement_list)*
        """
        declarations = []

        while self.current_token.type is not EOF:
            if self.current_token.type == USE:
                declarations.extend(self.import_function())
            elif self.current_token.type == DECFUN:
                declarations.append(self.function_declaration())
            else:
                declarations.append(self.statement_list())

        return Program(declarations, self.lexer.line_counter)

    def import_function(self):
        """
        import_function             : ID<'use'> ID (COMMA ID)*

        :return:
        """
        built_in_functions = []
        self.eat(USE)
        built_in_functions.append(BuiltInFunction(self.current_token.value, self.lexer.line_counter))
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            built_in_functions.append(BuiltInFunction(self.current_token.value, self.lexer.line_counter))
            self.eat(ID)

        self.eat(SEMICOLON)

        return built_in_functions

    def function_declaration(self):
        """
        function_declaration        : ID<'decfun'> ID LPAREN parameters RPAREN COLON function_type_spec function_body
        function_type_spec          : (int | float | string | array | boolean | do)
        function_body               : LBRACKET statement_list* RBRACKET

        :return:
        """
        line_counter = self.lexer.line_counter
        self.eat(DECFUN)
        fun_name = self.current_token.value
        self.eat(ID)

        self.eat(LPAREN)
        parameters_node = Args(self.parameters(), self.lexer.line_counter)
        self.eat(RPAREN)

        self.eat(COLON)

        type_node = Type(self.current_token.value, self.lexer.line_counter)
        self.eat(TYPE)

        statements = []
        self.eat(LBRACKET)
        while self.current_token.type != RBRACKET:
            statements.append(self.statement_list())
        self.eat(RBRACKET)

        stmts_node = Stmts(statements, self.lexer.line_counter)
        return FunDecl(type_node=type_node, fun_name=fun_name, args_node=parameters_node, stmts_node=stmts_node, line_counter=line_counter)

    def parameters(self):
        """
        parameters                  : empty
                                    | param (COMMA param)*

        param                       : variable COLON type_spec
        variable                    : DOLLAR ID
        type_spec                   : (int | float | string | array | boolean)

        :return:
        """
        line_counter = self.lexer.line_counter
        params = []

        while self.current_token.type != RPAREN:
            var_name = self.current_token.value
            if var_name[0] != '$':
                self.error('($) DOLLAR sign')
            self.eat(ID)
            self.eat(COLON)
            type_node = Type(self.current_token.value, self.lexer.line_counter)
            self.eat(TYPE)
            var_node = Var(var_name, self.lexer.line_counter)

            params.append(VarDecl(type_node, var_node, line_counter))

            if self.current_token.type == COMMA:
                self.eat(COMMA)

        return params

    def statement_list(self):
        """
        statement_list              : var_declaration_list
                                    | function_call SEMICOLON
                                    | condition_statement
                                    | loop_condition
                                    | return_statement
                                    | empty

        :return:
        """
        statements = []
        if self.current_token.type == ID and self.current_token.value[0] == '@':
            statements.append(self.function_call())
            self.eat(SEMICOLON)
        elif self.current_token.type == DEC:
            statements.extend(self.var_declaration_list())
        elif self.current_token.type == COND:
            statements.append(self.condition_statement())
        elif self.current_token.type == LOOND:
            statements.append(self.loop_condition())
        elif self.current_token.type == RETURN:
            statements.append(self.return_statement())
        else:
            self.error("function call, declaration, condition, loop, return")

        return Stmts(statements, self.lexer.line_counter)

    def function_call(self):
        line_counter = self.lexer.line_counter
        fun_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        parameters = []
        while self.current_token.type != RPAREN:
            var_node = Var(self.current_token.value, self.lexer.line_counter)
            parameters.append(var_node)
            self.eat(ID)

            if self.current_token.type == COMMA:
                self.eat(COMMA)

        self.eat(RPAREN)

        return FunctionCall(fun_name, parameters, line_counter)

    def condition_statement(self):
        line_counter = self.lexer.line_counter
        self.eat(COND)
        self.eat(LPAREN)
        node = self.bool_expr()
        self.eat(RPAREN)
        self.eat(LBRACKET)

        statements = []
        while self.current_token.type != RBRACKET:
            statements.append(self.statement_list())

        node = Condition(node, Stmts(statements, self.lexer.line_counter), line_counter)
        self.eat(RBRACKET)

        return node

    def loop_condition(self):
        line_counter = self.lexer.line_counter
        self.eat(LOOND)
        self.eat(LPAREN)
        node = self.bool_expr()
        self.eat(RPAREN)
        self.eat(LBRACKET)

        statements = []
        while self.current_token.type != RBRACKET:
            statements.append(self.statement_list())

        node = LoopCondition(node, Stmts(statements, self.lexer.line_counter), line_counter)
        self.eat(RBRACKET)

        return node

    def return_statement(self):
        line_counter = self.lexer.line_counter
        self.eat(RETURN)
        var_node = Var(self.current_token.value, self.lexer.line_counter)
        self.eat(ID)
        self.eat(SEMICOLON)
        node = Return(var_node, line_counter)

        return node

    def var_declaration_list(self):
        """
        var_declaration_list        : ID<'dec'> variable COLON type_spec var_initialization SEMICOLON

        variable                    : DOLLAR ID
        type_spec                   : (int | float | string | array | boolean)

        :return:
        """
        declarations = []

        self.eat(DEC)

        var_name = self.current_token.value
        if var_name[0] != '$':
            self.error('($) DOLLAR sign')

        self.eat(ID)
        self.eat(COLON)
        type_node = Type(self.current_token.value, self.lexer.line_counter)
        self.eat(TYPE)
        var_node = Var(var_name, self.lexer.line_counter)

        declarations.append(VarDecl(type_node, var_node, self.lexer.line_counter))

        declarations.extend(self.var_initialization(var_node, type_node))
        self.eat(SEMICOLON)

        return declarations

    def var_initialization(self, var_node, type_node):
        """
        var_initialization          : (ASSIGN (expr | string_expr | bool_expr))?

        :param type_node:
        :param var_node:
        :return:
        """
        declarations = []
        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)

            if type_node.type in ('int', 'float'):
                declarations.append(Assign(var_node, self.expr(), self.lexer.line_counter))
            elif type_node.type == 'string':
                declarations.append(Assign(var_node, self.string_expr(), self.lexer.line_counter))
            elif type_node.type == 'array':
                declarations.append(Assign(var_node, self.string_expr(), self.lexer.line_counter))

        return declarations

    def factor(self):
        """
        factor              : PLUS factor
                            | MINUS factor
                            | INT_NUMBER
                            | FLOAT_NUMBER
                            | LPAREN expr RPAREN
                            | variable
                            | function_call

        :return:
        """
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token, self.lexer.line_counter)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token, self.lexer.line_counter)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            if token.value[0] == '@':
                return self.function_call()
            elif token.value[0] == '$':
                self.eat(ID)
                return Var(token.value, self.lexer.line_counter)
            else:
                self.error('variable or function call')

    def term(self):
        """
        term                        : factor ((MUL | DIV | REAL_DIV | MOD) factor)*

        :return:
        """
        node = self.factor()

        while self.current_token.type in (MUL, DIV, REAL_DIV, MOD):
            token = self.current_token
            if token.type in (MUL, DIV, REAL_DIV, MOD):
                self.eat(token.type)
            else:
                self.error(' or '.join([MUL, DIV, REAL_DIV, MOD]))

            node = BinOp(left=node, op=token, right=self.factor(), line_counter=self.lexer.line_counter)

        return node

    def expr(self):
        """
        expr                        : term ((PLUS | MINUS) term)*

        :return:
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error(' or '.join([PLUS, MINUS]))

            node = BinOp(left=node, op=token, right=self.expr(), line_counter=self.lexer.line_counter)

        return node

    def string_term(self):
        """
        string_term                 : STRING | variable | function_call

        :return:
        """
        token = self.current_token
        if token.type == STRING:
            self.eat(STRING)
            return String(token, self.lexer.line_counter)
        elif token.type == ID:
            if token.value[0] == '@':
                return self.function_call()
            elif token.value[0] == '$':
                self.eat(ID)
                return Var(token.value, self.lexer.line_counter)
            else:
                self.error('String, variable or function call')

    def string_expr(self):
        """
        string_expr                 : string_term (DOT string_term)*

        :return:
        """
        node = self.string_term()
        while self.current_token.type == DOT:
            self.eat(DOT)

            node = ConcatStr(left=node, right=self.string_expr(), line_counter=self.lexer.line_counter)
        return node

    def bool_expr(self):
        """
        bool_expr                   : bool_simple_expr | bool_complex_expr

        :return:
        """
        if self.current_token.type == INTEGER or self.current_token.type == ID:
            return self.bool_simple_expr()
        else:
            return self.bool_complex_expr()

    def bool_simple_expr(self):
        """
        bool_simple_expr            : expr comparision_operation expr (comparision_operation expr)*

        :return:
        """
        node = self.expr()

        token = self.current_token
        if token.type in (LESS, LESS_EQ, GREATER, GREATER_EQ, EQUAL, NOT_EQUAL):
            self.eat(token.type)
        else:
            self.error(' or '.join([LESS, LESS_EQ, GREATER, GREATER_EQ, EQUAL, NOT_EQUAL]))

        node = ComparationOp(left=node, op=token, right=self.expr(), line_counter=self.lexer.line_counter)

        return node

    def bool_complex_expr(self):
        """
        bool_complex_expr           : logic_unar_operation? LPAREN bool_simple_expr RPAREN
                                        (logic_operation logic_unar_operation? LPAREN bool_simple_expr RPAREN)*

        :return:
        """
        if self.current_token.type == NOT:
            un_token = self.current_token
            self.eat(NOT)
            self.eat(LPAREN)
            node = self.bool_simple_expr()
            self.eat(RPAREN)

            node = UnOp(un_token, node, self.lexer.line_counter)
        else:
            self.eat(LPAREN)
            node = self.bool_simple_expr()
            self.eat(RPAREN)

        while self.current_token.type in (AND, OR):
            token = self.current_token
            self.eat(self.current_token.type)

            if self.current_token.type == NOT:
                un_token = self.current_token
                self.eat(NOT)
                self.eat(LPAREN)

                node = BinOp(node, token, UnOp(un_token, self.bool_simple_expr(), self.lexer.line_counter), self.lexer.line_counter)

                self.eat(RPAREN)

            else:
                self.eat(LPAREN)

                node = BinOp(node, token, self.bool_simple_expr(), self.lexer.line_counter)

                self.eat(RPAREN)

        return node

    def parse(self):
        return self.program()
