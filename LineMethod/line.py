#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random
import numpy as np

from LineMethod.line_point import LinePoint

class Line(object):
    def __init__(self, line_idx):
        self.line_idx = line_idx

        self.line_type = "g-"
        self.line_width = 2
        self.label = str(self.line_idx)

        self.x_list = []
        self.point_list = []
        self.y_list = []

        self.fit_polyline = False

        self.show_confidence_interval = False
        self.confidence_diff_min = 0.5
        self.confidence_diff_max = 1.0
        self.confidence_interval_list = []
        return

    def reset(self):
        self.x_list.clear()
        self.point_list.clear()
        return True

    def setLineProperty(self, line_type, line_width, label):
        self.line_type = line_type
        self.line_width = line_width
        self.label = label
        return True

    def setXRange(self, x_start, x_num, x_step):
        new_x = x_start
        for _ in range(x_num):
            self.x_list.append(new_x)
            new_x += x_step
        return True

    def addPoint(self, x_idx, y_value):
        if x_idx >= len(self.x_list):
            print("Line::addPoint :")
            print("x_idx out of range!")
            return False

        new_point = LinePoint(x_idx, y_value)

        if len(self.point_list) == 0:
            self.point_list.append(new_point)
            return True

        for i in range(len(self.point_list)):
            search_x_idx = self.point_list[i].x_idx
            if search_x_idx < x_idx:
                continue
            if search_x_idx == x_idx:
                print("Line::addPoint :")
                print("point at x_idx = " + str(x_idx) + " already exist")
                return False

            self.point_list.insert(i, new_point)
            return True

        self.point_list.append(new_point)
        return True

    def updateYValue(self):
        self.y_list.clear()

        if len(self.point_list) == 0:
            return True

        if len(self.point_list) == 1:
            for _ in self.x_list:
                self.y_list.append(self.point_list[0].y_value)
            return True

        point_idx_list = []
        point_x_value_list = []
        point_y_value_list = []

        if self.point_list[0].x_idx != 0:
            first_point = self.point_list[0]
            second_point = self.point_list[1]
            x_diff = self.x_list[second_point.x_idx] - self.x_list[first_point.x_idx]
            y_diff = second_point.y_value - first_point.y_value
            line_tan = 1.0 * y_diff / x_diff
            point_idx_list.append(0)
            point_x_value_list.append(self.x_list[0])
            point_y_value_list.append(first_point.y_value - self.x_list[first_point.x_idx] * line_tan)

        for point in self.point_list:
            point_idx_list.append(point.x_idx)
            point_x_value_list.append(self.x_list[point.x_idx])
            point_y_value_list.append(point.y_value)

        point_list_back_idx = len(self.point_list) - 1
        x_list_back_idx = len(self.x_list) - 1
        if self.point_list[point_list_back_idx].x_idx != x_list_back_idx:
            first_point = self.point_list[point_list_back_idx]
            second_point = self.point_list[point_list_back_idx - 1]
            x_diff = self.x_list[second_point.x_idx] - self.x_list[first_point.x_idx]
            y_diff = second_point.y_value - first_point.y_value
            line_tan = 1.0 * y_diff / x_diff
            point_idx_list.append(x_list_back_idx)
            point_x_value_list.append(self.x_list[x_list_back_idx])
            point_y_value_list.append(
                first_point.y_value + (self.x_list[x_list_back_idx] - self.x_list[first_point.x_idx]) * line_tan)

        if self.fit_polyline:
            poly_function = np.poly1d(np.polyfit(point_x_value_list, point_y_value_list, 6))
            for x_value in self.x_list:
                self.y_list.append(poly_function(x_value))
            return True

        for i in range(len(point_idx_list) - 1):
            current_point_x_value = point_x_value_list[i]
            current_point_y_value = point_y_value_list[i]
            next_point_x_value = point_x_value_list[i + 1]
            next_point_y_value = point_y_value_list[i + 1]
            current_x_diff = next_point_x_value - current_point_x_value
            current_y_diff = next_point_y_value - current_point_y_value
            current_tan = 1.0 * current_y_diff / current_x_diff
            idx_diff = point_idx_list[i + 1] - point_idx_list[i]
            for j in range(idx_diff):
                self.y_list.append(current_point_y_value + j * current_tan)
            if i == len(point_idx_list) - 2:
                self.y_list.append(current_point_y_value + idx_diff * current_tan)
        return True

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
            point_data.append([point.x_idx, point.y_value])
        return point_data

    def loadPointData(self, point_data):
        self.point_list.clear()
        for point in point_data:
            new_point = LinePoint(point[0], point[1])
            self.point_list.append(new_point)
        return True

