#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from LineMethod.line_renderer import LineRenderer

def demo():
    json_file_path = "/home/chli/chLi/coscan_data/different_robot_num/DC_data.json"
    show_line_label = True
    show_confidence_interval_label = True
    pdf_save_file_path = "/home/chli/chLi/coscan_data/different_robot_num/DC_chart.pdf"

    data_stream = ""
    with open(json_file_path, "r") as f:
        data_stream = f.read()
    data_json = json.loads(data_stream)

    line_renderer = LineRenderer()

    line_renderer.loadDataJson(data_json)

    line_renderer.savePDF(pdf_save_file_path,
                          show_line_label,
                          show_confidence_interval_label)

def demo_folder():
    json_file_folder_path = "/home/chli/chLi/coscan_data/different_robot_num/"
    show_line_label = True
    show_confidence_interval_label = True

    for json_file_name in os.listdir(json_file_folder_path):
        if json_file_name[-5:] != ".json":
            continue
        json_file_path = json_file_folder_path + json_file_name
        pdf_save_file_path = \
            json_file_folder_path + json_file_name.split(".json")[0] + ".pdf"

        data_stream = ""
        with open(json_file_path, "r") as f:
            data_stream = f.read()
        data_json = json.loads(data_stream)

        line_renderer = LineRenderer()

        line_renderer.loadDataJson(data_json)

        line_renderer.savePDF(pdf_save_file_path,
                              show_line_label,
                              show_confidence_interval_label)
    return True

if __name__ == "__main__":
    demo_folder()

