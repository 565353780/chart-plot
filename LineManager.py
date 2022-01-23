#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random
import numpy as np

class LinePoint(object):
    def __init__(self, x_idx, y_value):
        self.x_idx = x_idx
        self.y_value = y_value
        return

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

class LineManager(object):
    def __init__(self):
        self.line_list = []
        return

    def reset(self):
        self.line_list.clear()
        return True

    def addLine(self,
                x_start,
                x_num,
                x_step,
                line_type,
                line_width,
                label,
                fit_polyline,
                show_confidence_interval,
                confidence_diff_min,
                confidence_diff_max):
        new_line = Line(len(self.line_list))
        if not new_line.setLineProperty(line_type, line_width, label):
            print("LineManager::addLine :")
            print("setLineProperty for line " + str(new_line.line_idx) + " failed!")
            return False

        if not new_line.setXRange(x_start, x_num, x_step):
            print("LineManager::addLine :")
            print("setXRange for line " + str(new_line.line_idx) + " failed!")
            return False

        new_line.fit_polyline = fit_polyline
        new_line.show_confidence_interval = show_confidence_interval
        new_line.confidence_diff_min = confidence_diff_min
        new_line.confidence_diff_max = confidence_diff_max

        self.line_list.append(new_line)
        return True

    def setXRange(self, line_idx, x_start, x_num, x_step):
        if line_idx >= len(self.line_list):
            print("LineManager::setXRange :")
            print("line_idx out of range!")
            return False

        if not self.line_list[line_idx].setXRange(x_start, x_num, x_step):
            print("LineManager::setXRange :")
            print("setXRange for line " + str(line_idx) + " failed!")
            return False
        return True

    def addPoint(self, line_idx, x_idx, y_value):
        if line_idx >= len(self.line_list):
            print("LineManager::addPoint :")
            print("line_idx out of range!")
            return False

        if not self.line_list[line_idx].addPoint(x_idx, y_value):
            print("LineManager::addPoint :")
            print("addPoint for line " + str(line_idx) + " failed!")
            return False

        if self.line_list[line_idx].show_confidence_interval:
            if not self.line_list[line_idx].updateConfidenceInterval():
                print("LineManager::addLine :")
                print("updateConfidenceInterval for line " + str(line_idx) + " failed!")
                return False
        return True

    def getYRange(self):
        y_min = 0
        y_max = 0

        if len(self.line_list) == 0:
            return y_max - y_min

        y_min = min(self.line_list[0].y_list)
        y_max = max(self.line_list[0].y_list)

        for line in self.line_list:
            y_min = min(y_min, min(line.y_list))
            y_max = max(y_max, max(line.y_list))
        return y_max - y_min

