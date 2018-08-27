from pyparsing import *

def substring(str,level):
    index_start = str.find(level) + len(level)
    index_start = index_start + str[index_start:].find('{') + 1
    next_index = index_start + str[index_start:].find('}')
    return str[index_start:next_index]

def parse_def_var():
    type_var = Word(alphanums + '_')
    name_var = Word(alphanums + '_')
    num_var = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    value_var = Optional(Suppress('=') + Word(alphanums + '_'))
    def_var = type_var + name_var + num_var + value_var
    return def_var

def parse_init_var():
    name_var = Word(alphanums + '_')
    num_var = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    value_var = Optional(Suppress('=') + Word(alphanums + '_') + num_var)
    parse_prop = Optional(Suppress('.') + Word(alphanums + '_'))
    init_var = name_var + num_var +  parse_prop + value_var
    return init_var

def parse_name_class(str):
    class_name = (Word(alphanums + '_'))('class_name')
    parse_class =  class_name + Suppress('{')
    res = parse_class.parseString(str)
    print(res)
    
def parse_i_g(str, level):
    parse_expression(substring(str,level))

def index_second_close_bracket(str, close_bracket = '}'):
    index_first = str.find(close_bracket)
    return str[index_first+1:].find(close_bracket) + index_first + 1

def parse_class_prop(str):
    st = substring(str,'properties')
    def_var = parse_def_var()
    for s in st.split(';')[:-1]:
        res1 = def_var.parseString(s)
        print(res1)
        
def parse_expression(str):
    def_var = parse_def_var()
    init_var = parse_init_var()
    for s in str.split(';')[:-1]:
        if s.find('=') != -1:
            res1 = init_var.parseString(s)
        else:
            res1 = def_var.parseString(s)
        print(res1)

def parse_action_name_and_param(str):
    name_action = Word(alphanums + '_')('name_action')
    parse_param = (parse_init_var() + Optional(','))
    action_head = name_action + Suppress('(') + OneOrMore(parse_param) + Suppress(')')
    res1 = action_head.parseString(str)
    print(res1)

def parse_action_p_r(str, level):
    index_start = str.find(level) + len(level) + 1
    next_index = str[:].strip().find('}')
    parse_expression(str[index_start:next_index])

def parse_action_prec(str):
    parse_action_p_r(str,'preconditions')

def parse_action_result(str):
    parse_action_p_r(str,'result')

def parse_action(str):
    parse_action_prec(str)
    parse_action_result(str)

def parse_set(str,level, func1, func2):
    index_start = str.find(level)
    while(index_start != -1):
        index_start = index_start + len(level) + 1
        str = str[index_start:]
        func1(str)
        index_start = str.find('{') + 1
        next_index = index_second_close_bracket(str)
        func2(str[index_start:next_index])
        index_start = str.find(level)




f=open('assembly.rps','r')
orig_s = f.read().strip().replace('\n','').replace('\t','')
s = orig_s[:]

print('-----------CLASS---------')
parse_set(s,'class',parse_name_class,parse_class_prop)

print('-----------INIT---------')
s = s[next_index + 1:].strip()
parse_i_g(s, 'initialization')

print('-----------ACTION---------')
parse_set(s,'action',parse_action_name_and_param,parse_action)

print('-----------GOAL---------')
s = s[next_index + 1:].strip()
parse_i_g(s, 'goal')
