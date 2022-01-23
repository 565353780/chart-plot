#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random
import numpy as np

from LineMethod.point import Point

class Line(object):
    def __init__(self, line_idx):
        self.line_idx = line_idx

        self.line_type = "g-"
        self.line_width = 2
        self.label = str(self.line_idx)

        self.point_list = []

        self.fit_polyline = False

        self.show_confidence_interval = False
        self.confidence_diff_min = 0.5
        self.confidence_diff_max = 1.0
        self.confidence_interval_list = []
        return

    def reset(self):
        self.point_list.clear()
        return True

    def addPoint(self, x, y):
        new_point = Point(x, y)

        if len(self.point_list) == 0:
            self.point_list.append(new_point)
            return True

        for i in range(len(self.point_list)):
            search_point_x = self.point_list[i].x
            if search_point_x == x:
                self.point_list[i].y = y
                return True

            if search_point_x < x:
                continue

            self.point_list.insert(i, new_point)
            return True

        self.point_list.append(new_point)
        return True

    def setPoint(self, point_idx, x, y):
        if point_idx >= len(self.point_list):
            print("Line::setPoint :")
            print("point_idx out of range!")
            return False

        self.point_list.pop(point_idx)
        return self.addPoint(x, y)

    def getXYList(self):
        x_list = []
        y_list = []

        if len(self.point_list) == 0:
            return x_list, y_list

        for point in self.point_list:
            x_list.append(point.x)
            y_list.append(point.y)

        if self.fit_polyline:
            poly_sample_num = 100
            poly_function = np.poly1d(np.polyfit(x_list, y_list, 6))
            x_min = self.point_list[0].x
            x_max = self.point_list[len(self.point_list) - 1].x
            delta_x_diff = 1.0 * (x_max - x_min) / poly_sample_num
            x_list.clear()
            y_list.clear()
            for i in range(100):
                current_x = x_min + i * delta_x_diff
                x_list.append(current_x)
                y_list.append(poly_function(current_x))
            return x_list, y_list
        return x_list, y_list

    def getBBoxXYXY(self):
        x_min = None
        y_min = None
        x_max = None
        y_max = None

        if len(self.point_list) == 0:
            return x_min, y_min, x_max, y_max

        x_min = self.point_list[0].x
        y_min = self.point_list[0].y
        x_max = x_min
        y_max = y_min

        for point in self.point_list:
            x_min = min(x_min, point.x)
            y_min = min(y_min, point.y)
            x_max = max(x_max, point.x)
            y_max = max(y_max, point.y)
        return x_min, y_min, x_max, y_max

    def getXYRange(self):
        x_min, y_min, x_max, y_max = self.getBBoxXYXY()
        if x_min is None:
            return 0, 0
        return x_max - x_min, y_max - y_min

    def getNearestPointIdx(self, x, y):
        nearest_point_idx = -1
        if len(self.point_list) == 0:
            return nearest_point_idx
        nearest_point_dist2 = None
        for i in range(len(self.point_list)):
            current_x_diff = self.point_list[i].x - x
            current_y_diff = self.point_list[i].y - y
            current_point_dist2 = \
                current_x_diff * current_x_diff +\
                current_y_diff * current_y_diff
            if nearest_point_dist2 is None:
                nearest_point_idx = i
                nearest_point_dist2 = current_point_dist2
                continue
            if current_point_dist2 < nearest_point_dist2:
                nearest_point_idx = i
                nearest_point_dist2 = current_point_dist2
        return nearest_point_idx

    def updateConfidenceInterval(self):
        self.confidence_interval_list.clear()
        for _ in self.point_list:
            confidence_diff = random() * (self.confidence_diff_max - self.confidence_diff_min)
            self.confidence_interval_list.append(
                self.confidence_diff_min + confidence_diff)
        return True

    def getPointData(self):
        point_data = []
        for point in self.point_list:
            point_data.append([point.x, point.y])
        return point_data

    def loadPointData(self, point_data):
        self.point_list.clear()
        for point in point_data:
            new_point = Point(point[0], point[1])
            self.point_list.append(new_point)
        return True

