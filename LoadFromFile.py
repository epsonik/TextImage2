import csv

import cv2
import numpy as np

from InputData import input_data, get_field_size
from Obj import Obj
from SceneDescription import scene_description

image = np.zeros((get_field_size()[0], get_field_size()[1], 3), np.uint8)


def save_desc_to_file(description, file_name):
    file_name=file_name.replace('.csv','_description.csv')
    w = csv.writer(open(file_name, "w"))
    w.writerow(description)


def show_rectangles(bound_boxes):
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
        if key == ord("c"):
            break


def load_from_file(bound_boxes, readCSV, file_name):
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    save_desc_to_file(description, file_name)
    show_rectangles(readCSV)


file_name = input("Enter a file name to load bBoxes. Data must be delimited with ',': ")
file_name = str(file_name)

# Prints in the console the variable as requested
print("The file name you entered is: ", file_name)
v_boxes = {}
v_boxes_temp = []
with open(file_name) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for b_box in readCSV:
        name = b_box[0]
        v_boxes_temp.append(b_box)
        XtopLeft, YtopLeft = int(b_box[1]), int(b_box[2])
        XbottomRight, YbottomRight = int(b_box[3]), int(b_box[4])
        X_len = abs(XbottomRight - XtopLeft)
        Y_len = abs(YbottomRight - YtopLeft)
        obj = Obj(name, [YtopLeft, XtopLeft], [Y_len, X_len])
        v_boxes[int(name)] = obj
load_from_file(v_boxes, v_boxes_temp, file_name)
