def grouping(b_boxes_to_merge):
    XtopLeftList, YtopLeftList = list(), list()
    XbottomRightList, YbottomRightList = list(), list()
    for box in b_boxes_to_merge:
        XtopLeftList.append(int(box[1]))
        YtopLeftList.append(int(box[2]))
        XbottomRightList.append(int(box[3]))
        YbottomRightList.append(int(box[4]))

    return min(XtopLeftList), min(YtopLeftList), max(XbottomRightList), max(YbottomRightList), b_boxes_to_merge[0][5]


def group_filter_name(names_set: set, v_boxes_temp: list):
    groups = {}
    v_boxes_new = []
    if names_set.__len__() != v_boxes_temp.__len__():
        for name in names_set:
            groups[name] = []
            for box in v_boxes_temp:
                temp_name = box[0]
                if temp_name == name:
                    groups[name].append(box)
    for key, value in groups.items():
        if len(value) > 1:
            v_boxes_new.append([key] + list(grouping(value)))
        else:
            v_boxes_new.append(value[0])
    return v_boxes_new


def intersection_measure(v_boxes_temp: list, n=15):
    intersection_list = []
    for boxA in v_boxes_temp:
        intersection_row = []
        boxAadj = adj_width_height(boxA, n)
        for boxB in v_boxes_temp:
            intersection_over_union_val = intersection_over_union(boxA, boxB)
            if intersection_over_union_val == 0:
                boxBadj = adj_width_height(boxB, n)
                intersection_over_union_val = intersection_over_union(boxAadj, boxBadj)
            intersection_row.append(intersection_over_union_val)
        intersection_list.append(intersection_row)
    return intersection_list


def adj_width_height(box, n):
    XtopLeft, YtopLeft = int(box[1]), int(box[2])
    XbottomRight, YbottomRight = int(box[3]), int(box[4])
    return box[0], XtopLeft - n, YtopLeft - n, XbottomRight + n, YbottomRight + n


def intersection_over_union(box1, box2):
    x1, y1, w1, h1 = change_to_width_len_format(box1)
    x2, y2, w2, h2 = change_to_width_len_format(box2)
    w_intersection = min(x1 + w1, x2 + w2) - max(x1, x2)
    h_intersection = min(y1 + h1, y2 + h2) - max(y1, y2)
    if w_intersection <= 0 or h_intersection <= 0:  # No overlap
        return 0
    I = w_intersection * h_intersection
    U = w1 * h1 + w2 * h2 - I  # Union = Total Area - I
    return I / U


def change_to_width_len_format(box):
    XtopLeft, YtopLeft = int(box[1]), int(box[2])
    XbottomRight, YbottomRight = int(box[3]), int(box[4])
    X_len = abs(XbottomRight - XtopLeft)
    Y_len = abs(YbottomRight - YtopLeft)
    return XtopLeft, YtopLeft, X_len, Y_len
