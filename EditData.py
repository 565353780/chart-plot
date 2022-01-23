#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from LineMethod.line_editor import LineEditor

if __name__ == "__main__":
    json_file_path = "./coscan_data/test.json"
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

