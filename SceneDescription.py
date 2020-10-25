import statistics
from math import sqrt

import numpy
import pandas as pd

from DrawField import draw_field
from Obj import Obj, ObjData
from Prop import Prop
from Rule import Rule


def create_bound_boxes():
    objects = {}
    objects[0] = Obj('A', [5, 15], [15, 30])
    objects[1] = Obj('B', [45, 150], [25, 90])
    objects[2] = Obj('C', [200, 115], [55, 80])
    return objects


def create_prop():
    props = {}
    props[0] = Prop('left edge', 1, 0.9, 'b_l', 'trapezoid', [-2, -2, -1, -0.85],
                    ["Przy lewej krawędzi znajduje się ", ". "])
    props[1] = Prop('left side', 2, 0.8, 'b_l', 'trapezoid', [-10, -0.9, -0.6, 0],
                    ["W lewej części pola widzimy ", ". "])
    props[2] = Prop('center left-right', 3, 0.9, 'c_lr', 'trapezoid', [-0.2, -0.05, 0.05, 0.2],
                    ["Na środku szerokości znajduje się ", ". "])
    props[3] = Prop('right side', 4, 0.8, 'b_r', 'trapezoid', [0, 0.6, 0.9, 10],
                    ["W prawej części pola widzimy ", ". "])
    props[4] = Prop('right edge', 5, 0.9, 'b_r', 'trapezoid', [0.85, 1, 2, 2],
                    ["Przy prawej krawędzi znajduje się ", ". "])
    props[5] = Prop('top edge', 6, 0.7, 'b_t', 'trapezoid', [-2, -2, -1, -0.85],
                    ["Przy górnej krawędzi znajduje się ", ". "])
    props[6] = Prop('upper part', 7, 0.5, 'b_t', 'trapezoid', [-10, -0.9, -0.6, 0],
                    ["W górnej części pola widzimy ", ". "])
    props[7] = Prop('center up-down', 8, 0.8, 'c_tb', 'trapezoid', [-0.2, -0.05, 0.05, 0.2],
                    ["Na środku wysokości znajduje się ", ". "])
    props[8] = Prop('lower part', 9, 0.5, 'b_b', 'trapezoid', [0, 0.6, 0.9, 10],
                    ["W dolnej części pola widzimy ", ". "])
    props[9] = Prop('bottom edge', 10, 0.7, 'b_b', 'trapezoid', [0.85, 1, 2, 2],
                    ["Przy dolnej krawędzi znajduje się ", ". "])
    return props


def create_rels():
    rels = {}

    rels[0] = Prop('on the right', 21, 0.8, 'd_lr', 'trapezoid', [0, 0.01, 0.5, 2],
                   ["Obiekt ", " znajduje się po prawej stronie obiektu ", ". "])
    rels[1] = Prop('on the left', 22, 0.8, 'd_lr', 'trapezoid', [-2, -0.5, -0.01, 0],
                   ["Obiekt ", " znajduje się po lewej stronie obiektu ", ". "])

    rels[2] = Prop('above', 23, 0.8, 'd_tb', 'trapezoid', [-2, -0.5, -0.01, 0],
                   ["Obiekt ", " znajduje się powyżej obiektu ", ". "])

    rels[3] = Prop('below', 24, 0.8, 'd_tb', 'trapezoid', [0, 0.01, 0.5, 2],
                   ["Obiekt ", " znajduje się poniżej obiektu ", ". "])

    return rels


def create_rules():
    rules = {}
    rules[0] = Rule('center', 41, 1, 3, 8, 'min', ["Obiekt ", " znajduje się na środku pola", ". "])
    rules[1] = Rule('top left corner', 42, 1, 1, 6, 'min',
                    ["Obiekt ", " znajduje się w lewym-górnym narożniku pola", ". "])
    rules[2] = Rule('top right corner', 43, 1, 5, 6, 'min',
                    ["Obiekt ", " znajduje się w prawym-górnym narożniku pola", ". "])
    rules[3] = Rule('bottom right corner', 44, 1, 5, 10, 'min', ["Obiekt ", " w prawym-dolnym narożniku pola", ". "])
    rules[4] = Rule('bottom left corner', 45, 1, 1, 10, 'min',
                    ["Obiekt ", " znajduje się w lewym-dolnym narożniku pola", ". "])
    rules[5] = Rule('top left part', 46, 1, 2, 7, 'min', ["Obiekt ", " znajduje się w lewej-górnej części pola", ". "])
    rules[6] = Rule('top right part', 47, 1, 4, 7, 'min',
                    ["Obiekt ", " znajduje się w prawej-górnej części pola", ". "])
    rules[7] = Rule('bottom right part', 48, 1, 4, 9, 'min',
                    ["Obiekt ", " znajduje się w prawej-dolnej części pola", ". "])
    rules[8] = Rule('bottom left part', 49, 1, 2, 9, 'min',
                    ["Obiekt ", " znajduje się w lewej-dolnej części pola", ". "])
    return rules


def get_field_size():
    return [400, 400]


def scene_description(obj, field_size):
    # generowanie opisu sceny
    # wyznaczamy względne współrzędne obiektów
    obj_data = get_relpos(obj, field_size)
    pred = get_predicates(obj_data, create_prop(), create_rels())
    rule_pred = add_rule_predicates(obj_data, pred, create_rules())
    pred_sel = select_predicates(obj_data, pred + rule_pred, 1)
    description = get_description(obj, pred_sel, create_prop(), create_rels(), create_rules())
    return description


def get_relpos(obj, field_size):
    num = len(obj)
    left = []
    right = []
    horiz_len = []
    up = []
    down = []
    vert_len = []
    size = []
    for i in range(num):
        left.append(2 * obj[i].pos[1] / field_size[1] - 1)
        right.append(2 * (obj[i].pos[1] + obj[i].length[1]) / field_size[1] - 1)
        horiz_len.append(obj[i].length[1] / field_size[1])
        up.append(2 * obj[i].pos[0] / field_size[0] - 1)
        down.append(2 * (obj[i].pos[0] + obj[i].length[0]) / field_size[1] - 1)
        vert_len.append(obj[i].length[0] / field_size[0])
        size.append(horiz_len[i] * vert_len[i])
    obj_data = ObjData(num, left, right, horiz_len, up, down, vert_len, size)

    return obj_data


def get_mfarg(ob_data, pr, ob_num1, ob_num2):
    out = [0]
    if (pr.farg == 'b_l'):
        out = ob_data.left
    elif (pr.farg == 'b_r'):
        out = ob_data.right
    elif (pr.farg == 'c_lr'):
        out = (numpy.array(ob_data.left) + numpy.array(ob_data.right)) / 2
    elif (pr.farg == 'b_t'):
        out = ob_data.up
    elif (pr.farg == 'b_b'):
        out = ob_data.down
    elif (pr.farg == 'c_ud'):
        out = (numpy.array(ob_data.up) + numpy.array(ob_data.down)) / 2
    elif (pr.farg == 'd_lr'):
        out = [(ob_data.right[ob_num1] + ob_data.left[ob_num1]) / 2 - (
                ob_data.right[ob_num2] + ob_data.left[ob_num2]) / 2]
    elif (pr.farg == 'd_tb'):
        out = [(ob_data.up[ob_num1] + ob_data.down[ob_num1]) / 2 - (ob_data.up[ob_num2] + ob_data.down[ob_num2]) / 2]
    elif (pr.farg == 'd'):
        dist_ud = (ob_data.up[ob_num1] + ob_data.down[ob_num1]) / 2 - (ob_data.up[ob_num2] + ob_data.down[ob_num2]) / 2
        dist_lr = (ob_data.right[ob_num1] + ob_data.left[ob_num1]) / 2 - (
                ob_data.right[ob_num2] + ob_data.left[ob_num2]) / 2
        out = [sqrt(dist_ud * dist_ud + dist_lr * dist_lr)]
    return out


def tmf(in_arg, ftype, fval):
    import copy
    out = copy.copy(in_arg)
    if ftype == 'trapezoid':
        for i in range(len(in_arg)):
            if (in_arg[i] < fval[0]):
                out[i] = 0
            elif (in_arg[i] < fval[1]):
                out[i] = (in_arg[i] - fval[0]) / (fval[1] - fval[0])
            elif (in_arg[i] < fval[2]):
                out[i] = 1
            elif (in_arg[i] < fval[3]):
                out[i] = (fval[3] - in_arg[i]) / (fval[3] - fval[2])
            else:
                out[i] = 0
    else:
        print('wrong membership function type')
    return out


def get_properties(ob_data, prop):
    obj_prop = []
    max = 1
    for i in range(len(prop)):
        a = tmf(get_mfarg(ob_data, prop[i], 0, 0), prop[i].ftype, prop[i].fthr)
        if len(a) > max:
            max = len(a)
        if len(a) < max:
            obj_prop.append(a * max)
        else:
            obj_prop.append(a)
    return obj_prop


def get_predicates(obj_data, prop, rel):
    sal = obj_data.size
    obj_prop = get_properties(obj_data, prop)
    obj_rel = get_relations(obj_data, rel)
    counter = 0
    pred = []
    for i in range(obj_data.num):
        for j in range(len(prop)):
            if obj_prop[j][i] > 0:
                temp = []
                temp.append(prop[j].id)
                temp.append(obj_prop[j][i] * sal[i] * prop[j].psal)
                temp.append(0)
                temp.append(i)
                temp.append(-1)
                temp.append(j)
                temp.append(obj_prop[j][i])
                pred.append(temp)
                counter += 1
        for k in range(obj_data.num):
            for j in range(len(rel)):
                if obj_rel[j, i, k] > 0:
                    temp = []
                    temp.append(rel[j].id)
                    temp.append(obj_rel[j, i, k] * sal[i] * rel[j].psal)
                    temp.append(0)
                    temp.append(i)
                    temp.append(k)
                    temp.append(j)
                    temp.append(obj_rel[j, i, k])
                    pred.append(temp)
                    counter = counter + 1

    return pred


def get_relations(ob_data, rel):
    import numpy
    obj_rel = numpy.ones((len(rel), ob_data.num, ob_data.num))

    for k in range(len(rel)):
        for i in range(ob_data.num):
            for j in range(ob_data.num):
                temp = tmf(get_mfarg(ob_data, rel[k], i, j), rel[k].ftype, rel[k].fthr)
                obj_rel[k, i, j] = temp[0]
    return obj_rel


def add_rule_predicates(obj_data, pred, rule):
    sal = obj_data.size
    counter = 0
    rule_pred = []
    for i in range(len(rule)):
        for j in range(len(pred)):
            if (pred[j][0] == rule[i].id_first):
                obj_found = pred[j][3]
                for k in range(len(pred)):
                    if ((pred[k][0] == rule[i].id_second) and (pred[k][3] == obj_found)):
                        if ((pred[j][6] != 0) and (pred[k][6] != 0)):
                            ruleobj_cf = combine_mf(pred[j][6], pred[k][6], rule[i].operator)
                            temp = []
                            temp.append(rule[i].id)
                            temp.append(ruleobj_cf * sal[obj_found] * rule[i].psal)
                            temp.append(0)
                            temp.append(obj_found)
                            temp.append(-2)
                            temp.append(i)
                            temp.append(ruleobj_cf)
                            rule_pred.append(temp)
                            counter = counter + 1
    return rule_pred


def combine_mf(val1, val2, type):
    out = 0
    if type == 'min':
        out = min(val1, val2)
    elif type == 'max':
        out = max(val1, val2)
    elif type == 'mean':
        out = statistics.mean([val1, val2])
    return out


def select_predicates(obj_data, pred, num_times):
    def myFunc(e):
        return e[1]

    pred.sort(key=myFunc, reverse=True)
    pred_out = []
    used = numpy.zeros((obj_data.num))
    for i in range(len(pred)):
        if pred[i][4] < 0:
            if used[pred[i][3]] < num_times:
                used[pred[i][3]] = used[pred[i][3]] + 1
                pred[i][2] = 1
        else:
            if (used[pred[i][3]] < num_times) & (used[pred[i][3]] == 1):
                used[pred[i][3]] = used[pred[i][3]] + 1
                pred[i][2] = 1
    A = pd.DataFrame(numpy.array(pred))
    t = A[1].apply(lambda x: True if x > 0 else False)
    c = A[2].apply(lambda x: True if x == 1 else False)

    filter = numpy.logical_and(t, c)
    pred_out = A[filter]
    return pred_out.to_numpy()


def get_description(obj, pred, prop, rel, rule):
    desc = []
    for i in range(len(pred)):
        if (pred[i][4] == -1):
            zdanie = prop[pred[i][5]].text[0] + obj[pred[i][3]].name + prop[pred[i][5]].text[1]
            desc.append(zdanie)
        elif (pred[i][4] == -2):
            zdanie = rule[pred[i][5]].text[0] + obj[pred[i][3]].name + rule[pred[i][5]].text[1]
            desc.append(zdanie)
        else:
            zdanie = rel[pred[i][5]].text[0] + obj[pred[i][3]].name + rel[pred[i][5]].text[1] + obj[pred(i, 5)].name, \
                     rel[pred[i][5]].text[2]
            desc.append(zdanie)
    return desc


def show_image(imf):
    import matplotlib.pyplot as plt
    plt.imshow(imf[2])
    plt.show()


description = scene_description(create_bound_boxes(), get_field_size())
print(description)
imf = draw_field(create_bound_boxes(), get_field_size(), -1, 1)
show_image(imf)
a= imf[0]
b= imf[1]
c= imf[2]
print('test')