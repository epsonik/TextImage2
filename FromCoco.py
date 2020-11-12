import csv

from InputData import input_data
from Obj import Obj
from SceneDescription import scene_description
from YOLO.img_det import vbox_engine, draw_boxes


def save_desc_to_file(description, file_name):
    file_name = file_name.replace('.jpg', '_description.csv')
    w = csv.writer(open(file_name, "w"))
    w.writerow(description)


def load_from_file(bound_boxes, file_name):
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    save_desc_to_file(description, file_name)


input_filename = input("Enter a file name to load bBoxes. Data must be delimited with ',': ")
input_filename = str(input_filename)

# Prints in the console the variable as requested
print("The file name you entered is: ", input_filename)
input_filename = 'street.jpg'
photo_boxed_filename = input_filename.replace('.jpg', '_boxed.jpg')
v_boxes, v_labels, v_scores, image_w, image_h = vbox_engine(input_filename)
draw_boxes(input_filename, photo_boxed_filename, v_boxes, v_labels, v_scores)

v_boxes = {}
v_boxes_temp = []
for i in range(len(v_boxes)):
    box = v_boxes[i]
    X_len = abs(box.XbottomRight - box.XtopLeft)
    Y_len = abs(box.YbottomRight - box.YtopLeft)
    obj = Obj(str(i), [box.YtopLeft, box.XtopLeft], [Y_len, X_len])
    v_boxes[i] = obj
load_from_file(v_boxes, input_filename)
