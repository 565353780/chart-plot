#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
import matplotlib.pyplot as plt

class ChartPlot:
    def __init__(self):
        self.x_list = []
        self.y_list = []
        self.fixed_point_list = []
        return

    def reset(self):
        self.x_list.clear()
        self.y_list.clear()
        self.fixed_point_list.clear()
        return True

    def setXRange(self, x_start, x_num, x_step):
        self.reset()

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
        while True:
            input_key = getch()
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

    print(chart_plot.x_list)
    print(chart_plot.y_list)

    plt.plot(yy, color='r', linewidth=5, linestyle=':', label='Data 1')
    plt.plot(xx, color='g', linewidth=2, linestyle='--', label='Data 2')
    plt.plot(zz, color='b', linewidth=0.5, linestyle='-', label='Data 3')
    plt.legend(loc=2)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('title')
    plt.ylim(0,10)
    plt.show()

