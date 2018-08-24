'''
from itertools import chain
import re

def sequence(*funcs):
    if len(funcs) == 0:
        def result(src):
            yield (), src
        return result
    def result(src):
        for arg1, src in funcs[0](src):
            for others, src in sequence(*funcs[1:])(src):
                yield (arg1,) + others, src
    return result

number_regex = re.compile(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)

def parse_number(src):
    match = number_regex.match(src)
    if match is not None:
        number, src = match.groups()
        yield eval(number), src

string_regex = re.compile(r"('(?:[^\\']|\\['\\/bfnrt]|\\u[0-9a-fA-F]{4})*?')\s*(.*)", re.DOTALL)

def parse_string(src):
    match = string_regex.match(src)
    if match is not None:
        string, src = match.groups()
        yield eval(string), src

def parse_word(word, value=None):
    l = len(word)
    def result(src):
        if src.startswith(word):
            yield value, src[l:].lstrip()
    result.__name__ = "parse_%s" % word
    return result

parse_true = parse_word("true", True)
parse_false = parse_word("false", False)
parse_null = parse_word("null", None)

def parse_value(src):
    for match in chain(
        parse_string(src),
        parse_number(src),
        parse_array(src),
        parse_object(src),
        parse_true(src),
        parse_false(src),
        parse_null(src),
    ):
        yield match
        return

parse_left_square_bracket = parse_word("[")
parse_right_square_bracket = parse_word("]")
parse_empty_array = sequence(parse_left_square_bracket, parse_right_square_bracket)

def parse_array(src):
    for _, src in parse_empty_array(src):
        yield [], src
        return

    for (_, items, _), src in sequence(
        parse_left_square_bracket,
        parse_comma_separated_values,
        parse_right_square_bracket,
    )(src):
        yield items, src

parse_comma = parse_word(",")

def parse_comma_separated_values(src):
    for (value, _, values), src in sequence(
        parse_value,
        parse_comma,
        parse_comma_separated_values
    )(src):
        yield [value] + values, src
        return

    for value, src in parse_value(src):
        yield [value], src

parse_left_curly_bracket = parse_word("{")
parse_right_curly_bracket = parse_word("}")
parse_empty_object = sequence(parse_left_curly_bracket, parse_right_curly_bracket)

def parse_object(src):
    for _, src in parse_empty_object(src):
        yield {}, src
        return
    for (_, items, _), src in sequence(
        parse_left_curly_bracket,
        parse_comma_separated_keyvalues,
        parse_right_curly_bracket,
    )(src):
        yield items, src

parse_colon = parse_word(":")

def parse_keyvalue(src):
    for (key, _, value), src in sequence(
        parse_string,
        parse_colon,
        parse_value
    )(src):
        yield {key: value}, src

def parse_comma_separated_keyvalues(src):
    for (keyvalue, _, keyvalues), src in sequence(
        parse_keyvalue,
        parse_comma,
        parse_comma_separated_keyvalues,
    )(src):
        keyvalue.update(keyvalues)
        yield keyvalue, src
        return

    for keyvalue, src in parse_keyvalue(src):
        yield keyvalue, src

def parse(s):
    s = s.strip()
    match = list(parse_value(s))
    if len(match) != 1:
        raise ValueError("not a valid JSON string")
    result, src = match[0]
    if src.strip():
        raise ValueError("not a valid JSON string")
    return result
'''

from pyparsing import *
import string
#print (parse("{'a' : ['arr', 5]}"))

def parse_class(str):
    class_name = (Word(alphanums + '_'))('class_name')
    prop = Word(alphanums + ' _\t;=')('prop')
    def_prop = Suppress('{') + prop + Suppress('}')
    def_class = Suppress('{' + 'properties') + def_prop + Suppress('}')
    parse_module =  Suppress('class') + class_name + def_class
    res = parse_module.parseString(str)
    return res;

def index_second_close_bracket(str):
    index_first = str.find('}')
    return str[index_first+1:].find('}') + index_first + 1

def parse_class_prop(str):
    type_var = Word(alphanums + '_')
    name_var = Word(alphanums + '_')
    value_var = Optional(Suppress('=') + Word(alphanums + '_'))
    parse_var = type_var + name_var + value_var
    #print(res.prop.split(';'))
    for s in str.split(';')[:-1]:
        res1 = parse_var.parseString(s)
        print(res1)

def parse_init(str):
    type_var = Word(alphanums + '_')
    name_var = Word(alphanums + '_')
    value_var = Optional('=' + Word(alphanums + '_'))
    parse_count = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    parse_prop = Word(alphanums + '_')
    parse_def_var = type_var + name_var + parse_count
    parse_init_var = name_var + parse_count + Suppress('.') + parse_prop + value_var
    for s in str.split(';')[:-1]:
        if s.find('=') != -1:
            res1 = parse_init_var.parseString(s)
        else:
            res1 = parse_def_var.parseString(s)
        print(res1)


def parse_goal(str):
    name_var = Word(alphanums + '_')
    num_var = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    value_var = Optional('=' + Word(alphanums + '_') + num_var)
    parse_prop = Word(alphanums + '_')
    parse_init_var = name_var + num_var + Suppress('.') + parse_prop + value_var
    for s in str.split(';')[:-1]:
        res1 = parse_init_var.parseString(s)
        print(res1)


def parse_action_param(str):
    type_var = Word(alphanums + '_')
    name_var = Word(alphanums + '_')
    num_var = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    parse_param = type_var + name_var + num_var
    for s in str.split(',')[:-1]:
        res1 = parse_init_var.parseString(s)
        print(res1)

def parse_action_prec(str):
    pass

def parse_action_res(str):
    pass

def parse_action(str):
    pass


f=open('assembly.rps','r')
s = f.read().replace('\n','').replace('\t','')
index_start = s.find('class')

while(index_start != -1):
    res = parse_class(s)
    print(res)
    parse_class_prop(res.prop)
    next_index = index_second_close_bracket(s)
    s = s[next_index + 1:].strip()
    
    index_start = s.find('class')

print(s)

index_start = s.find('initialization') + len('initialization')
index_start = index_start + s[index_start:].find('{') + 1
next_index = index_start + s[index_start:].find('}')
print(index_start,next_index)
print(s[index_start:next_index])
parse_init(s[index_start:next_index])

index_start = s.find('goal') + len('goal')
index_start = index_start + s[index_start:].find('{') + 1
print(s[index_start:-1])
next_index = index_start + s[index_start:].find('}')
print(index_start,next_index)
print(s[index_start:next_index])
parse_goal(s[index_start:next_index])

