#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
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
        self.point_list.append(new_point)
        return True

    def getLine(self):
        line_x_list = []
        line_y_list = []

        y_list = []
        for i in range(len(self.x_list)):
            y_list.append(None)
        for point in self.point_list:
            y_list[point.x_idx] = point.y_value

        for i in range(len(y_list)):
            if y_list[i] is None:
                continue
            line_x_list.append(self.x_list[i])
            line_y_list.append(y_list[i])
        return line_x_list, line_y_list

class ChartPlot:
    def __init__(self):
        self.line_list = []
        return

    def reset(self):
        self.line_list.clear()
        return True

    def addLine(self, x_start, x_num, x_step, line_type, line_width, label):
        new_line = Line(len(self.line_list))
        if not new_line.setLineProperty(line_type, line_width, label):
            print("ChartPlot::addLine :")
            print("setLineProperty for line " + str(new_line.line_idx) + " failed!")
            return False

        if not new_line.setXRange(x_start, x_num, x_step):
            print("ChartPlot::addLine :")
            print("setXRange for line " + str(new_line.line_idx) + " failed!")
            return False

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
        return True

    def render(self):
        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()
        while True:
            plt.cla()

            plt.title("ChartPlot Render")
            plt.xlabel("x label")
            plt.ylabel("y label")

            for line in self.line_list:
                line_x_list, line_y_list = line.getLine()
                plt.plot(line_x_list, line_y_list, line.line_type, linewidth=line.line_width, label=line.label)

            # position can be : upper lower left right center
            plt.legend(loc="upper right", shadow=True)
            plt.pause(0.1)

            input_key = getch()
            if input_key == "q":
                plt.ioff()
                break
        return True

if __name__ == "__main__":
    yy = [1,2,3,4,5,2,3,7,4,3,9,2]
    xx = [3,6,4,8,2,6,9,4,5,8,1,7]
    zz = [5,6,8,1,3,4,9,1,3,4,8,1]
    x_start = 0
    x_num = len(yy)
    x_step = 1

    chart_plot = ChartPlot()
    chart_plot.addLine(x_start, x_num, x_step, "r:", 5, "Data 1")
    chart_plot.addLine(x_start, x_num, x_step, "g--", 2, "Data 2")
    chart_plot.addLine(x_start, x_num, x_step, "b-", 0.5, "Data 3")
    for i in range(len(yy)):
        chart_plot.addPoint(0, i, yy[i])
    for i in range(len(xx)):
        chart_plot.addPoint(1, i, xx[i])
    for i in range(len(zz)):
        chart_plot.addPoint(2, i, zz[i])

    chart_plot.render()

