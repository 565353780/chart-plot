#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from LineMethod.line_creater import LineCreater

if __name__ == "__main__":
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 10
    confidence_diff_max = 20
    show_line_label = True
    show_confidence_interval_label = False
    save_json_file_path = "./new_data.json"

    line_creater = LineCreater()

    line_creater.setParam(fit_polyline,
                        show_confidence_interval,
                        confidence_diff_min,
                        confidence_diff_max)

    line_creater.editLine(show_line_label, show_confidence_interval_label)

    data_json = line_creater.getDataJson()
    data_json_dump = json.dumps(data_json, indent=4)
    with open(save_json_file_path, "w") as f:
        f.write(data_json_dump)

