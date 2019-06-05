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
        declarations = []
        print(self.current_token)
        while self.current_token.type in [USE, DEC]:
            if self.current_token.type == USE:
                declarations.extend(self.include_functions())
            elif self.current_token.type == DEC:
                declarations.extend(self.var_declaration_list())
            # elif self.check_function():
            #     declarations.append(self.function_declarations())
            # else:
            #     declarations.extend(self.var_declaration_list())

        return Program(declarations)

    @restorable
    def check_function(self):
        self.eat(TYPE)
        self.eat(ID)
        return self.current_token.type == LPAREN

    def include_functions(self):
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

    def function_declarations(self):
        type_node = Type(self.current_token.value)
        self.eat(TYPE)

        fun_name = self.current_token.value
        self.eat(ID)

        self.eat(LPAREN)
        args_node = Args(self.argument_list())
        self.eat(RPAREN)

        self.eat(LBRACKET)
        stmts_node = Stmts(self.statement_list())
        self.eat(RBRACKET)

        return FunDecl(type_node=type_node, fun_name=fun_name, args_node=args_node, stmts_node=stmts_node)

    def argument_list(self):
        params = []

        while self.current_token.type != RPAREN:
            type_node = Type(self.current_token.value)
            self.eat(TYPE)

            var_node = Var(self.current_token.value)
            self.eat(ID)

            params.append(VarDecl(type_node, var_node))

            if self.current_token.type == COMMA:
                self.eat(COMMA)


        return params

    def statement_list(self):
        statements = []

        return statements


    def var_declaration_list(self):

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

        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)

            # if type is int, then expr
            # if type is boolean, than bool_expr
            # if type is string, than string_expr

            if self.current_token.type == INTEGER:
                # TODO: check if var is declared as integer
                declarations.append(Assign(var_node, self.expr()))

            elif self.current_token.type == FLOAT:
                # TODO: check if var is declared as float
                declarations.append(Assign(var_node, self.expr()))

            elif self.current_token.type == STRING:
                # TODO: check if var is declared as string
                declarations.append(Assign(var_node, self.string_expr()))

        self.eat(SEMICOLON)

        return declarations

    def factor(self):
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

    def term(self):
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
        token = self.current_token

        self.eat(STRING)
        return String(token)

    def string_expr(self):
        node = self.string_term()
        while self.current_token.type == DOT:
            self.eat(DOT)

            node = ConcatStr(left=node, right=self.string_expr())
        return node

    def parse(self):
       return self.program()