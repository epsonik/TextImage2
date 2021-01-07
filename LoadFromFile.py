import csv
import os

import cv2
import numpy as np

from InputData import input_data, get_field_size
from Intersection import change_to_width_len_format, group_filter_name
from Obj import Obj
from SceneDescription import scene_description


def save_desc_to_file(description, file_name):
    file_name = file_name.replace('.csv', '_description.csv')
    w = csv.writer(open(file_name, "w"))
    w.writerow(description)


def show_rectangles(bound_boxes):
    image = np.zeros((get_field_size()[0], get_field_size()[1], 3), np.uint8)
    for _, ref_point in enumerate(bound_boxes):
        color = tuple(eval(ref_point[5]))
        l = (int(ref_point[1]), int(ref_point[2]))
        r = (int(ref_point[3]), int(ref_point[4]))
        rec = cv2.rectangle(image, l, r, color, 2)
        x, y = int(ref_point[1]), int(ref_point[2])
        name = str(ref_point[0])
        cv2.putText(rec, name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 2)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        # if the 'c' key is pressed, break from the loop
        cv2.imshow("image", image)
        cv2.imwrite(file_name.replace('.csv', '_image.jpg'), image)

        if key == ord("c"):
            break


def show_rectangles_grouping(v_boxes_new, v_boxes_old):
    def show_img(image_t, b_boxes):
        for _, ref_point in enumerate(b_boxes):
            color = tuple(eval(ref_point[5]))
            l = (int(ref_point[1]), int(ref_point[2]))
            r = (int(ref_point[3]), int(ref_point[4]))
            rec = cv2.rectangle(image_t, l, r, color, 2)
            x, y = int(ref_point[1]), int(ref_point[2])
            name = str(ref_point[0])
            cv2.putText(rec, name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 2)
        return image_t

    imageNew = np.zeros((get_field_size()[0], get_field_size()[1], 3), np.uint8)
    imageNew = show_img(imageNew, v_boxes_new)
    imageOld = np.zeros((get_field_size()[0], get_field_size()[1], 3), np.uint8)
    imageOld = show_img(imageOld, v_boxes_old)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("imageNEW", imageNew)
        cv2.imshow("imageOLD", imageOld)
        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        # if the 'c' key is pressed, break from the loop
        cv2.imshow("imageNEW", imageNew)
        cv2.imshow("imageOLD", imageOld)
        cv2.imwrite(file_name.replace('.csv', '_image.jpg'), imageNew)
        cv2.imwrite(file_name.replace('.csv', '_image.jpg'), imageOld)
        if key == ord("c"):
            break


def load_from_file(bound_boxes, v_boxes_new, file_name, v_boxes_old):
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(*description, sep='\n')
    save_desc_to_file(description, file_name)
    show_rectangles_grouping(v_boxes_new, v_boxes_old)


def prepare(v_boxes_n):
    v_boxes = []
    for b_box in v_boxes_n:
        name = b_box[0]
        XtopLeft, YtopLeft, X_len, Y_len = change_to_width_len_format(b_box)
        obj = Obj(name, [YtopLeft, XtopLeft], [Y_len, X_len])
        v_boxes.append(obj)
    return v_boxes


# file_name = input("Enter a file name to load bBoxes. Data must be delimited with ',': ")
# file_name = str(file_name)
#
# # Prints in the console the variable as requested
# print("The file name you entered is: ", file_name)
os.chdir(r'test')
os.chdir(r'grouping_test')
file_name = "COCO_train2014_000000360452grouping_test_10.csv"
v_boxes_temp = []
names_set = set()
with open(file_name) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for box in readCSV:
        if len(box) > 0:
            v_boxes_temp.append(box)
            name = box[0]
            names_set.add(name)
v_boxes_new = group_filter_name(names_set, v_boxes_temp)
v_boxes = prepare(v_boxes_new)

load_from_file(v_boxes, v_boxes_new, file_name, v_boxes_temp)
