#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from LineMethod.line_renderer import LineRenderer

if __name__ == "__main__":
    json_file_path = "./new_data.json"
    show_line_label = True
    show_confidence_interval_label = True

    data_stream = ""
    with open(json_file_path, "r") as f:
        data_stream = f.read()
    data_json = json.loads(data_stream)

    line_renderer = LineRenderer()

    line_renderer.loadDataJson(data_json)

    line_renderer.renderLine(
        show_line_label,
        show_confidence_interval_label)

