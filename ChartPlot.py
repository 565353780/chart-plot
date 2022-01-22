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
    def __init__(self, line_idx, x_start, x_num, x_step):
        self.line_idx = line_idx
        self.x_list = x_start
        self.point_list = []
        return

    def reset(self):
        self.point_list.clear()
        return True

    def addPoint(self, point):
        self.point_list.append(point)
        return True

class ChartPlot:
    def __init__(self):
        self.line_list = []
        return

    def reset(self):
        self.line_list.clear()
        return True

    def addLine(self, x_start, x_num, x_step):
        new_line = Line(len(self.line_list))
        new_x = x_start
        for i in range(x_num):
            new_point = LinePoint(new_x, )
            self.x_list.append(new_x)
            self.y_list.append(None)
            new_x += x_step
        return True

    def setXRange(self, line_idx, x_start, x_num, x_step):
        new_x = x_start
        for _ in range(x_num):
            self.x_list.append(new_x)
            self.y_list.append(None)
            new_x += x_step
        return True

    def setYValue(self, x_idx, y_value):
        if x_idx >= len(self.x_list):
            print("ChartPlot::setYValue :")
            print("x_idx out of range!")
            return False

        self.y_list[x_idx] = y_value
        return True

    def addFixedPoint(self, x_idx, y_value):
        if x_idx >= len(self.x_list):
            print("ChartPlot::addFixedPoint :")
            print("x_idx out of range!")
            return False

        self.fixed_point_list.append([x_idx, y_value])
        return True

    def render(self):
        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()
        while True:
            plt.cla()

            plt.title("ChartPlot Render")
            plt.xlabel("x label")
            plt.ylabel("y label")

            plt.plot(self.x_list, self.y_list, "r-", linewidth=2.0, label="line 1 label")

            # position can be : upper lower left right center
            plt.legend(loc="upper left", shadow=True)
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
    chart_plot.setXRange(x_start, x_num, x_step)
    for i in range(len(yy)):
        chart_plot.setYValue(i, yy[i])

    chart_plot.render()

    plt.plot(yy, color='r', linewidth=5, linestyle=':', label='Data 1')
    plt.plot(xx, color='g', linewidth=2, linestyle='--', label='Data 2')
    plt.plot(zz, color='b', linewidth=0.5, linestyle='-', label='Data 3')
    plt.legend(loc=2)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('title')
    plt.ylim(0,10)
    plt.show()

