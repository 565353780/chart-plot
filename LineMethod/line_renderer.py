#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
import matplotlib.pyplot as plt

from LineMethod.line_manager import LineManager

class LineRenderer(LineManager):
    def __init__(self):
        LineManager.__init__(self)
        return

    def renderLine(self, show_line_label, show_confidence_interval_label):
        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()

        if len(self.line_list) == 0:
           print("LineRenderer::renderLine :")
           print("no lines to render!")
           return True

        edit_line_idx = 0
        edit_point_idx = 0
        while True:
            plt.cla()

            plt.title("LineRenderer")
            plt.xlabel("x label")
            plt.ylabel("y label")

            for line in self.line_list:
                line.updateYValue()
                if show_line_label:
                    plt.plot(
                        line.x_list, line.y_list,
                        line.line_type, linewidth=line.line_width,
                        label=line.label)
                else:
                    plt.plot(
                        line.x_list, line.y_list,
                        line.line_type, linewidth=line.line_width)
                if line.show_confidence_interval:
                    up_confidence_interval_y_list = []
                    down_confidence_interval_y_list = []
                    for i in range(len(line.point_list)):
                        up_confidence_interval_y_list.append(
                            line.point_list[i].y_value + line.confidence_interval_list[i])
                        down_confidence_interval_y_list.append(
                            line.point_list[i].y_value - line.confidence_interval_list[i])
                    if show_confidence_interval_label:
                        plt.fill_between(
                            line.x_list,
                            up_confidence_interval_y_list,
                            down_confidence_interval_y_list,
                            alpha=0.5,
                            label="Data " + str(line.line_idx + 1) + " Confidence Interval")
                    else:
                        plt.fill_between(
                            line.x_list,
                            up_confidence_interval_y_list,
                            down_confidence_interval_y_list,
                            alpha=0.5)

            edit_x_idx = self.line_list[edit_line_idx].point_list[edit_point_idx].x_idx
            edit_x_value = self.line_list[edit_line_idx].x_list[edit_x_idx]
            edit_y_value = self.line_list[edit_line_idx].point_list[edit_point_idx].y_value
            plt.plot([edit_x_value], [edit_y_value], "bo", linewidth=20, label="EDIT")

            # position can be : upper lower left right center
            plt.legend(loc="upper right", shadow=True)
            plt.pause(0.1)

            y_range = self.getYRange()

            input_key = getch()
            if input_key == "q":
                plt.ioff()
                break
            if input_key == "h":
                edit_point_idx = max(edit_point_idx - 1, 0)
            elif input_key == "l":
                edit_point_idx = min(edit_point_idx + 1, len(self.line_list[edit_line_idx].point_list) - 1)
            elif input_key == "j":
                self.line_list[edit_line_idx].point_list[edit_point_idx].y_value -= 0.01 * y_range
                self.line_list[edit_line_idx].updateYValue()
            elif input_key == "k":
                self.line_list[edit_line_idx].point_list[edit_point_idx].y_value += 0.01 * y_range
                self.line_list[edit_line_idx].updateYValue()
            elif input_key == "J":
                self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] = max(
                    self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] - 0.01 * y_range, 0)
            elif input_key == "K":
                self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] += 0.01 * y_range
            elif input_key == "n":
                edit_line_idx = min(edit_line_idx + 1, len(self.line_list) - 1)
            elif input_key == "p":
                edit_line_idx = max(edit_line_idx - 1, 0)
            elif input_key == "u":
                self.line_list[edit_line_idx].updateConfidenceInterval()
        return True

if __name__ == "__main__":
    xx = [1,2,3,4,5,2,3,7,4,3,9,2]
    yy = [3,6,4,8,2,6,9,4,5,8,1,7]
    zz = [5,6,8,1,3,4,9,1,3,4,8,1]
    x_start = 0
    x_num = len(xx)
    x_step = 1
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 0.5
    confidence_diff_max = 1.0
    show_line_label = True
    show_confidence_interval_label = False

    line_renderer = LineRenderer()

    line_renderer.addLine(
        x_start, x_num, x_step,
        "r:", 5, "Data 1", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(yy)):
        line_renderer.addPoint(0, i, xx[i])

    line_renderer.addLine(
        x_start, x_num, x_step,
        "g--", 2, "Data 2", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(xx)):
        line_renderer.addPoint(1, i, yy[i])

    line_renderer.addLine(
        x_start, x_num, x_step,
        "b-", 0.5, "Data 3", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(zz)):
        line_renderer.addPoint(2, i, zz[i])

    line_renderer.renderLine(show_line_label, show_confidence_interval_label)

