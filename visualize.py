import cv2
import os
import glob
import json
import math
import numpy as np


def new_coord(cur_x, cur_y, offset_x, offset_y, mul_x, mul_y):
    new_x = (cur_x + offset_x) * mul_x + 105
    new_y = (cur_y + offset_y) * mul_y + 5
    return (int(new_x) - 100, 600 - int(new_y))


def check_arrow(img_name, img_path, json_path, save_path):
    output_path = save_path + '/' + img_name + '.png'

    img = cv2.imread(img_path)
    data = None
    with open(json_path) as f:
        data = json.load(f)

    color = (0, 255, 0)
    thickness = 2

    min_x = 1000
    max_x = -1000
    min_y = 1000
    max_y = -1000
    for line in data['line']:
        min_x = min(min_x, line['start_x'], line['end_x'])
        max_x = max(max_x, line['start_x'], line['end_x'])
        min_y = min(min_y, line['start_y'], line['end_y'])
        max_y = max(max_y, line['start_y'], line['end_y'])

    # let min_x, min_y to be origin

    offset_x = -min_x
    offset_y = -min_y
    # an offset is applied to all coordinates from JSON

    mul_x = 590 / (max_x + offset_x)
    mul_y = 590 / (max_y + offset_y)

    for line in data['line']:
        start_point = new_coord(
            line['start_x'], line['start_y'], offset_x, offset_y, mul_x, mul_y)
        end_point = new_coord(
            line['end_x'], line['end_y'], offset_x, offset_y, mul_x, mul_y)
        img = cv2.line(img, start_point, end_point, color, thickness)

    for arrow in data['arrow']:
        arrow_point = new_coord(
            arrow['x'], arrow['y'], offset_x, offset_y, mul_x, mul_y)
        img = cv2.circle(img, arrow_point, 2, color, thickness)

    cv2.imwrite(output_path, img)
    # cv2.imshow('ImageWindow', img)
    # cv2.waitKey()


if __name__ == "__main__":
    img_path = './with_dash_png/*.png'
    json_path_ori = './arrow_json_garbage'
    save_path = './arrow_check'

    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    path = glob.glob(img_path)

    for img in path:
        if img.endswith('0.png'):
            img_name = os.path.basename(img).split('.')[0]
            json_path = json_path_ori + '/' + img_name + '.json'
            check_arrow(img_name, img, json_path, save_path)
