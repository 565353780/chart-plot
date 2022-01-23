#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from LineMethod.line_editor import LineEditor

class LineCreater(LineEditor):
    def __init__(self):
        LineEditor.__init__(self)

        self.fit_polyline = False
        self.show_confidence_interval = True
        self.confidence_diff_min = 5
        self.confidence_diff_max = 10
        return

    def setParam(self,
                 fit_polyline,
                 show_confidence_interval,
                 confidence_diff_min,
                 confidence_diff_max):
        self.fit_polyline = fit_polyline
        self.show_confidence_interval = show_confidence_interval
        self.confidence_diff_min = confidence_diff_min
        self.confidence_diff_max = confidence_diff_max

        line_type = "-"
        line_width = 2

        self.addLine(line_type,
                     line_width,
                     str(len(self.line_list)),
                     self.fit_polyline,
                     self.show_confidence_interval,
                     self.confidence_diff_min,
                     self.confidence_diff_max)
        self.line_list[0].addPoint(0, 0)
        self.line_list[0].updateConfidenceInterval()
        return True

def demo():
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 5
    confidence_diff_max = 10
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
    return True

if __name__ == "__main__":
    demo()

