#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
from getch import getch

from LineMethod.line_renderer import LineRenderer

class LineEditor(LineRenderer):
    def __init__(self):
        LineRenderer.__init__(self)

        self.move_scale = 0.002
        self.scale_lower = 0.9
        self.scale_upper = 1.1

        self.NORMAL = "NORMAL"
        self.EDIT = "EDIT"
        self.ADD = "ADD"
        self.SCALE = "SCALE"
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
        if input_key == "s":
            if self.mode == self.SCALE:
                return False
            self.mode = self.SCALE
            return True
        return False

    def editLine(self, show_line_label, show_confidence_interval_label):
        self.show_line_label = show_line_label
        self.show_confidence_interval_label = show_confidence_interval_label

        plt.figure(figsize=(self.fig_size[0], self.fig_size[1]), dpi=self.dpi)
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
            x_min, y_min, _, _ = self.getBBoxXYXY()
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
                    self.line_list[edit_line_idx].point_list[edit_point_idx].x -= self.move_scale * x_range
                    continue
                if input_key == "l":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].x += self.move_scale * x_range
                    continue
                if input_key == "j":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].y -= self.move_scale * y_range
                    continue
                if input_key == "k":
                    self.line_list[edit_line_idx].point_list[edit_point_idx].y += self.move_scale * y_range
                    continue
                if input_key == "J":
                    self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] = max(
                        self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] - self.move_scale * y_range, 0)
                    continue
                if input_key == "K":
                    self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] += self.move_scale * y_range
                    continue
                if input_key == "o":
                    self.line_list[edit_line_idx].confidence_diff_max = max(
                        self.line_list[edit_line_idx].confidence_diff_max - self.move_scale * y_range,
                        self.line_list[edit_line_idx].confidence_diff_min)
                    self.line_list[edit_line_idx].updateConfidenceInterval()
                    continue
                if input_key == "p":
                    self.line_list[edit_line_idx].confidence_diff_max += self.move_scale * y_range
                    self.line_list[edit_line_idx].updateConfidenceInterval()
                    continue
                if input_key == "n":
                    self.line_list[edit_line_idx].confidence_diff_min = max(
                        self.line_list[edit_line_idx].confidence_diff_min - self.move_scale * y_range, 0)
                    self.line_list[edit_line_idx].updateConfidenceInterval()
                    continue
                if input_key == "m":
                    self.line_list[edit_line_idx].confidence_diff_min += self.move_scale * y_range
                    self.line_list[edit_line_idx].updateConfidenceInterval()
                    continue
            if self.mode == self.ADD:
                if input_key == "h":
                    edit_x -= self.move_scale * x_range
                    continue
                if input_key == "l":
                    edit_x += self.move_scale * x_range
                    continue
                if input_key == "j":
                    edit_y -= self.move_scale * y_range
                    continue
                if input_key == "k":
                    edit_y += self.move_scale * y_range
                    continue
                if input_key == "H":
                    edit_x -= 10.0 * self.move_scale * x_range
                    continue
                if input_key == "L":
                    edit_x += 10.0 * self.move_scale * x_range
                    continue
                if input_key == "J":
                    edit_y -= 10.0 * self.move_scale * y_range
                    continue
                if input_key == "K":
                    edit_y += 10.0 * self.move_scale * y_range
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
                    confidence_diff_min = 10
                    confidence_diff_max = 20

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
            if self.mode == self.SCALE:
                if input_key == "h":
                    move_dist = self.move_scale * x_range
                    edit_x -= move_dist
                    self.moveLeft(move_dist)
                    continue
                if input_key == "l":
                    move_dist = self.move_scale * x_range
                    edit_x += move_dist
                    self.moveRight(move_dist)
                    continue
                if input_key == "j":
                    move_dist = self.move_scale * y_range
                    edit_y -= move_dist
                    self.moveDown(move_dist)
                    continue
                if input_key == "k":
                    move_dist = self.move_scale * y_range
                    edit_y += move_dist
                    self.moveUp(move_dist)
                    continue
                if input_key == "H":
                    edit_x = x_min + self.scale_lower * (edit_x - x_min)
                    self.scaleX(self.scale_lower)
                    continue
                if input_key == "L":
                    edit_x = x_min + self.scale_upper * (edit_x - x_min)
                    self.scaleX(self.scale_upper)
                    continue
                if input_key == "J":
                    edit_y = y_min + self.scale_lower * (edit_y - y_min)
                    self.scaleY(self.scale_lower)
                    continue
                if input_key == "K":
                    edit_y = y_min + self.scale_upper * (edit_y - y_min)
                    self.scaleY(self.scale_upper)
                    continue
        return True

def demo():
    json_file_path = "./new_data.json"
    show_line_label = True
    show_confidence_interval_label = True

    data_stream = ""
    with open(json_file_path, "r") as f:
        data_stream = f.read()
    data_json = json.loads(data_stream)

    line_editor = LineEditor()

    line_editor.loadDataJson(data_json)

    line_editor.editLine(
        show_line_label,
        show_confidence_interval_label)

    data_json = line_editor.getDataJson()

    data_json_dump = json.dumps(data_json, indent=4)
    with open(json_file_path, "w") as f:
        f.write(data_json_dump)
    return True

if __name__ == "__main__":
    demo()

