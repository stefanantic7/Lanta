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
def array_append(arr, value):
    arr.append(value)
"""

array_size = """
def array_size(arr):
    return len(arr)
"""

array_get = """
def array_get(arr, index):
    return arr[index]
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
    return int(value.isalpha())
"""

str_is_digit = """
def str_is_digit(value):
    return int(value.isdigit())
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

cput = """
def cput(value):
    print(value)
"""

cget = """
def cget(value):
    return input(value)
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
    'str_split': str_split,
    'cput': cput,
    'cget': cget
}

str_equals_parameters = Args([VarDecl(Type('string'), Var('s1')), VarDecl(Type('string'), Var('s2'))])
str_equals_return_type = Type('int')
str_equals_dec = FunDecl(type_node=str_equals_return_type, fun_name='str_equals', args_node=str_equals_parameters, stmts_node=Stmts([]))

cast_to_parameters = Args([VarDecl(Type('any'), Var('var')), VarDecl(Type('string'), Var('type'))])
cast_to_return_type = Type('any')
cast_to_dec = FunDecl(type_node=cast_to_return_type, fun_name='cast_to', args_node=cast_to_parameters, stmts_node=Stmts([]))

random_parameters = Args([VarDecl(Type('int'), Var('arg_from')), VarDecl(Type('int'), Var('arg_to'))])
random_return_type = Type('int')
random_dec = FunDecl(type_node=random_return_type, fun_name='random', args_node=random_parameters, stmts_node=Stmts([]))

sqrt_parameters = Args([VarDecl(Type('int'), Var('value'))])
sqrt_return_type = Type('float')
sqrt_dec = FunDecl(type_node=sqrt_return_type, fun_name='sqrt', args_node=sqrt_parameters, stmts_node=Stmts([]))

array_init_parameters = Args([])
array_init_return_type = Type('array')
array_init_dec = FunDecl(type_node=array_init_return_type, fun_name='array_init', args_node=array_init_parameters, stmts_node=Stmts([]))

is_integer_parameters = Args([VarDecl(Type('float'), Var('value'))])
is_integer_return_type = Type('int')
is_integer_dec = FunDecl(type_node=is_integer_return_type, fun_name='is_integer', args_node=is_integer_parameters, stmts_node=Stmts([]))

array_append_parameters = Args([VarDecl(Type('array'), Var('arr')), VarDecl(Type('any'), Var('value'))])
array_append_return_type = Type('do')
array_append_dec = FunDecl(type_node=array_append_return_type, fun_name='array_append', args_node=array_append_parameters, stmts_node=Stmts([]))

array_size_parameters = Args([VarDecl(Type('array'), Var('arr'))])
array_size_return_type = Type('int')
array_size_dec = FunDecl(type_node=array_size_return_type, fun_name='array_size', args_node=array_size_parameters, stmts_node=Stmts([]))

array_get_parameters = Args([VarDecl(Type('array'), Var('arr')), VarDecl(Type('int'), Var('index'))])
array_get_return_type = Type('any')
array_get_dec = FunDecl(type_node=array_get_return_type, fun_name='array_get', args_node=array_get_parameters, stmts_node=Stmts([]))

str_char_at_parameters = Args([VarDecl(Type('string'), Var('value')), VarDecl(Type('int'), Var('index'))])
str_char_at_return_type = Type('string')
str_char_at_dec = FunDecl(type_node=str_char_at_return_type, fun_name='str_char_at', args_node=str_char_at_parameters, stmts_node=Stmts([]))

str_length_parameters = Args([VarDecl(Type('string'), Var('value'))])
str_length_return_type = Type('int')
str_length_dec = FunDecl(type_node=str_length_return_type, fun_name='str_length', args_node=str_length_parameters, stmts_node=Stmts([]))

str_is_alpha_parameters = Args([VarDecl(Type('string'), Var('value'))])
str_is_alpha_return_type = Type('int')
str_is_alpha_dec = FunDecl(type_node=str_is_alpha_return_type, fun_name='str_is_alpha', args_node=str_is_alpha_parameters, stmts_node=Stmts([]))

str_is_digit_parameters = Args([VarDecl(Type('string'), Var('value'))])
str_is_digit_return_type = Type('int')
str_is_digit_dec = FunDecl(type_node=str_is_digit_return_type, fun_name='str_is_digit', args_node=str_is_digit_parameters, stmts_node=Stmts([]))

str_to_upper_parameters = Args([VarDecl(Type('string'), Var('value'))])
str_to_upper_return_type = Type('string')
str_to_upper_dec = FunDecl(type_node=str_to_upper_return_type, fun_name='str_to_upper', args_node=str_to_upper_parameters, stmts_node=Stmts([]))

file_read_parameters = Args([VarDecl(Type('string'), Var('file_path'))])
file_read_return_type = Type('string')
file_read_dec = FunDecl(type_node=file_read_return_type, fun_name='file_read', args_node=file_read_parameters, stmts_node=Stmts([]))

str_split_parameters = Args([VarDecl(Type('string'), Var('content')), VarDecl(Type('string'), Var('delimiter'))])
str_split_return_type = Type('array')
str_split_dec = FunDecl(type_node=str_split_return_type, fun_name='str_split', args_node=str_split_parameters, stmts_node=Stmts([]))

cput_parameters = Args([VarDecl(Type('string'), Var('value'))])
cput_return_type = Type('do')
cput_dec = FunDecl(type_node=cput_return_type, fun_name='cput', args_node=cput_parameters, stmts_node=Stmts([]))

cget_parameters = Args([VarDecl(Type('string'), Var('value'))])
cget_return_type = Type('string')
cget_dec = FunDecl(type_node=cget_return_type, fun_name='cget', args_node=cget_parameters, stmts_node=Stmts([]))

built_in_metadata_map = {
    'sqrt': sqrt_dec,
    'str_equals': str_equals_dec,
    'cast_to': cast_to_dec,
    'random': random_dec,
    'array_init': array_init_dec,
    'is_integer': is_integer_dec,
    'array_append': array_append_dec,
    'array_size': array_size_dec,
    'array_get': array_get_dec,
    'str_char_at': str_char_at_dec,
    'str_length': str_length_dec,
    'str_is_alpha': str_is_alpha_dec,
    'str_is_digit': str_is_digit_dec,
    'str_to_upper': str_to_upper_dec,
    'file_read': file_read_dec,
    'str_split': str_split_dec,
    'cput': cput_dec,
    'cget': cget_dec
}