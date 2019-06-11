from interpreter.syntax_analysis.interpreter import Args, VarDecl, Type, Var, FunDecl, Stmts

str_equals = """
def str_equals(s1, s2):
    return int(s1 == s2)

"""

cast_to = """
def cast_to(var, type):
    if type == 'int':
        return int(var)
    elif type == 'string':
        return str(var)
    return None
"""

random = """
import random as random_b
def random(arg_from, arg_to):
    return random_b.randrange(arg_from, arg_to)
"""

array_init = """
def array_init():
    return []
"""

sqrt = """
import math
def sqrt(value):
    return math.sqrt(value)
"""

is_integer = """
def is_integer(value):
    if float.is_integer(value):
        return 1
    return 0
"""

array_append = """
def array_append(array, value):
    array.append(value)
"""

array_size = """
def array_size(array):
    return len(array)
"""

array_get = """
def array_get(array, index):
    return array[index]
"""

str_char_at = """
def str_char_at(value, index):
    return value[index]
"""

str_length = """
def str_length(value):
    return len(value)
"""

str_is_alpha = """
def str_is_alpha(value):
    return value.isalpha()
"""

str_is_digit = """
def str_is_digit(value):
    return value.isdigit()
"""

str_to_upper = """
def str_to_upper(value):
    return value.upper()
"""

file_read = """
def file_read(file_path):
    file = open(file_path)
    content = file.read()
    file.close()
    return content
"""

str_split = """
def str_split(content, delimiter):
    return content.split(delimiter)
"""

built_in_impl_map = {
    'str_equals': str_equals,
    'cast_to': cast_to,
    'random': random,
    'array_init': array_init,
    'sqrt': sqrt,
    'is_integer': is_integer,
    'array_append': array_append,
    'array_size': array_size,
    'array_get': array_get,
    'str_char_at': str_char_at,
    'str_length': str_length,
    'str_is_alpha': str_is_alpha,
    'str_is_digit': str_is_digit,
    'str_to_upper': str_to_upper,
    'file_read': file_read,
    'str_split': str_split
}
str_equals_parameters = Args([VarDecl(Type('string'), Var('s1')), VarDecl(Type('string'), Var('s2'))])
str_equals_return_type = Type('int')
str_equals_dec = FunDecl(type_node=str_equals_return_type, fun_name='str_equals', args_node=str_equals_parameters, stmts_node=Stmts([]))

cast_to_parameters = Args([VarDecl(Type('any'), Var('var')), VarDecl(Type('string'), Var('type'))])
cast_to_return_type = Type('any')
cast_to_dec = FunDecl(type_node=cast_to_return_type, fun_name='cast_to', args_node=cast_to_parameters, stmts_node=Stmts([]))

sqrt_parameters = Args([VarDecl(Type('int'), Var('value'))])
sqrt_return_type = Type('float')
sqrt_dec = FunDecl(type_node=sqrt_return_type, fun_name='sqrt', args_node=sqrt_parameters, stmts_node=Stmts([]))

built_in_metadata_map = {
    'sqrt': sqrt_dec,
    'str_equals': str_equals_dec,
    'cast_to': cast_to_dec
}