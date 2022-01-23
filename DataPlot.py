#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from ChartPlot import ChartPlot

if __name__ == "__main__":
    json_file_path = "./coscan_data/scene_recovery_rate.txt"
    x_start = 0
    x_step = 1
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 5
    confidence_diff_max = 10
    show_line_label = True
    show_confidence_interval_label = False

    chart_plot = ChartPlot()

    data = {}
    with open(json_file_path, "r") as f:
        data = json.load(f)
    for key in data.keys():
        key_data = data[key]
        x_num = len(key_data)
        chart_plot.addLine(
            x_start, x_num, x_step,
            "r:", 5, key, fit_polyline,
            show_confidence_interval,
            confidence_diff_min, confidence_diff_max)
        for i in range(len(key_data)):
            chart_plot.addPoint(0, i, key_data[i])

    chart_plot.renderLine(
        show_line_label,
        show_confidence_interval_label)

