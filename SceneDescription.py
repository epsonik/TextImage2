import statistics
from math import sqrt

import numpy
import pandas as pd

from DrawField import draw_field
from InputData import input_data
from Obj import ObjData


# generate description
def scene_description(create_bound_boxes, create_prop, create_rels, create_rules, get_field_size):
    # generowanie opisu sceny
    # create relative positions of obiektów
    obj_data = get_relpos(create_bound_boxes, get_field_size)
    pred = get_predicates(obj_data, create_prop, create_rels)
    # create predicated based on rules
    rule_pred = add_rule_predicates(obj_data, pred, create_rules)
    # select correct predicated
    pred_sel = select_predicates(obj_data, pred + rule_pred, 1, 3)
    # generate description from selected predicated
    description = get_description(create_bound_boxes, pred_sel, create_prop, create_rels, create_rules)
    return description


# create relative position of objects
def get_relpos(obj, field_size):
    number_of_b_boxes = len(obj)
    left = []
    right = []
    horiz_len = []
    up = []
    down = []
    vert_len = []
    size = []
    for i in range(number_of_b_boxes):
        # check if object left position trend is 1 not -1
        left.append(2 * obj[i].pos[1] / field_size[1] - 1)
        right.append(2 * (obj[i].pos[1] + obj[i].length[1]) / field_size[1] - 1)
        horiz_len.append(obj[i].length[1] / field_size[1])
        up.append(2 * obj[i].pos[0] / field_size[0] - 1)
        down.append(2 * (obj[i].pos[0] + obj[i].length[0]) / field_size[1] - 1)
        vert_len.append(obj[i].length[0] / field_size[0])
        size.append(horiz_len[i] * vert_len[i])
    obj_data = ObjData(number_of_b_boxes, left, right, horiz_len, up, down, vert_len, size)

    return obj_data


# return argument of memebership function
# ob_data - matrix of bounding boxes data
# pr - seetings or relation of
#
def get_mfarg(ob_data, pr, ob_num1, ob_num2):
    out = [0]
    # left borde of bound_box
    if (pr.farg == 'b_l'):
        out = ob_data.left
    # right border of bound_box
    elif (pr.farg == 'b_r'):
        out = ob_data.right
    #     centroid of left-right bound_box
    elif (pr.farg == 'c_lr'):
        out = (numpy.array(ob_data.left) + numpy.array(ob_data.right)) / 2
    # top border of bound_box
    elif (pr.farg == 'b_t'):
        out = ob_data.up
    # bottom border of bound_box
    elif (pr.farg == 'b_b'):
        out = ob_data.down
    elif (pr.farg == 'f_w'):
        out = ob_data.horiz_len
    elif (pr.farg == 'f_h'):
        out = ob_data.vert_len
    # centroid top-bottom
    elif (pr.farg == 'c_ud'):
        out = (numpy.array(ob_data.up) + numpy.array(ob_data.down)) / 2
    # distance betwen centroids left-right
    elif (pr.farg == 'd_lr'):
        out = [(ob_data.right[ob_num1] + ob_data.left[ob_num1]) / 2 - (
                ob_data.right[ob_num2] + ob_data.left[ob_num2]) / 2]
    # distance between centroids top-bottom
    elif (pr.farg == 'd_tb'):
        out = [(ob_data.up[ob_num1] + ob_data.down[ob_num1]) / 2 - (ob_data.up[ob_num2] + ob_data.down[ob_num2]) / 2]
    # Euclidean distance between centroids
    elif (pr.farg == 'd'):
        dist_ud = (ob_data.up[ob_num1] + ob_data.down[ob_num1]) / 2 - (ob_data.up[ob_num2] + ob_data.down[ob_num2]) / 2
        dist_lr = (ob_data.right[ob_num1] + ob_data.left[ob_num1]) / 2 - (
                ob_data.right[ob_num2] + ob_data.left[ob_num2]) / 2
        out = [sqrt(dist_ud * dist_ud + dist_lr * dist_lr)]
    return out


# trapezoid membership function
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


# generate values of fuzzy descriptors position per  properties
# vector of values per which we are counting values of descriptior values
def get_properties(ob_data, prop):
    obj_prop = []
    max = 1
    # property number
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
    # generate predicated per properties and relations
    # saliency of objects that is proportional to size of object
    sal = obj_data.size
    # count values of prperties confidence factor
    obj_prop = get_properties(obj_data, prop)
    # count values of realations confidence factor
    obj_rel = get_relations(obj_data, rel)
    # generate predicates
    counterA = 0
    counterB = 0
    pred = []
    # iterate over object reference number
    for box_idx_main in range(obj_data.number_of_b_boxes):
        # properties
        for prop_idx in range(len(prop)):
            # values of membership fuction
            if obj_prop[prop_idx][box_idx_main] > 0:
                temp = []
                # predicate id from property
                temp.append(prop[prop_idx].id)
                # confidence factor
                temp.append(obj_prop[prop_idx][box_idx_main] * sal[box_idx_main] * prop[prop_idx].psal)
                # usage pointer
                temp.append(0)
                # number of referencje object
                temp.append(box_idx_main)
                # not use with properties
                temp.append(-1)
                # property number
                temp.append(prop_idx)
                # used in rules
                temp.append(obj_prop[prop_idx][box_idx_main])
                pred.append(temp)
                counterA += 1
        # realtions
        # iterate over objects, which  i objects is in relation
        for box_idx in range(obj_data.number_of_b_boxes):
            # iterate over relation number
            for rel_idx in range(len(rel)):
                if obj_rel[rel_idx, box_idx_main, box_idx] > 0:
                    temp = []
                    # predicate id from relation
                    temp.append(rel[rel_idx].id)
                    # confidence factor
                    temp.append(obj_rel[rel_idx, box_idx_main, box_idx] * sal[box_idx_main] * rel[rel_idx].psal)
                    # usage pointer
                    temp.append(0)
                    # number of referencje object
                    temp.append(box_idx_main)
                    # number of second object from relation
                    temp.append(box_idx)
                    # relation number
                    temp.append(rel_idx)
                    # used in rules
                    temp.append(obj_rel[rel_idx, box_idx_main, box_idx])
                    pred.append(temp)
                    counterB = counterB + 1

    return pred


# generate values od fuzzy descriptors position per relations
def get_relations(ob_data, rel):
    import numpy
    obj_rel = numpy.ones((len(rel), ob_data.number_of_b_boxes, ob_data.number_of_b_boxes))

    for k in range(len(rel)):
        for i in range(ob_data.number_of_b_boxes):
            for j in range(ob_data.number_of_b_boxes):
                temp = tmf(get_mfarg(ob_data, rel[k], i, j), rel[k].ftype, rel[k].fthr)
                obj_rel[k, i, j] = temp[0]
    return obj_rel


#  add predicates  from rules - inference
def add_rule_predicates(obj_data, pred, rule):
    # saliency of objects proportional to relative length
    sal = obj_data.size
    counter = 0
    rule_pred = []
    # iterate over rules
    for i in range(len(rule)):
        # iterate over predicates
        for j in range(len(pred)):
            # found predicate with first premise
            if (pred[j][0] == rule[i].id_first):
                # save object number
                obj_found = pred[j][3]
                # iterate over predicates - look for second premise
                for k in range(len(pred)):
                    if ((pred[k][0] == rule[i].id_second) and (pred[k][3] == obj_found)):
                        # second second premise for the same object
                        if ((pred[j][6] != 0) and (pred[k][6] != 0)):
                            # if is not equal to 0, calculates new predicate
                            ruleobj_cf = combine_mf(pred[j][6], pred[k][6], rule[i].operator)
                            temp = []
                            # predicate id from rules
                            temp.append(rule[i].id)
                            # confidence factor
                            temp.append(ruleobj_cf * sal[obj_found] * rule[i].psal)
                            # usage pointer
                            temp.append(0)
                            # object number
                            temp.append(obj_found)
                            # lack of second object(rule)
                            temp.append(-2)
                            # rule number
                            temp.append(i)
                            #
                            temp.append(ruleobj_cf)
                            rule_pred.append(temp)
                            counter = counter + 1
    return rule_pred


# cobination of two values of membership function(used in rules)
def combine_mf(val1, val2, type):
    out = 0
    if type == 'min':
        out = min(val1, val2)
    elif type == 'max':
        out = max(val1, val2)
    elif type == 'mean':
        out = statistics.mean([val1, val2])
    return out


# select most important predicates
# num_times - how often object is mentioned in the text
def select_predicates(obj_data, pred, num_times_coordinate_x, num_times_coordinate_y):
    # sort by certainty factor of predicate
    def myFunc(e):
        return e[1]

    pred.sort(key=myFunc, reverse=True)
    # select most improtant predicates
    used = numpy.zeros((obj_data.number_of_b_boxes))
    for pred_idx in range(len(pred)):
        # properties or rules
        if pred[pred_idx][4] < 0:
            if used[pred[pred_idx][3]] < num_times_coordinate_y:
                used[pred[pred_idx][3]] = used[pred[pred_idx][3]] + 1
                pred[pred_idx][2] = 1
        # pred(i,5) > 0 -> relation
        else:
            # second object in relation should used previously
            if (used[pred[pred_idx][3]] < num_times_coordinate_y) & (used[pred[pred_idx][3]] == 1):
                used[pred[pred_idx][3]] = used[pred[pred_idx][3]] + 1
                pred[pred_idx][2] = 1
    A = pd.DataFrame(numpy.array(pred))

    # reduce predicate matrix to the most important ones
    def most_important_predicates_filter():
        t = A[1].apply(lambda x: True if x > 0 else False)
        c = A[2].apply(lambda x: True if x == 1 else False)
        filter = numpy.logical_and(t, c)
        return filter

    pred_out = A[most_important_predicates_filter()]
    return pred_out.to_numpy()


# generate decription from the matrix with most important predicates
def get_description(obj, pred, prop, rel, rule):
    desc = []
    for i in range(len(pred)):
        # property
        if (pred[i][4] == -1):
            zdanie = prop[pred[i][5]].text[0] + obj[int(pred[i][3])].name + prop[pred[i][5]].text[1]
            desc.append(zdanie)
        elif (pred[i][4] == -2):
            zdanie = rule[pred[i][5]].text[0] + obj[int(pred[i][3])].name + rule[pred[i][5]].text[1]
            desc.append(zdanie)
        # relation
        else:
            zdanie = rel[pred[i][5]].text[0] + obj[int(pred[i][3])].name + rel[pred[i][5]].text[1] + obj[
                pred(i, 5)].name, \
                     rel[pred[i][5]].text[2]
            desc.append(zdanie)
    return desc


# plot image
def show_image(imf):
    import matplotlib.pyplot as plt
    plt.imshow(imf[2])
    plt.show()


def create_output_image_and_desc():
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(create_bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    imf = draw_field(create_bound_boxes, get_field_size, -1, 1)
    show_image(imf)
