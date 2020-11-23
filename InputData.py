#  dane testowe
from Obj import Obj
from Prop import Prop
from Rule import Rule


def input_data():
    # data of objects at the beginning
    return create_bound_boxes(), create_prop(), create_rels(), create_rules(), get_field_size()


def create_bound_boxes():
    objects = {}
    objects[0] = Obj('A', [5, 15], [15, 30])
    objects[1] = Obj('B', [45, 150], [25, 90])
    objects[2] = Obj('C', [200, 115], [55, 80])
    return objects


def create_prop():
    props = {}
    # properties left and right
    props[0] = Prop('left edge', 1, 0.9, 'b_l', 'trapezoid', [-2, -2, -1, -0.85],
    # trapezod coordinates
                    ["Przy lewej krawędzi znajduje się ", ". "])
    props[1] = Prop('left side', 2, 0.8, 'b_l', 'trapezoid', [-10, -0.9, -0.6, 0],
                    ["W lewej części pola widzimy ", ". "])
    props[2] = Prop('center left-right', 3, 0.9, 'c_lr', 'trapezoid', [-0.2, -0.05, 0.05, 0.2],
                    ["Na środku szerokości znajduje się ", ". "])
    props[3] = Prop('right side', 4, 1, 'b_r', 'trapezoid', [0, 0.6, 0.9, 10],
                    ["W prawej części pola widzimy ", ". "])
    props[4] = Prop('right edge', 5, 0.9, 'b_r', 'trapezoid', [0.85, 1, 2, 2],
                    ["Przy prawej krawędzi znajduje się ", ". "])
    # propertes down and upper
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


# define relations
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


# define rules
def create_rules():
    rules = {}
    rules[0] = Rule('center', 41, 1, 3, 8, 'min', ["Obiekt ", " znajduje się na środku pola", ". "])
    rules[1] = Rule('top left corner', 42, 1, 1, 6, 'min',
                    ["Obiekt ", " znajduje się w lewym-górnym narożniku pola", ". "])
    rules[2] = Rule('top right corner', 43, 1, 5, 6, 'min',
                    ["Obiekt ", " znajduje się w prawym-górnym narożniku pola", ". "])
    rules[3] = Rule('bottom right corner', 44, 1, 5, 10, 'min',
                    ["Obiekt ", " w prawym-dolnym narożniku pola", ". "])
    rules[4] = Rule('bottom left corner', 45, 1, 1, 10, 'min',
                    ["Obiekt ", " znajduje się w lewym-dolnym narożniku pola", ". "])
    rules[5] = Rule('top left part', 46, 1, 2, 7, 'min',
                    ["Obiekt ", " znajduje się w lewej-górnej części pola", ". "])
    rules[6] = Rule('top right part', 47, 1, 4, 7, 'min',
                    ["Obiekt ", " znajduje się w prawej-górnej części pola", ". "])
    rules[7] = Rule('bottom right part', 48, 1, 4, 9, 'min',
                    ["Obiekt ", " znajduje się w prawej-dolnej części pola", ". "])
    rules[8] = Rule('bottom left part', 49, 1, 2, 9, 'min',
                    ["Obiekt ", " znajduje się w lewej-dolnej części pola", ". "])
    return rules


# predefined field size
def get_field_size():
    return [400, 400]
