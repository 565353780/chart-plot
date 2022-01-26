#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from LineMethod.line_manager import LineManager

class LineRenderer(LineManager):
    def __init__(self):
        LineManager.__init__(self)
        return

    def renderFrame(self):
        if len(self.line_list) == 0:
           print("LineRenderer::renderLine :")
           print("no lines to render!")
           return True

        plt.cla()

        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)

        for line in self.line_list:
            x_list, y_list = line.getXYList()
            if self.show_line_label:
                plt.plot(
                    x_list, y_list,
                    line.line_type, color=line.line_color, linewidth=line.line_width,
                    label=line.label, marker=self.marker)
            else:
                plt.plot(
                    x_list, y_list,
                    line.line_type, color=line.line_color, linewidth=line.line_width,
                    marker=self.marker)
            if line.show_confidence_interval:
                confidence_interval_x_list = []
                up_confidence_interval_y_list = []
                down_confidence_interval_y_list = []
                for i in range(len(line.point_list)):
                    confidence_interval_x_list.append(line.point_list[i].x)
                    up_confidence_interval_y_list.append(
                        line.point_list[i].y + line.confidence_interval_list[i])
                    down_confidence_interval_y_list.append(
                        line.point_list[i].y - line.confidence_interval_list[i])
                if self.show_confidence_interval_label:
                    plt.fill_between(
                        confidence_interval_x_list,
                        up_confidence_interval_y_list,
                        down_confidence_interval_y_list,
                        alpha=self.fill_alpha,
                        color=line.line_color,
                        label=line.label + " Confidence Interval")
                else:
                    plt.fill_between(
                        confidence_interval_x_list,
                        up_confidence_interval_y_list,
                        down_confidence_interval_y_list,
                        alpha=self.fill_alpha,
                        color=line.line_color)

        if self.show_line_label or self.show_confidence_interval_label:
            # position can be : upper lower left right center
            plt.legend(loc="lower right", shadow=True)
        return True

    def renderLine(self, show_line_label, show_confidence_interval_label):
        self.show_line_label = show_line_label
        self.show_confidence_interval_label = show_confidence_interval_label

        plt.figure(figsize=(self.fig_size[0], self.fig_size[1]), dpi=self.dpi)
        plt.ion()

        while True:
            self.renderFrame()
            plt.pause(0.001)

def demo():
    xx = [1,2,3,4,5,2,3,7,4,3,9,2]
    yy = [3,6,4,8,2,6,9,4,5,8,1,7]
    zz = [5,6,8,1,3,4,9,1,3,4,8,1]
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 0.5
    confidence_diff_max = 1.0
    show_line_label = True
    show_confidence_interval_label = False

    line_renderer = LineRenderer()

    line_renderer.show_line_label = show_line_label
    line_renderer.show_confidence_interval_label = show_confidence_interval_label

    line_renderer.addLine(
        "r:", 5, "Data 1", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(yy)):
        line_renderer.line_list[0].addPoint(i, xx[i])

    line_renderer.addLine(
        "g--", 2, "Data 2", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(xx)):
        line_renderer.line_list[1].addPoint(i, yy[i])

    line_renderer.addLine(
        "b-", 0.5, "Data 3", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(zz)):
        line_renderer.line_list[2].addPoint(i, zz[i])

    line_renderer.renderLine(show_line_label, show_confidence_interval_label)
    return True

if __name__ == "__main__":
    demo()

