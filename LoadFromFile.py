import csv

from DrawField import draw_field
from InputData import input_data
from Obj import Obj
from SceneDescription import scene_description, show_image


def save_desc_to_file(description, file_name):
    w = csv.writer(open(file_name, "a+"))
    w.writerow(description)


def load_from_file(bound_boxes, file_name):
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    save_desc_to_file(description, file_name)


file_name = input("Enter a file name to load bBoxes. Data must be delimited with ',': ")
file_name = str(file_name)

# Prints in the console the variable as requested
print("The file name you entered is: ", file_name)
v_boxes = {}
with open(file_name) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for b_box in readCSV:
        name = b_box[0]
        XtopLeft, YtopLeft = int(b_box[1]), int(b_box[2])
        XbottomRight, YbottomRight = int(b_box[3]), int(b_box[4])

        X_len = abs(XbottomRight - XtopLeft)
        Y_len = abs(YbottomRight - YtopLeft)
        obj = Obj(name, [YtopLeft, XtopLeft], [Y_len, X_len])

        v_boxes[int(name)] = obj
load_from_file(v_boxes, file_name)
