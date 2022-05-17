#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from LineMethod.line_creater import LineCreater

def getData():
    '''
    chart_data_dict = [robot_num][metric_name][x or scene_level] -> value_list
    '''
    data_file_path = "/home/chli/chLi/coscan_data/different_robot_num.txt"
    metric_name_list = ["DC", "TC", "D-LB", "T-LB"]
    metric_col_idx_list = [5, 6, 11, 12]
    data_list = []

    with open(data_file_path, "r") as f:
        for line in f.readlines():
            line_split_list = line.replace(" ", "").split("\n")[0].split("|")[1:-1]
            valid_line_data = \
                [line_split_list[col_idx] for col_idx in metric_col_idx_list]
            data_list.append(valid_line_data)

    chart_data_dict = {}
    for metric_name in metric_name_list:
        chart_data_dict[metric_name] = {}
        chart_data_dict[metric_name]["x"] = [i for i in range(3, 11)]

    scene_level_list = ["Small", "Middle", "Large"]
    for metric_idx in range(len(metric_name_list)):
        for scene_level in range(3):
            chart_y_list = []
            for data_idx in range(8):
                chart_y_list.append(
                    data_list[3 * data_idx + scene_level][metric_idx])
            chart_data_dict[
                metric_name_list[metric_idx]][
                    scene_level_list[scene_level]] = \
                chart_y_list
    return chart_data_dict

if __name__ == "__main__":
    chart_data_dict = getData()

    fit_polyline = False
    show_confidence_interval = False
    confidence_diff_min = 0
    confidence_diff_max = 0
    show_line_label = True
    show_confidence_interval_label = False

    line_type = "-"
    line_width = 2
    line_color_list = ["tomato", "teal", "orange"]

    for chart_name in chart_data_dict.keys():
        line_creater = LineCreater()

        line_creater.setParam(fit_polyline,
                              show_confidence_interval,
                              confidence_diff_min,
                              confidence_diff_max)

        line_creater.x_label = "#Robot"
        line_creater.y_label = chart_name
        line_creater.title = ""
        line_creater.line_list = []

        chart_data = chart_data_dict[chart_name]
        chart_x_list = chart_data["x"]
        line_color_idx = 0
        for chart_y_name in chart_data.keys():
            if chart_y_name == "x":
                continue
            chart_y_list = chart_data[chart_y_name]

            new_line_idx = len(line_creater.line_list)
            line_creater.addLine(line_type,
                                 line_width,
                                 chart_y_name,
                                 fit_polyline,
                                 show_confidence_interval,
                                 confidence_diff_min,
                                 confidence_diff_max)
            line_creater.line_list[new_line_idx].line_color = \
                line_color_list[line_color_idx]
            line_color_idx += 1
            for i in range(len(chart_x_list)):
                line_creater.line_list[new_line_idx].addPoint(
                    chart_x_list[i], chart_y_list[i])
            line_creater.line_list[new_line_idx].updateConfidenceInterval()

        line_creater.renderLine(show_line_label, show_confidence_interval_label)
        continue

        chart_save_path = "./test/" + chart_name + "_data.json"
        data_json = line_creater.getDataJson()
        data_json_dump = json.dumps(data_json, indent=4)
        with open(chart_save_path, "w") as f:
            f.write(data_json_dump)

