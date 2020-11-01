# import the necessary packages
import cv2
import numpy as np

from DrawField import draw_field
from InputData import input_data
from Obj import Obj
from SceneDescription import scene_description, show_image


def _interactive_mode(image_path):
    image = cv2.imread(image_path)
    img_h, image_w, channels = image.shape

    def show_rectangles():
        for index, ref_point in enumerate(ref_points):
            rec = cv2.rectangle(image, ref_point[0], ref_point[1], ref_point[2], 2)
            x, y = ref_point[0]
            cv2.putText(rec, str(index), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, ref_point[2], 2)
        cv2.imshow("image", image)

    def adj_x(corner):
        corner_l = list(corner)
        corner_l[0] += 5
        return tuple(corner_l)

    def unadj_x(corner):
        corner_l = list(corner)
        corner_l[0] -= 5
        return tuple(corner_l)

    def unadj_y(corner):
        corner_l = list(corner)
        corner_l[1] -= 5
        return tuple(corner_l)

    def adj_y(corner):
        corner_l = list(corner)
        corner_l[1] += 5
        return tuple(corner_l)

    clone = image.copy()
    cv2.namedWindow("image")

    ref_points = [[(30, 30), (60, 60), (0, 255, 0)]]
    actual_rectangle = ref_points[0]
    actual_rectangle_idx = 0
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break
        elif key == ord("0"):
            actual_rectangle = ref_points[0]
            actual_rectangle_idx = 0
            print("You chose rectangle number 0.")
        elif key == ord("1"):
            actual_rectangle = ref_points[1]
            actual_rectangle_idx = 1
            print("You chose rectangle number 1.")
        elif key == ord("2"):
            actual_rectangle = ref_points[2]
            actual_rectangle_idx = 2
            print("You chose rectangle number 2.")
        elif key == ord("3"):
            actual_rectangle = ref_points[3]
            actual_rectangle_idx = 3
            print("You chose rectangle number 3.")
        elif key == ord("n"):
            color = list(np.random.random(size=3) * 256)
            ref_points.append([(80, 80), (110, 110), color])
            actual_rectangle = ref_points[-1]
            actual_rectangle_idx = len(ref_points) - 1
            # draw a rectangle around the region of interest
            show_rectangles()
        elif key == ord("d"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_x(actual_rectangle[0])
            actual_rectangle[1] = adj_x(actual_rectangle[1])

            # draw a rectangle around the region of interest
            image = clone.copy()
            show_rectangles()
        elif key == ord("w"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_y(actual_rectangle[0])
            actual_rectangle[1] = unadj_y(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        elif key == ord("s"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_y(actual_rectangle[0])
            actual_rectangle[1] = adj_y(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        elif key == ord("a"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_x(actual_rectangle[0])
            actual_rectangle[1] = unadj_x(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        # up arrow
        elif key == ord("i"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_y(actual_rectangle[0])
            actual_rectangle[1] = adj_y(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        # down arrow
        elif key == ord("k"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_y(actual_rectangle[0])
            actual_rectangle[1] = unadj_y(actual_rectangle[1])
            image = clone.copy()
            show_rectangles()
        # right arrow
        elif key == ord("l"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_x(actual_rectangle[0])
            actual_rectangle[1] = adj_x(actual_rectangle[1])
            # draw a rectangle around the region of interest
            image = clone.copy()
            show_rectangles()
        # left arrow
        elif key == ord("j"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_x(actual_rectangle[0])
            actual_rectangle[1] = unadj_x(actual_rectangle[1])
            # draw a rectangle around the region of interest
            image = clone.copy()
            show_rectangles()
        elif key == ord("y"):
            if ref_points.__len__() > 1:
                _calculate_pos(ref_points, image_w, img_h)
    # close all open windows
    cv2.destroyAllWindows()


def _calculate_pos(ref_points, image_w, image_h):
    v_boxes = {}
    for index, ref_point in enumerate(ref_points):
        XtopLeft, YtopLeft = ref_point[0][0], ref_point[0][1]
        XbottomRight, YbottomRight = ref_point[1][0], ref_point[1][1]

        X_len = abs(XbottomRight - XtopLeft)
        Y_len = abs(YbottomRight - YtopLeft)
        obj = Obj(str(index), [YtopLeft, XtopLeft], [Y_len, X_len])

        v_boxes[index] = obj
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()

    description = scene_description(v_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    print("Area method")


def create_output_image_and_desc():
    create_bound_boxes, create_prop, create_rels, create_rules, get_field_size = input_data()
    description = scene_description(create_bound_boxes, create_prop, create_rels, create_rules, get_field_size)
    print(description)
    imf = draw_field(create_bound_boxes, get_field_size, -1, 1)
    show_image(imf)


_interactive_mode("bicycle_boxed.jpg")