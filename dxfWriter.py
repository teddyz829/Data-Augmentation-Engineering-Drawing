import ezdxf
from dxfIO import streamIO
import json
import sys
import random
import itertools


class AddEntity:

    def __init__(self, streamIO=None, file_name=None):
        self.streamIO = streamIO

        with open(file_name, 'r') as openfile:
            self.json_object = json.load(openfile)

    def add_line(self, start, end, layer):
        """
        Add a line to the dxf file.
        :param start: start point coordinate, (x,y) tuple.
        :param end: end point coordinate, (x,y) tuple.
        :param layer: String type, can be 'CONSTRUCTION', 'DIMENSION', 'CONTOUR'.
        :return: N/A.
        """
        self.streamIO.msp.add_line(start, end, dxfattribs={'layer': layer})



    def add_line_color(self, start, end, layer):
        """
        Add a colored line to the dxf file. (This is for construction line) use blue color
        :param start: start point coordinate, (x,y) tuple.
        :param end: end point coordinate, (x,y) tuple.
        :param layer: String type, can be 'CONSTRUCTION', 'DIMENSION', 'CONTOUR'.
        :return: N/A.
        """
        self.streamIO.msp.add_line(start, end, dxfattribs={'layer': layer, 'color': 2})


    def add_circle(self, center, radius, layer):
        """
        Add a circle to the dxf file.
        :param center: center of circle, (x,y) tuple
        :param radius: radius of circle, positive float.
        :param layer: String type, can be 'CONSTRUCTION', 'DIMENSION', 'CONTOUR'.
        :return: N/A
        """
        self.streamIO.msp.add_circle(center, radius,
                                     dxfattribs={'layer': layer})

    def add_arc(self, center, radius, start, end, layer):
        """
        Add an arc to the dxf file.
        :param center: center of arc, (x,y) tuple
        :param radius: radius of arc, positive float.
        :param start: start angle of arc, float. Angle start at the
        positive x position. Angle increase in counterclockwise direction.
        :param end: end angle of arc, float.
        :param layer: String type, can be 'CONSTRUCTION', 'DIMENSION', 'CONTOUR'.
        :return: N/A
        """
        self.streamIO.msp.add_arc(center, radius, start, end,
                                  dxfattribs={'layer': layer})

    def add_text(self, text, position, rotation, align):
        """
        Add text to the dxf file.
        :param text: String type, text.
        :param position: location of text, (x,y) tuple.
        :param rotation: angle of text. Angle start at the
        positive x position. Angle increase in counterclockwise direction.
        :param align: text alignment, can be 'TOP_LEFT', 'TOP_CENTER', 'TOP_RIGHT',
        'Middle', 'MIDDLE_LEFT', 'MIDDLE_CENTER', 'MIDDLE_RIGHT', 'Bottom',
        'BOTTOM_LEFT', 'BOTTOM_CENTER', 'BOTTOM_RIGHT', 'Baseline', 'LEFT',
        'CENTER', 'RIGHT'.
        :return: N/A
        """
        self.streamIO.msp.add_text(text, dxfattribs={'color': 5,
                                                     'rotation': rotation}).set_pos(
            position, align=align)





    def add_linear_dimension(self, base, start, end, angles):
        self.streamIO.msp.add_linear_dim(base=base, p1=start, p2=end,
                                         angle=angles,
                                         override={'dimdec': 2,  ## decimal places
                                                   'dimlfac': 1,  ## scale factor
                                                   'dimrnd': 0.01,  ## rounding
                                                   'dimdsep': ord('.'),
                                                   'dimclre': 5,   ## extension line color  blue
                                                   'dimclrt': 6,   ## text color  Magenta
                                                   'dimclrd': 1,   ## dimension color  red
                                                   'dimasz': 2,   ## arrow size
                                                   'dimtsz': 0,
                                                   'dimtxsty': 'Standard'}).render()

    def add_diameter_dimension(self, center, radius, location):
        self.streamIO.msp.add_radius_dim(center=center, location=location,
                                         radius=radius,
                                         override={'dimtoh': 1,
                                                   'dimcen': 2.5,
                                                   'dimlfac': 1,
                                                   'dimrnd': 0.01,
                                                   'dimdsep': ord('.'),
                                                   'dimdec': 2,
                                                   'dimclre': 5,
                                                   'dimclrt': 6,
                                                   'dimclrd': 1,
                                                #    'dimasz': 1,
                                                   'dimtxsty': 'Standard'}).render()


    def draw_contour_line(self):
        if len(self.json_object.get('line')) != 0:
            for i in range(len(self.json_object.get('line'))):
                x1 = self.json_object.get('line')[i].get('start_x')
                y1 = self.json_object.get('line')[i].get('start_y')
                x2 = self.json_object.get('line')[i].get('end_x')
                y2 = self.json_object.get('line')[i].get('end_y')
                self.add_line((x1, y1), (x2, y2), 'CONTOUR_LINE')

    def draw_contour_circle(self):
        if len(self.json_object.get('circle')) != 0:
            for i in range(len(self.json_object.get('circle'))):
                center_x = self.json_object.get('circle')[i].get('center_x')
                center_y = self.json_object.get('circle')[i].get('center_y')
                radius = self.json_object.get('circle')[i].get('radius')
                self.add_circle((center_x, center_y), radius, 'CONTOUR_CIRCLE')

    def draw_contour_arc(self):
        if len(self.json_object.get('arc')) != 0:
            for i in range(len(self.json_object.get('arc'))):
                center_x = self.json_object.get('arc')[i].get('center_x')
                center_y = self.json_object.get('arc')[i].get('center_y')
                radius = self.json_object.get('arc')[i].get('radius')
                start_angle = self.json_object.get('arc')[i].get('start_angle')
                end_angle = self.json_object.get('arc')[i].get('end_angle')
                self.add_arc((center_x, center_y), radius, start_angle,
                               end_angle, 'CONTOUR_ARC')

    def draw_dash(self):
        if len(self.json_object.get('dash_line')) != 0:
            for i in range(len(self.json_object.get('dash_line'))):
                x1 = self.json_object.get('dash_line')[i].get('start_x')
                y1 = self.json_object.get('dash_line')[i].get('start_y')
                x2 = self.json_object.get('dash_line')[i].get('end_x')
                y2 = self.json_object.get('dash_line')[i].get('end_y')
                self.add_line((x1, y1), (x2, y2), 'CONTOUR_DASH')

    def draw_construction(self):
        if len(self.json_object.get('construction_line')) != 0:
            for i in range(len(self.json_object.get('construction_line'))):
                x1 = self.json_object.get('construction_line')[i].get('start_x')
                y1 = self.json_object.get('construction_line')[i].get('start_y')
                x2 = self.json_object.get('construction_line')[i].get('end_x')
                y2 = self.json_object.get('construction_line')[i].get('end_y')
                # self.add_line((x1, y1), (x2, y2), 'CONSTRUCTION')
                self.add_line_color((x1, y1), (x2, y2), 'CONSTRUCTION')

    def draw_dimension(self):
        if len(self.json_object.get('linear_dimension')) != 0:
            for i in range(len(self.json_object.get('linear_dimension'))):
                base_x = self.json_object.get('linear_dimension')[i].get(
                    'base_point_x')
                base_y = self.json_object.get('linear_dimension')[i].get(
                    'base_point_y')
                p1_x = self.json_object.get('linear_dimension')[i].get(
                    'dimension_point1_x')
                p1_y = self.json_object.get('linear_dimension')[i].get(
                    'dimension_point1_y')
                p2_x = self.json_object.get('linear_dimension')[i].get(
                    'dimension_point2_x')
                p2_y = self.json_object.get('linear_dimension')[i].get(
                    'dimension_point2_y')
                angle = self.json_object.get('linear_dimension')[i].get('angle')
                self.add_linear_dimension((base_x, base_y), (p1_x, p1_y),
                                            (p2_x, p2_y), angle)

        if len(self.json_object.get('diameter_dimension')) != 0:
            for i in range(len(self.json_object.get('diameter_dimension'))):
                center_x = self.json_object.get('diameter_dimension')[i].get(
                    'center_x')
                center_y = self.json_object.get('diameter_dimension')[i].get(
                    'center_y')
                radius = self.json_object.get('diameter_dimension')[i].get(
                    'radius')
                l_x = self.json_object.get('diameter_dimension')[i].get(
                    'location_x')
                l_y = self.json_object.get('diameter_dimension')[i].get(
                    'location_y')
                self.add_diameter_dimension((center_x, center_y), radius,
                                              (l_x, l_y))

    # def draw_bound(self):
    #     # self.add_line((0,0),(600,0), "CONTOUR_LINE")
    #     # self.add_line((600,0),(600,600), "CONTOUR_LINE")
    #     # self.add_line((600,600),(0,600), "CONTOUR_LINE")
    #     # self.add_line((0,600),(0,0), "CONTOUR_LINE")
    #     x_point = []; y_point = []
    #     if len(self.json_object.get('line')) != 0:
    #         for i in range(len(self.json_object.get('line'))):
    #             x1 = self.json_object.get('line')[i].get('start_x')
    #             y1 = self.json_object.get('line')[i].get('start_y')
    #             x2 = self.json_object.get('line')[i].get('end_x')
    #             y2 = self.json_object.get('line')[i].get('end_y')
    #             x_point.append(x1); x_point.append(x2)
    #             y_point.append(y1); y_point.append(y2)

    #     x_min = min(x_point); x_max = max(x_point)
    #     y_min = min(y_point); y_max = max(y_point)

    #     l = 35

    #     c_x = (x_max + x_min) / 2
    #     c_y = (y_max + y_min) / 2
    #     if (x_max - x_min) >= (y_max - y_min):
    #         x1 = c_x - (x_max - c_x) - l
    #         y1 = c_y - (x_max - c_x) - l
    #         x2 = c_x + (x_max - c_x) + l
    #         y2 = c_y + (x_max - c_x) + l
    #         self.add_line((x1, y1), (x1, y2), 'CONTOUR_LINE')
    #         self.add_line((x1, y2), (x2, y2), 'CONTOUR_LINE')
    #         self.add_line((x2, y2), (x2, y1), 'CONTOUR_LINE')
    #         self.add_line((x2, y1), (x1, y1), 'CONTOUR_LINE')
    #     else:
    #         x1 = c_x - (y_max - c_y) - l
    #         y1 = c_y - (y_max - c_y) - l
    #         x2 = c_x + (y_max - c_y) + l
    #         y2 = c_y + (y_max - c_y) + l
    #         self.add_line((x1, y1), (x1, y2), 'CONTOUR_LINE')
    #         self.add_line((x1, y2), (x2, y2), 'CONTOUR_LINE')
    #         self.add_line((x2, y2), (x2, y1), 'CONTOUR_LINE')
    #         self.add_line((x2, y1), (x1, y1), 'CONTOUR_LINE')






    def draw_random_dimension(self):

        point = []; x_point = []; y_point = []
        if len(self.json_object.get('line')) != 0:
            for i in range(len(self.json_object.get('line'))):
                x1 = self.json_object.get('line')[i].get('start_x')
                y1 = self.json_object.get('line')[i].get('start_y')
                x2 = self.json_object.get('line')[i].get('end_x')
                y2 = self.json_object.get('line')[i].get('end_y')
                x_point.append(x1); x_point.append(x2)
                y_point.append(y1); y_point.append(y2)
                point.append((x1,y1)); point.append((x2,y2))

        if len(self.json_object.get('circle')) != 0:
            for i in range(len(self.json_object.get('circle'))):
                x1 = self.json_object.get('circle')[i].get('center_x')
                y1 = self.json_object.get('circle')[i].get('center_y')
                x_point.append(x1); y_point.append(y1)
                point.append((x1,y1))

        ## boundary of points
        x_min = min(x_point); x_max = max(x_point)
        y_min = min(y_point); y_max = max(y_point)

        ## get random pairs of points
        point = list(dict.fromkeys(point))
        pairs = list(itertools.combinations(point, 2))
        random.shuffle(pairs)

        ## Get random number of linear dimensions
        # num = len(self.json_object.get('linear_dimension'))
        # percentage = 1 + random.uniform(-0.2, 0.2)
        # random_num = int(num * percentage)

        random_num = len(self.json_object.get('linear_dimension'))
        x_set = set()
        y_set = set()
        count = 0
        for i in range(len(pairs)):
            if count == random_num:
                break
            

            x_1 = pairs[i][0][0]
            y_1 = pairs[i][0][1]
            x_2 = pairs[i][1][0]
            y_2 = pairs[i][1][1]

            # ### filter 处理掉穿过shape的extension line
            # if abs(x_1 - x_2) > 2 and abs(y_1 - y_2) > 2:
            #     continue


            # if abs(x_1-x_2) > (x_max-x_min)/3 and abs(y_1-y_2) > (y_max-y_min)/3:
            #     continue
            
            angle = 0; base_x = 0; base_y = 0
            p1_x = 0; p1_y = 0; p2_x = 0; p2_y = 0

            side = (-1)**random.randint(0,1)   ## -1 means dimension on the left/ bottom side; 1 means on the right/top side
            
            # side = 1

            ## horizontal cases
            if abs(x_1 - x_2) >= abs(y_1 - y_2):

                # ## determind side
                # avg_y = (y_1 + y_2) / 2
                # if abs(y_max - avg_y) >= abs(y_min - avg_y):
                #     side = -1


                if x_1 < x_2:
                    p1_x = x_1; p2_x = x_2
                    p1_y = y_1; p2_y = y_2
                else:
                    p1_x = x_2; p2_x = x_1
                    p1_y = y_2; p2_y = y_1

                if side == -1:
                    base_x = p2_x
                    # base_y = int(min(p1_y,p2_y) - (min(p1_y,p2_y) - y_min) - random.uniform(4,30))
                    base_y = int(min(p1_y,p2_y) - (min(p1_y,p2_y) - y_min) - random.uniform(-30,30))

                    # num_try = 0
                    # while base_y in y_set and num_try < 4:
                    #     num_try += 1
                    #     base_y = int(min(p1_y,p2_y) - (min(p1_y,p2_y) - y_min) - random.uniform(4,30))
                    # if num_try == 4:
                    #     continue
                    # for yp in range(base_y-4, base_y+4):
                    #     y_set.add(yp)
                else:
                    base_x = p2_x
                    base_y = int(max(p1_y,p2_y) + (y_max - max(p1_y,p2_y)) + random.uniform(-30,30))

                    # num_try = 0
                    # while base_y in y_set and num_try < 4:
                    #     num_try += 1
                    #     base_y = int(max(p1_y,p2_y) + (y_max - max(p1_y,p2_y)) + random.uniform(4,30))
                    # if num_try == 4:
                    #     continue
                    # for yp in range(base_y-4, base_y+4):
                    #     y_set.add(yp)

            else:
                # ## determind side
                # avg_x = (x_1 + x_2) / 2
                # if abs(x_max - avg_x) >= abs(x_min - avg_x):
                #     side = -1


                angle = 90
                if y_1 < y_2:
                    p1_x = x_1; p2_x = x_2
                    p1_y = y_1; p2_y = y_2
                else:
                    p1_x = x_2; p2_x = x_1
                    p1_y = y_2; p2_y = y_1

                if side == -1:
                    base_y = p2_y
                    base_x = int(min(p1_x,p2_x) - (min(p1_x,p2_x) - x_min) - random.uniform(-30,30))

                    # num_try = 0
                    # while base_x in x_set and num_try < 4:
                    #     num_try += 1
                    #     base_x = int(min(p1_x,p2_x) - (min(p1_x,p2_x) - x_min) - random.uniform(4,30))
                    # if num_try == 4:
                    #     continue
                    # for xp in range(base_x-4, base_x+4):
                    #     x_set.add(xp)
                else:
                    base_y = p2_y
                    base_x = int(max(p1_x,p2_x) + (x_max - max(p1_x,p2_x)) + random.uniform(-30,30))

                    # num_try = 0
                    # while base_x in x_set and num_try < 4:
                    #     num_try += 1
                    #     base_x = int(max(p1_x,p2_x) + (x_max - max(p1_x,p2_x)) + random.uniform(4,30))
                    # if num_try == 4:
                    #     continue
                    # for xp in range(base_x-4, base_x+4):
                    #     x_set.add(xp)


            self.add_linear_dimension((base_x, base_y), (p1_x, p1_y),
                                            (p2_x, p2_y), angle)
            count += 1



        if len(self.json_object.get('diameter_dimension')) != 0:
            circle_num = len(self.json_object.get('diameter_dimension'))
            circle = []
            for i in range(len(self.json_object.get('circle'))):
                x_c = self.json_object.get('circle')[i].get('center_x')
                y_c = self.json_object.get('circle')[i].get('center_y')
                radius = self.json_object.get('circle')[i].get('radius')
                circle.append((x_c, y_c, radius))

            for i in range(len(self.json_object.get('arc'))):
                x_c = self.json_object.get('arc')[i].get('center_x')
                y_c = self.json_object.get('arc')[i].get('center_y')
                radius = self.json_object.get('arc')[i].get('radius')
                circle.append((x_c, y_c, radius))

            random.shuffle(circle)

            center_seen = set()
            for i in range(circle_num):
                center_x = circle[i][0]; center_y = circle[i][1]; radius = circle[i][2]
                cur_center = (int(center_x), int(center_y))
                if cur_center in center_seen:
                    continue
                else:
                    center_seen.add(cur_center)
                l_x = -1
                l_y = -1
                dist_x_max = abs(x_max - center_x)
                dist_x_min = abs(x_min - center_x)
                dist_y_max = abs(y_max - center_y)
                dist_y_min = abs(y_min - center_y)

                min_dist = min(dist_x_max, dist_x_min, dist_y_max, dist_y_min)
                if dist_x_max <= dist_x_min:
                    delta = min_dist
                    delta = delta + 10
                    l_x = int(center_x + delta)
                    if dist_y_max < dist_y_min:
                        l_y = int(center_y + delta)
                    else:
                        l_y = int(center_y - delta)
                    while l_x in x_set or l_y in y_set:
                        l_x += 2
                        if dist_y_max < dist_y_min:
                            l_y += 2
                        else:
                            l_y -= 2
                    for xp in range(l_x-3, l_x+3):
                        x_set.add(xp)
                    for yp in range(l_y-3, l_y+3):
                        y_set.add(yp)
                else:
                    delta = min_dist
                    delta = delta + 10
                    l_x = int(center_x - delta)
                    if dist_y_max < dist_y_min:
                        l_y = int(center_y + delta)
                    else:
                        l_y = int(center_y - delta)
                    while l_x in x_set or l_y in y_set:
                        l_x -= 2
                        if dist_y_max < dist_y_min:
                            l_y += 2
                        else:
                            l_y -= 2
                    for xp in range(l_x-3, l_x+3):
                        x_set.add(xp)
                    for yp in range(l_y-3, l_y+3):
                        y_set.add(yp)





                # if abs(center_x - x_min) < abs(center_x - x_max):
                #     l_x = int(x_min - random.uniform(2,30))
                #     num_try = 0
                #     while l_x in x_set and num_try < 4:
                #         num_try += 1
                #         l_x = int(x_min - random.uniform(2,30))
                #     if num_try == 4:
                #         continue
                #     for xp in range(l_x-3, l_x+3):
                #         x_set.add(xp)
                # else:
                #     l_x = int(x_max + random.uniform(2,30))
                #     num_try = 0
                #     while l_x in x_set and num_try < 4:
                #         num_try += 1
                #         l_x = int(x_max + random.uniform(2,30))
                #     if num_try == 4:
                #         continue
                #     for xp in range(l_x-3, l_x+3):
                #         x_set.add(xp)

                # if abs(center_y - y_min) < abs(center_y - y_max):
                #     l_y = int(y_min - random.uniform(2,30))
                #     num_try = 0
                #     while l_y in y_set and num_try < 4:
                #         num_try += 1
                #         l_y = int(y_min - random.uniform(2,30))
                #     if num_try == 4:
                #         continue
                #     for yp in range(l_y-3, l_y+3):
                #         y_set.add(yp)
                # else:
                #     l_y = int(y_max + random.uniform(2,30))
                #     num_try = 0
                #     while l_y in y_set and num_try < 4:
                #         num_try += 1
                #         l_y = int(y_max + random.uniform(2,30))
                #     if num_try == 4:
                #         continue
                #     for yp in range(l_y-3, l_y+3):
                #         y_set.add(yp)



                self.add_diameter_dimension((center_x, center_y), radius,
                                            (l_x, l_y))



def coordinate_transform(old_x, old_y, size_y):
    """
    Function works to perform coordinates transformation between
    coordinates with left-bottom corner as origin and
    coordinates with left-upper corner as origin.
    :param old_x: horizontal coordinate.
    :param old_y: vertical coordinate.
    :param size_y: vertical height of the image.
    :return: new_x: the new horizontal coordinate; new_y the new vertical coordinate.
    """
    new_x = x
    new_y = abs(size_y - y)
    return new_x, new_y

#
# if __name__ == "__main__":
#     stream1 = streamIO(filename='./ground_truth/0716/0716.DXF')
#     stream1.load_doc()
#     file_name = './ground_truth/0716/0716.json'
#
#     stream = AddEntity(stream1,file_name)
#
#     stream.draw_contour()
#     stream.draw_dimension()
#     stream1.saveDXF()