#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
import matplotlib.pyplot as plt

from LineMethod.line_renderer import LineRenderer

class LineEditor(LineRenderer):
    def __init__(self):
        LineRenderer.__init__(self)
        return

    def editLine(self, show_line_label, show_confidence_interval_label):
        self.show_line_label = show_line_label
        self.show_confidence_interval_label = show_confidence_interval_label

        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()

        edit_line_idx = 0
        edit_point_idx = 0
        while True:
            self.renderFrame()

            edit_x_idx = self.line_list[edit_line_idx].point_list[edit_point_idx].x_idx
            edit_x_value = self.line_list[edit_line_idx].x_list[edit_x_idx]
            edit_y_value = self.line_list[edit_line_idx].point_list[edit_point_idx].y_value
            plt.plot([edit_x_value], [edit_y_value], "bo", linewidth=20, label="EDIT")

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

