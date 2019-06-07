from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import *
from interpreter.syntax_analysis.util import restorable


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Greska u parsiranju')

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

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
                declarations.extend(self.statement_list())

        return Program(declarations)

    @restorable
    def check_function(self):
        self.eat(TYPE)
        self.eat(ID)
        return self.current_token.type == LPAREN

    @restorable
    def is_bool_expr(self):
        it_is = False
        while self.current_token.type != SEMICOLON:
            if self.current_token.type in (LESS, LESS_EQ, GREATER, GREATER_EQ, EQUAL, NOT_EQUAL):
                it_is = True
                break
        return it_is
    def import_function(self):
        """
        import_function             : ID<'use'> ID (COMMA ID)*

        :return:
        """
        built_in_functions = []
        self.eat(USE)
        # TODO: Check if function exists
        built_in_functions.append(BuiltInFunction(self.current_token.value))
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            built_in_functions.append(BuiltInFunction(self.current_token.value))
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
        self.eat(DECFUN)

        fun_name = self.current_token.value
        self.eat(ID)

        self.eat(LPAREN)
        parameters_node = Args(self.parameters())
        self.eat(RPAREN)

        self.eat(COLON)

        type_node = Type(self.current_token.value)
        self.eat(TYPE)

        self.eat(LBRACKET)
        stmts_node = Stmts(self.statement_list())
        self.eat(RBRACKET)

        return FunDecl(type_node=type_node, fun_name=fun_name, args_node=parameters_node, stmts_node=stmts_node)

    def parameters(self):
        """
        parameters                  : empty
                                    | param (COMMA param)*

        param                       : variable COLON type_spec
        variable                    : DOLLAR ID
        type_spec                   : (int | float | string | array | boolean)

        :return:
        """
        params = []

        while self.current_token.type != RPAREN:
            # TODO: Should start with DOLLAR sign
            var_name = self.current_token.value
            self.eat(ID)
            self.eat(COLON)
            type_node = Type(self.current_token.value)
            self.eat(TYPE)
            var_node = Var(var_name)

            params.append(VarDecl(type_node, var_node))

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
        if self.current_token.type == DEC:
            statements.extend(self.var_declaration_list())
        elif self.current_token.type == COND:
            # TODO
            statements.append(self.condition_statement())
        elif self.current_token.type == LOOND:
            # TODO
            statements.append(self.loop_condition())
        elif self.current_token.type == RETURN:
            # TODO
            statements.append(self.return_statement())

        return statements

    def condition_statement(self):
        node = None

        return node

    def loop_condition(self):
        node = None

        return node

    def return_statement(self):
        node = None

        return Node

    def var_declaration_list(self):
        """
        var_declaration_list        : ID<'dec'> variable COLON type_spec var_initialization SEMICOLON

        variable                    : DOLLAR ID
        type_spec                   : (int | float | string | array | boolean)

        :return:
        """
        declarations = []

        self.eat(DEC)
        # TODO: Should start with DOLLAR sign
        var_name = self.current_token.value
        self.eat(ID)
        self.eat(COLON)
        type_node = Type(self.current_token.value)
        self.eat(TYPE)
        var_node = Var(var_name)

        declarations.append(VarDecl(type_node, var_node))

        declarations.extend(self.var_initialization(var_node, type_node))

        self.eat(SEMICOLON)

        return declarations

    def var_initialization(self, var_node, type_node):
        """
        var_initialization          : (ASSIGN (expr | string_expr | bool_expr))?

        :param var_node:
        :return:
        """
        declarations = []
        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)

            # TODO: Maybe should do check in node visitor?
            # if type is int, then expr
            # if type is boolean, than bool_expr
            # if type is string, than string_expr

            if type_node.type == 'int':
                # TODO: check if var is declared as integer
                declarations.append(Assign(var_node, self.expr()))

            elif type_node.type == 'float':
                # TODO: check if var is declared as float
                declarations.append(Assign(var_node, self.expr()))

            elif type_node.type == 'string':
                # TODO: check if var is declared as string
                declarations.append(Assign(var_node, self.string_expr()))

            elif type_node.type == 'boolean':
                # TODO: check if var is declared as string
                declarations.append(Assign(var_node, self.bool_expr()))

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
            return Num(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            self.eat(ID)
            return Var(token.value)

    def term(self):
        """
        term                        : factor ((MUL | DIV | REAL_DIV | MOD) factor)*

        :return:
        """
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            else:
                self.error()

            node = BinOp(left=node, op=token, right=self.factor())

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
                self.error()

            node = BinOp(left=node, op=token, right=self.expr())

        return node

    def string_term(self):
        """
        string_term                 : STRING | variable | function_call

        :return:
        """
        token = self.current_token
        if token.type == STRING:
            self.eat(STRING)
            return String(token)
        elif token.type == ID:
            self.eat(ID)
            return Var(token)

    def string_expr(self):
        """
        string_expr                 : string_term (DOT string_term)*

        :return:
        """
        node = self.string_term()
        while self.current_token.type == DOT:
            self.eat(DOT)

            node = ConcatStr(left=node, right=self.string_expr())
        return node

    def bool_expr(self):
        """
        bool_expr                   : bool_simple_expr | bool_complex_expr

        :return:
        """
        if self.current_token.type == INTEGER:
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
            self.error()

        node = ComparationOp(left=node, op=token, right=self.expr())

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

            node = UnOp(un_token, node)
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

                node = BinOp(node, token, UnOp(un_token, self.bool_simple_expr()))

                self.eat(RPAREN)

            else:
                self.eat(LPAREN)

                node = BinOp(node, token, self.bool_simple_expr())

                self.eat(RPAREN)

        return node

    def parse(self):
        return self.program()
