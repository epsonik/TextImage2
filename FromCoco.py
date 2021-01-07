import csv
import os

import numpy as np

from InputData import input_data
from SceneDescription import scene_description
from YOLO.img_det import vbox_engine


def save_desc_to_file(description, file_name):
    file_name = file_name.replace('.jpg', '_description.csv')
    w = csv.writer(open(file_name, "w"))
    w.writerow(description)


def load_from_file(bound_boxes, file_name):
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    save_desc_to_file(description, file_name)


def save_b_boxes(v_boxes, v_labels, input_filename, image_w, image_h):
    w = csv.writer(open(input_filename, "w"))

    for index, ref_point in enumerate(v_boxes):
        box = v_boxes[index]
        color = list(np.random.random(size=3) * 256)
        XtopLeft = int(box.XtopLeft * 400 / image_w)
        YtopLeft = int(box.YtopLeft * 400 / image_h)
        XbottomRight = int(box.XbottomRight * 400 / image_w)
        YbottomRight = int(box.YbottomRight * 400 / image_h)
        w.writerow([v_labels[index], XtopLeft, YtopLeft, XbottomRight, YbottomRight, color])


def process_for_grouping():
    os.chdir(r'test')
    _, _, filenames = next(os.walk(('grouping_test')))
    os.chdir(r'grouping_test')
    for idx, input_filename in enumerate(filenames):
        v_boxes, v_labels, v_scores, image_w, image_h = vbox_engine(input_filename)
        new_name = 'grouping_test_{}.csv'.format(idx)
        input_filename = input_filename.replace('.jpg', new_name)
        save_b_boxes(v_boxes, v_labels, input_filename, image_w, image_h)


process_for_grouping()
# input_filename = input("Enter a file name to load bBoxes. Data must be delimited with ',': ")
# input_filename = str(input_filename)
#
# # Prints in the console the variable as requested
# print("The file name you entered is: ", input_filename)
# photo_boxed_filename = input_filename.replace('.jpg', '_boxed.jpg')
# v_boxes, v_labels, v_scores, image_w, image_h = vbox_engine(input_filename)
# draw_boxes(input_filename, photo_boxed_filename, v_boxes, v_labels, v_scores)
#
# v_boxes_t = {}
# v_boxes_temp = []
# for i in range(len(v_boxes)):
#     box = v_boxes[i]
#     X_len = abs(box.XbottomRight - box.XtopLeft)
#     Y_len = abs(box.YbottomRight - box.YtopLeft)
#     obj = Obj(v_labels[i], [box.YtopLeft, box.XtopLeft], [Y_len, X_len])
#     v_boxes_t[i] = obj
# load_from_file(v_boxes_t, input_filename, v_labels)
