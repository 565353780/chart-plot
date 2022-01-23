#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from LineMethod.line_renderer import LineRenderer

if __name__ == "__main__":
    json_file_path = "./test.json"
    x_start = 0
    x_step = 1
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 5
    confidence_diff_max = 10
    show_line_label = True
    show_confidence_interval_label = False

    line_renderer = LineRenderer()

    data_stream = ""
    with open(json_file_path, "r") as f:
        data_stream = f.read()
    data_json = json.loads(data_stream)
    line_renderer.loadDataJson(data_json)

    line_renderer.renderLine(
        show_line_label,
        show_confidence_interval_label)

    data_json = line_renderer.getDataJson()
    data_json_dump = json.dumps(data_json, indent=4)
    with open(json_file_path, "w") as f:
        f.write(data_json_dump)

