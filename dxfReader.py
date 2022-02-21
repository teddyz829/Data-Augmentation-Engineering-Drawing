import ezdxf
import sys
import json
import math


class Reader:

    def __init__(self):

        self.data = {'line': [], 'dash_line': [], 'circle': [], 'arc': [],
                     'construction_line': [], 'linear_dimension': [],
                     'diameter_dimension': []}
        self.doc = None
        self.msp = None

    def read_dxf(self, dxf_input):
        """
        Read input dxf file.
        :param dxf_input: dxf file
        """
        self.doc = ezdxf.readfile(dxf_input)
        self.msp = self.doc.modelspace()

    def save_info(self):
        """
        Parse info from model space and save info in to dictionary.
        """

        for e in self.msp:
            if e.dxftype() == 'LINE':
                if e.dxf.linetype == 'HIDDEN':
                    self.data['dash_line'].append({
                        'start_x': e.dxf.start[0],
                        'start_y': e.dxf.start[1],
                        'end_x': e.dxf.end[0],
                        'end_y': e.dxf.end[1]
                    })
                else:
                    self.data['line'].append({
                        'start_x': e.dxf.start[0],
                        'start_y': e.dxf.start[1],
                        'end_x': e.dxf.end[0],
                        'end_y': e.dxf.end[1]
                    })
            if e.dxftype() == 'CIRCLE':
                self.data['circle'].append({
                    'center_x': e.dxf.center[0],
                    'center_y': e.dxf.center[1],
                    'radius': e.dxf.radius
                })
                self.data['construction_line'].append({
                    'start_x': e.dxf.center[0] - 1.4 * e.dxf.radius,
                    'start_y': e.dxf.center[1],
                    'end_x': e.dxf.center[0] + 1.4 * e.dxf.radius,
                    'end_y': e.dxf.center[1]
                })
                self.data['construction_line'].append({
                    'start_x': e.dxf.center[0],
                    'start_y': e.dxf.center[1] - 1.4 * e.dxf.radius,
                    'end_x': e.dxf.center[0],
                    'end_y': e.dxf.center[1] + 1.4 * e.dxf.radius
                })
            if e.dxftype() == 'ARC':
                self.data['arc'].append({
                    'center_x': e.dxf.center[0],
                    'center_y': e.dxf.center[1],
                    'radius': e.dxf.radius,
                    'start_angle': e.dxf.start_angle,
                    'end_angle': e.dxf.end_angle
                })
            if e.dxftype() == 'DIMENSION':
                if e.dxf.dimtype == 160:
                    p1_x = e.dxf.defpoint2[0]
                    p1_y = e.dxf.defpoint2[1]
                    p2_x = e.dxf.defpoint3[0]
                    p2_y = e.dxf.defpoint3[1]
                    # determine horizontal还是vertical
                    angle = 90
                    l_x = e.dxf.text_midpoint[0]
                    l_y = e.dxf.text_midpoint[1]
                    if ((p1_x < l_x < p2_x) or (p1_x > l_x > p2_x)) and (
                            (l_y > p1_y and l_y > p2_y) or (
                            l_y < p1_y and l_y < p2_y)):
                        angle = 0
                    # edge cases of angle:
                    if p1_y == p2_y:
                        angle = 0

                    # identify the start and end point of the dimension
                    # if it is horizontal the one with smaller x coordinate is point1
                    if angle == 0 and p1_x > p2_x:
                        p1_x = e.dxf.defpoint3[0]
                        p1_y = e.dxf.defpoint3[1]
                        p2_x = e.dxf.defpoint2[0]
                        p2_y = e.dxf.defpoint2[1]

                    # if it is vertical, the one with smaller y coordinat is point1
                    if angle == 90 and p1_y > p2_y:
                        p1_x = e.dxf.defpoint3[0]
                        p1_y = e.dxf.defpoint3[1]
                        p2_x = e.dxf.defpoint2[0]
                        p2_y = e.dxf.defpoint2[1]

                    b_x = p2_x
                    b_y = e.dxf.text_midpoint[1]

                    if angle == 90:
                        b_x = e.dxf.text_midpoint[0]
                        b_y = p2_y

                    self.data['linear_dimension'].append({
                        'base_point_x': b_x,
                        'base_point_y': b_y,
                        'dimension_point1_x': p1_x,
                        'dimension_point1_y': p1_y,
                        'dimension_point2_x': p2_x,
                        'dimension_point2_y': p2_y,
                        'angle': angle
                    })
                else:
                    p1_x = e.dxf.defpoint[0]
                    p1_y = e.dxf.defpoint[1]
                    p2_x = e.dxf.defpoint4[0]
                    p2_y = e.dxf.defpoint4[1]
                    center_x = p1_x
                    center_y = p1_y
                    radius = math.sqrt(
                        (p1_x - p2_x) ** 2 + (p1_y - p2_y) ** 2)

                    k = (p1_y - p2_y) / (p1_x - p2_x)
                    b = (p1_y - k * p1_x)
                    location_y = e.dxf.text_midpoint[1] - 1.25 - 0.625
                    location_x = (location_y - b) / k

                    self.data['diameter_dimension'].append({
                        'center_x': center_x,
                        'center_y': center_y,
                        'radius': radius,
                        'location_x': location_x,
                        'location_y': location_y
                    })

    def save_json(self, save_path):
        """
        Save the dictionary into a json file.
        :param save_path: input file path
        """
        json_object = json.dumps(self.data, indent=4)
        with open(save_path, 'w') as outfile:
            outfile.write(json_object)
