#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getch import getch
import os
import json
import matplotlib.pyplot as plt

from LineManager import LineManager

class PlaceData(LineManager):
    def __init__(self):
        LineManager.__init__(self)

        self.x_start = 0
        self.x_num = 100
        self.x_step = 1
        self.fit_polyline = False
        self.show_confidence_interval = True
        self.confidence_diff_min = 0.5
        self.confidence_diff_max = 1.0
        return

    def setParam(self,
                 x_start, x_num, x_step,
                 fit_polyline,
                 show_confidence_interval,
                 confidence_diff_min,
                 confidence_diff_max):
        self.x_start = x_start
        self.x_num = x_num
        self.x_step = x_step
        self.fit_polyline = fit_polyline
        self.show_confidence_interval = show_confidence_interval
        self.confidence_diff_min = confidence_diff_min
        self.confidence_diff_max = confidence_diff_max
        return True

    def renderLine(self, show_line_label, show_confidence_interval_label):
        plt.figure(figsize=(8, 6), dpi=80)
        plt.ion()

        edit_line_idx = 0
        edit_point_idx = 0
        while True:
            plt.cla()

            plt.title("PlaceData Render")
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
                self.line_list[edit_line_idx].confidence_interval_list[edit_point_idx] += 0.1 * y_range
            elif input_key == "n":
                edit_line_idx = min(edit_line_idx + 1, len(self.line_list) - 1)
            elif input_key == "p":
                edit_line_idx = max(edit_line_idx - 1, 0)
            elif input_key == "u":
                self.line_list[edit_line_idx].updateConfidenceInterval()
        return True

if __name__ == "__main__":
    x_start = 0
    x_num = 100
    x_step = 1
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 0.5
    confidence_diff_max = 1.0
    show_line_label = True
    show_confidence_interval_label = False
    save_json_file_path = "./test.json"

    place_data = PlaceData()

    place_data.setParam(x_start,
                        x_num,
                        x_step,
                        fit_polyline,
                        show_confidence_interval,
                        confidence_diff_min,
                        confidence_diff_max)

    place_data.renderLine(show_line_label, show_confidence_interval_label)

    data_json = place_data.getDataJson()
    json_dump = json.dumps(data_json)
    if os.path.exists(save_json_file_path):
        print("save_json_file_path already exist!")
    else:
        with open(save_json_file_path, "w") as f:
            f.write(data_json)

