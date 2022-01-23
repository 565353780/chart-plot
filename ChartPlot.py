#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
from random import random
import numpy as np
import matplotlib.pyplot as plt

class LinePoint:
    def __init__(self, x_idx, y_value):
        self.x_idx = x_idx
        self.y_value = y_value
        return

class Line:
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
        self.up_confidence_interval_y_list = []
        self.down_confidence_interval_y_list = []
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
        self.up_confidence_interval_y_list.clear()
        self.down_confidence_interval_y_list.clear()
        for point in self.point_list:
            confidence_diff = random() * (self.confidence_diff_max - self.confidence_diff_min)
            self.up_confidence_interval_y_list.append(
                point.y_value + self.confidence_diff_min + confidence_diff)
            self.down_confidence_interval_y_list.append(
                point.y_value - self.confidence_diff_min - confidence_diff)
        return True

class ChartPlot:
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
            print("ChartPlot::addLine :")
            print("setLineProperty for line " + str(new_line.line_idx) + " failed!")
            return False

        if not new_line.setXRange(x_start, x_num, x_step):
            print("ChartPlot::addLine :")
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
            print("ChartPlot::setXRange :")
            print("line_idx out of range!")
            return False

        if not self.line_list[line_idx].setXRange(x_start, x_num, x_step):
            print("ChartPlot::setXRange :")
            print("setXRange for line " + str(line_idx) + " failed!")
            return False
        return True

    def addPoint(self, line_idx, x_idx, y_value):
        if line_idx >= len(self.line_list):
            print("ChartPlot::addPoint :")
            print("line_idx out of range!")
            return False

        if not self.line_list[line_idx].addPoint(x_idx, y_value):
            print("ChartPlot::addPoint :")
            print("addPoint for line " + str(line_idx) + " failed!")
            return False

        if self.line_list[line_idx].show_confidence_interval:
            if not self.line_list[line_idx].updateConfidenceInterval():
                print("ChartPlot::addLine :")
                print("updateConfidenceInterval for line " + str(line_idx) + " failed!")
                return False
        return True

    def renderLine(self):
        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()

        if len(self.line_list) == 0:
               print("ChartPlot::renderLine :")
               print("no lines to render!")
               return True

        edit_line_idx = 0
        edit_point_idx = 0
        while True:
            plt.cla()

            plt.title("ChartPlot Render")
            plt.xlabel("x label")
            plt.ylabel("y label")

            for line in self.line_list:
                line.updateYValue()
                plt.plot(line.x_list, line.y_list, line.line_type, linewidth=line.line_width, label=line.label)
                if line.show_confidence_interval:
                    plt.fill_between(
                        line.x_list,
                        line.up_confidence_interval_y_list,
                        line.down_confidence_interval_y_list,
                        alpha=0.5,
                        label="Data " + str(line.line_idx) + " Confidence Interval"
                    )

            edit_x_idx = self.line_list[edit_line_idx].point_list[edit_point_idx].x_idx
            edit_x_value = self.line_list[edit_line_idx].x_list[edit_x_idx]
            edit_y_value = self.line_list[edit_line_idx].point_list[edit_point_idx].y_value
            plt.plot([edit_x_value], [edit_y_value], "bo", linewidth=20, label="EDIT")

            # position can be : upper lower left right center
            plt.legend(loc="upper right", shadow=True)
            plt.pause(0.1)

            input_key = getch()
            if input_key == "q":
                plt.ioff()
                break
            if input_key == "h":
                edit_point_idx = max(0, edit_point_idx - 1)
            elif input_key == "l":
                edit_point_idx = min(len(self.line_list[edit_line_idx].point_list) - 1, edit_point_idx + 1)
            elif input_key == "j":
                self.line_list[edit_line_idx].point_list[edit_point_idx].y_value -= 0.1
                self.line_list[edit_line_idx].updateYValue()
                self.line_list[edit_line_idx].updateConfidenceInterval()
            elif input_key == "k":
                self.line_list[edit_line_idx].point_list[edit_point_idx].y_value += 0.1
                self.line_list[edit_line_idx].updateYValue()
                self.line_list[edit_line_idx].updateConfidenceInterval()
            elif input_key == "u":
                self.line_list[edit_line_idx].updateConfidenceInterval()
        return True

if __name__ == "__main__":
    xx = [1,2,3,4,5,2,3,7,4,3,9,2]
    yy = [3,6,4,8,2,6,9,4,5,8,1,7]
    zz = [5,6,8,1,3,4,9,1,3,4,8,1]
    x_start = 0
    x_num = len(yy)
    x_step = 1
    fit_polyline = False
    show_confidence_interval = False

    chart_plot = ChartPlot()

    chart_plot.addLine(
        x_start, x_num, x_step,
        "r:", 5, "Data 1", fit_polyline,
        show_confidence_interval, 0.8, 1.0)
    for i in range(len(yy)):
        chart_plot.addPoint(0, i, xx[i])

    chart_plot.addLine(
        x_start, x_num, x_step,
        "g--", 2, "Data 2",fit_polyline,
        show_confidence_interval, 0.8, 1.0)
    for i in range(len(xx)):
        chart_plot.addPoint(1, i, yy[i])

    chart_plot.addLine(
        x_start, x_num, x_step,
        "b-", 0.5, "Data 3", fit_polyline,
        show_confidence_interval, 0.8, 1.0)
    for i in range(len(zz)):
        chart_plot.addPoint(2, i, zz[i])

    chart_plot.renderLine()

