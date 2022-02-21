import ezdxf
import sys
import json
import math
import numpy as np


class Arrow_Reader:

    def __init__(self):

        self.data = {'line': [], 'linear_dimension': [],
                     'diameter_dimension': [], 'arrow': []}
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
            if e.dxftype() == 'DIMENSION':

                if e.dxf.dimtype == 32:
                    text_pos = e.dxf.text_midpoint
                    text_x = text_pos[0]
                    text_y = text_pos[1]

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
                        'text_x': text_x,
                        'text_y': text_y,
                        'angle': angle
                    })

                    arrow_x1 = 0
                    arrow_y1 = 0
                    arrow_x2 = 0
                    arrow_y2 = 0
                    if angle == 0:
                        arrow_y1 = text_y - 2
                        arrow_y2 = text_y - 2
                        delta_x = abs(b_x - text_x)
                        arrow_x1 = b_x
                        arrow_x2 = b_x - 2 * delta_x
                    else:

                        delta_y = abs(b_y - text_y)
                        arrow_y1 = b_y

                        arrow_x1 = text_x + 2
                        arrow_x2 = text_x + 2
                        arrow_y2 = b_y - 2 * delta_y

                        # if b_x < p1_x:
                        #     arrow_x1 = text_x + 2
                        #     arrow_x2 = text_x + 2
                        #     arrow_y2 = b_y - 2 * delta_y
                        # else:
                        #     arrow_x1 = text_x - 2
                        #     arrow_x2 = text_x - 2
                        #     arrow_y2 = b_y + 2 * delta_y

                    self.data['arrow'].append({
                        'x': arrow_x1,
                        'y': arrow_y1,
                        'angle': angle
                    })

                    self.data['arrow'].append({
                        'x': arrow_x2,
                        'y': arrow_y2,
                        'angle': angle
                    })

                else:
                    text_pos = e.dxf.text_midpoint
                    text_x = text_pos[0]
                    text_y = text_pos[1]

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
                        'location_y': location_y,
                        'text_x': text_x,
                        'text_y': text_y
                    })

                    # y = kx + b
                    k = (location_y - center_y) / (location_x - center_x)
                    b = location_y - k * location_x

                    arrow_x = 0
                    arrow_y = 0
                    angle = 0
                    # if location_x > center_x:
                    arrow_x1 = center_x - np.sqrt(radius**2 / (1 + k**2))
                    arrow_x2 = center_x + np.sqrt(radius**2 / (1 + k**2))
                    arrow_y1 = k * arrow_x1 + b
                    arrow_y2 = k * arrow_x2 + b
                    if location_x > center_x:
                        arrow_x = max(arrow_x1, arrow_x2)
                    else:
                        arrow_x = min(arrow_x1, arrow_x2)

                    if location_y > center_y:
                        arrow_y = max(arrow_y1, arrow_y2)
                    else:
                        arrow_y = min(arrow_y1, arrow_y2)

                    if abs(k) > 0.5:
                        angle = 90
                    else:
                        angle = 0

                    self.data['arrow'].append({
                        'x': arrow_x,
                        'y': arrow_y,
                        'angle': angle
                    })

    def save_json(self, save_path):
        """
        Save the dictionary into a json file.
        :param save_path: input file path
        """
        json_object = json.dumps(self.data, indent=4)
        with open(save_path, 'w') as outfile:
            outfile.write(json_object)

# if __name__ == "__main__":
#     path = './dxf_tobe_converted/0265_s_0_6.DXF'
#     output_path = '0265_s_0_0.json'
#     reader = Arrow_Reader()
#     reader.read_dxf(path)

#     # dwg = reader.doc
#     # print ("EXTMAX ", dwg.header['$EXTMAX'])
#     # print ("EXTMIN ", dwg.header['$EXTMIN'])
#     # print ("LIMMAX ", dwg.header['$LIMMAX'])
#     # print ("LIMMIN ", dwg.header['$LIMMIN'])

#     reader.save_info()
#     reader.save_json(output_path)
