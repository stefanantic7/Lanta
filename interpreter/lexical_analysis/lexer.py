from interpreter.lexical_analysis.token import Token
from interpreter.lexical_analysis.tokenType import *

# term | token type
# 123 => integer
# int => type


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line_counter = 1
        if len(text) > 0:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def error(self):
        raise Exception('Neocekivani karakter {} '.format(self.current_char))

    def new_line(self):
        self.line_counter += 1

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def number(self):
        number_value = ""

        while self.current_char is not None and self.current_char.isdigit():
            number_value += self.current_char
            self.advance()
        if self.current_char == '.':
            number_value += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                number_value += self.current_char
                self.advance()
            return Token(FLOAT, float(number_value))
        else:
            return Token(INTEGER, int(number_value))

    def string(self):
        string_value = '"'
        prev_char = '"'
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            string_value += self.current_char
            prev_char = self.current_char
            self.advance()
        # if self.current_char == '"' and prev_char != "\\":
        string_value += self.current_char
        self.advance()

        return Token(STRING, string_value)

    def variable(self):
        result = '$'
        self.advance()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token(ID, result)

    def function(self):
        result = '@'
        self.advance()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token(ID, result)

    def _id(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result == 'int':
            return Token(TYPE, result)
        elif result == 'string':
            return Token(TYPE, result)
        elif result == 'float':
            return Token(TYPE, result)
        elif result == 'boolean':
            return Token(TYPE, result)
        elif result == 'array':
            return Token(TYPE, result)
        elif result == 'do':
            return Token(TYPE, result)
        elif result == 'use':
            return Token(USE, result)
        elif result == 'dec':
            return Token(DEC, result)
        elif result == 'decfun':
            return Token(DECFUN, result)
        elif result == 'cond':
            return Token(COND, result)
        elif result == 'loond':
            return Token(LOOND, result)
        elif result == 'return':
            return Token(RETURN, result)
        else:
            return Token(ID, result)

    def skip_whitespace(self):

        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.new_line()
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

            if self.current_char is None:
                return Token(EOF, None)

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '$':
                return self.variable()

            if self.current_char == '@':
                return self.function()

            if self.current_char == '"':
                return self.string()

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACKET, '}')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '#':
                self.advance()
                return Token(HASH, '#')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                if self.current_char == '/':
                    self.advance()
                    return Token(DIV, '//')

                return Token(REAL_DIV, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LESS_EQ, '<=')
                return Token(LESS, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREATER_EQ, '>=')
                return Token(GREATER, '>')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUAL, '==')
                return Token(ASSIGN, '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NOT_EQUAL, '!=')
                return Token(NOT, '!')

            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token(AND, '&&')

            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token(AND, '||')

            self.error()

        return Token(EOF, None)
