from pyparsing import *
#print (parse("{'a' : ['arr', 5]}"))

def parse_class(str):
    class_name = (Word(alphanums + '_'))('class_name')
    prop = Word(alphanums + ' _\t;=')('prop')
    def_prop = Suppress('{') + prop + Suppress('}')
    def_class = Suppress('{' + 'properties') + def_prop + Suppress('}')
    parse_module =  Suppress('class') + class_name + def_class
    res = parse_module.parseString(str)
    return res;

def index_second_close_bracket(str, close_bracket = '}'):
    index_first = str.find(close_bracket)
    return str[index_first+1:].find(close_bracket) + index_first + 1

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
    parse_goal_var = name_var + num_var + Suppress('.') + parse_prop + value_var
    for s in str.split(';')[:-1]:
        res1 = parse_goal_var.parseString(s)
        print(res1)


def parse_action_name_and_param(str):
    name_action = Word(alphanums + '_')('name_action')
    type_var = Word(alphanums + '_')
    name_var = Word(alphanums + '_')
    num_var = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    parse_param = (type_var + name_var + num_var + Optional(','))
    action_head = name_action + Suppress('(') + OneOrMore(parse_param) + Suppress(')')
    res1 = action_head.parseString(str)
    print(res1)

def parse_action(str):
    name_var = Word(alphanums + '_')
    value_var = Optional('=' + Word(alphanums + '_'))
    parse_count = Optional(Suppress('[') + Word(nums) + Suppress(']'))
    parse_prop = Word(alphanums + '_')
    parse_prec_var = name_var + parse_count + Suppress('.') + parse_prop + value_var
    for s in str.split(';')[:-1]:
        res1 = parse_prec_var.parseString(s)
        print(res1)   

def parse_action_prec(str): 
    index_start = str.find('preconditions') + len('preconditions') + 1
    next_index = str[:].strip().find('}')
    parse_action(str[index_start:next_index])

def parse_action_result(str):
    index_start = str.find('result') + len('result') + 1
    next_index = str[:].strip().find('}')
    parse_action(str[index_start:next_index])

f=open('assembly.rps','r')
orig_s = f.read().replace('\n','').replace('\t','')
s = orig_s[:]

index_start = s.find('class')
while(index_start != -1):
    res = parse_class(s)
    print(res)
    parse_class_prop(res.prop)
    next_index = index_second_close_bracket(s,'}')
    s = s[next_index + 1:].strip()
    
    index_start = s.find('class')

index_start = s.find('initialization') + len('initialization')
index_start = index_start + s[index_start:].find('{') + 1
next_index = index_start + s[index_start:].find('}')
print(index_start,next_index)
print(s[index_start:next_index])
parse_init(s[index_start:next_index])

s = s[next_index + 1:].strip()

index_start = s.find('action')
while(index_start != -1):
    index_start = index_start + len('action') + 1
    s = s[index_start:]
    parse_action_name_and_param(s)
    index_start = s.find('{') + 1
    next_index = index_second_close_bracket(s,'}')

    parse_action_prec(s[index_start:next_index])

    parse_action_result(s[index_start:next_index])
    #print(res)
    #parse_class_prop(res.prop)
    index_start = s.find('action')

index_start = s.find('goal') + len('goal')
index_start = index_start + s[index_start:].find('{') + 1
print(s[index_start:-1])
next_index = index_start + s[index_start:].find('}')
print(index_start,next_index)
print(s[index_start:next_index])
parse_goal(s[index_start:next_index])
