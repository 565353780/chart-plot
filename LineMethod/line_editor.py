#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
import matplotlib.pyplot as plt

from LineMethod.line_renderer import LineRenderer

class LineEditor(LineRenderer):
    def __init__(self):
        LineRenderer.__init__(self)

        self.NORMAL = "NORMAL"
        self.EDIT = "EDIT"
        self.ADD = "ADD"
        self.mode = self.NORMAL
        return

    def updateMode(self, input_key):
        if input_key == "q":
            if self.mode == self.NORMAL:
                return False
            self.mode = self.NORMAL
            return True
        if input_key == "i":
            if self.mode == self.EDIT:
                return False
            self.mode = self.EDIT
            return True
        if input_key == "a":
            if self.mode == self.ADD:
                return False
            self.mode = self.ADD
            return True
        return False

    def editLine(self, show_line_label, show_confidence_interval_label):
        self.show_line_label = show_line_label
        self.show_confidence_interval_label = show_confidence_interval_label

        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()

        edit_line_idx = 0
        edit_point_idx = 0
        edit_x = self.line_list[edit_line_idx].point_list[edit_point_idx].x
        edit_y = self.line_list[edit_line_idx].point_list[edit_point_idx].y
        while True:
            self.renderFrame()

            if self.mode != self.ADD:
                edit_x = self.line_list[edit_line_idx].point_list[edit_point_idx].x
                edit_y = self.line_list[edit_line_idx].point_list[edit_point_idx].y
            if self.mode == self.NORMAL:
                plt.plot([edit_x], [edit_y], "go", linewidth=20, label="NORMAL")
            elif self.mode == self.EDIT:
                plt.plot([edit_x], [edit_y], "bo", linewidth=20, label="EDIT")
            elif self.mode == self.ADD:
                plt.plot([edit_x], [edit_y], "ro", linewidth=20, label="ADD")

            plt.pause(0.001)

            x_range, y_range = self.getXYRange()
            if x_range == 0:
                x_range = 100
                y_range = 100

            input_key = getch()

            if self.updateMode(input_key):
                if self.mode != self.ADD:
                    edit_point_idx = \
                        self.line_list[edit_line_idx].getNearestPointIdx(edit_x, edit_y)
                continue

            if input_key == "x":
                plt.ioff()
                break

            if input_key == "u":
                self.line_list[edit_line_idx].updateConfidenceInterval()
                continue
            if input_key == "d":
                self.line_list[edit_line_idx].point_list.pop(edit_point_idx)
                edit_point_idx = min(edit_point_idx + 1, len(self.line_list[edit_line_idx].point_list) - 1)
                self.line_list[edit_line_idx].updateConfidenceInterval()
                continue

            if self.mode == self.NORMAL:
                if input_key == "h":
                    edit_point_idx = max(edit_point_idx - 1, 0)
                    continue
                if input_key == "l":
                    edit_point_idx = min(edit_point_idx + 1, len(self.line_list[edit_line_idx].point_list) - 1)
                    continue
                if input_key == "j":
                    edit_line_idx = max(edit_line_idx - 1, 0)
                    if edit_point_idx >= len(self.line_list[edit_line_idx].point_list):
                        edit_point_idx = len(self.line_list[edit_line_idx].point_list) - 1
                    continue
                if input_key == "k":
                    edit_line_idx = min(edit_line_idx + 1, len(self.line_list) - 1)
                    if edit_point_idx >= len(self.line_list[edit_line_idx].point_list):
                        edit_point_idx = len(self.line_list[edit_line_idx].point_list) - 1
                    continue
                continue
            if self.mode == self.EDIT:
                if input_key == "h":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].x -= 0.01 * x_range
                    continue
                if input_key == "l":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].x += 0.01 * x_range
                    continue
                if input_key == "j":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].y -= 0.01 * y_range
                    continue
                if input_key == "k":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].y += 0.01 * y_range
                    continue
                if input_key == "J":
                    self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] = max(
                        self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] - 0.01 * y_range, 0)
                    continue
                if input_key == "K":
                    self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] += 0.01 * y_range
                    continue
            if self.mode == self.ADD:
                if input_key == "h":
                    edit_x -= 0.01 * x_range
                    continue
                if input_key == "l":
                    edit_x += 0.01 * x_range
                    continue
                if input_key == "j":
                    edit_y -= 0.01 * y_range
                    continue
                if input_key == "k":
                    edit_y += 0.01 * y_range
                    continue
                if input_key == "H":
                    edit_x -= 0.1 * x_range
                    continue
                if input_key == "L":
                    edit_x += 0.1 * x_range
                    continue
                if input_key == "J":
                    edit_y -= 0.1 * y_range
                    continue
                if input_key == "K":
                    edit_y += 0.1 * y_range
                    continue
                if input_key == "a":
                    self.line_list[edit_line_idx].addPoint(edit_x, edit_y)
                    self.line_list[edit_line_idx].updateConfidenceInterval()
                    continue
                if input_key == "n":
                    line_type = "-"
                    line_width = 2
                    fit_polyline = False
                    show_confidence_interval = True
                    confidence_diff_min = 5
                    confidence_diff_max = 10

                    new_line_idx = len(self.line_list)
                    self.addLine(line_type,
                                 line_width,
                                 str(new_line_idx),
                                 fit_polyline,
                                 show_confidence_interval,
                                 confidence_diff_min,
                                 confidence_diff_max)
                    self.line_list[new_line_idx].addPoint(edit_x, edit_y)
                    self.line_list[new_line_idx].updateConfidenceInterval()
                    edit_line_idx = new_line_idx
                    edit_point_idx = 0
                    continue
        return True

