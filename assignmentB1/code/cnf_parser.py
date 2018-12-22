from statements_axioms_variables import *


def get_predicates(line):
    return line.replace(' ', '').split('V')


def get_predicat_and_vars(name):
    is_not = False
    if '!' in name:
        is_not = True
        name = name.replace('!', '')
    res = name.replace(')', '').split('(')
    return is_not, res[0], res[1].split(',')


def create_variable(var=''):
    if var.isdigit():
        v = Variable(symbolic=var, var=int(var))
    elif var[0].islower():
        v = Variable(symbolic=var)
    else:
        v = Variable(symbolic=var, var=var)
    return v


def is_var_in_list(var, list_of_vars):
    for v in list_of_vars:
        if v.symbol == var:
            return True
    return False


def get_var_idx_in_list(var, list_of_vars):
    for i, v in enumerate(list_of_vars):
        if v.symbol == var:
            return i


def create_predicat_from_string(predicat, list_of_vars):
    is_not, pred_name, variables = get_predicat_and_vars(predicat)
    idx_list_for_predicat = []
    for v in variables:
        if not is_var_in_list(v, list_of_vars):
            list_of_vars.append(create_variable(v))
        idx = get_var_idx_in_list(v, list_of_vars)
        idx_list_for_predicat.append(idx)
    return Predicat(pred_name, [list_of_vars[i] for i in idx_list_for_predicat], is_not)


def create_axiom_from_line(line):
    try:
        list_of_predicats = []
        list_of_vars = []
        for predicat in get_predicates(line.replace('\n', '')):
            if predicat == '': continue
            list_of_predicats.append(create_predicat_from_string(predicat, list_of_vars))
        return Axiom(list_of_predicats)
    except:
        raise Exception('Problem with line: "{}"'.format(line.replace('\n', "")))

def parser(file_name):
    list_of_axioms = []
    with open(file_name) as f:
        for line in f:
            list_of_axioms.append(create_axiom_from_line(line))
    return list_of_axioms



if __name__ == '__main__':
    axioms = parser("hurricane_cnf.txt")
    for a in axioms:
        print str(a)