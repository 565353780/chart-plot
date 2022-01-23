#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from ChartPlot import ChartPlot

if __name__ == "__main__":
    f = open("./coscan_data/scene_recovery_rate.txt", "r")
    data = json.load(f)
    f.close()

    ours_value = data["Ours"]

    x_start = 0
    x_num = len(ours_value)
    x_step = 1
    fit_polyline = False
    show_confidence_interval = True
    confidence_diff_min = 5
    confidence_diff_max = 10
    show_line_label = True
    show_confidence_interval_label = True

    chart_plot = ChartPlot()

    chart_plot.addLine(
        x_start, x_num, x_step,
        "r:", 5, "Ours", fit_polyline,
        show_confidence_interval,
        confidence_diff_min, confidence_diff_max)
    for i in range(len(ours_value)):
        chart_plot.addPoint(0, i, ours_value[i])

    chart_plot.renderLine(
        show_line_label,
        show_confidence_interval_label)

