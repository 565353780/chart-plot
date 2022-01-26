#!/usr/bin/env python
# -*- coding: utf-8 -*-

from LineMethod.line import Line

class LineManager(object):
    def __init__(self):
        self.title = "Title"
        self.x_label = "X Label"
        self.y_label = "Y Label"
        self.marker = ""
        self.fill_alpha = 0.2
        self.fig_size = [20, 15]
        self.dpi = 80
        self.show_line_label = True
        self.show_confidence_interval_label = False

        self.line_list = []
        return

    def reset(self):
        self.line_list.clear()
        return True

    def addLine(self,
                line_type,
                line_width,
                label,
                fit_polyline,
                show_confidence_interval,
                confidence_diff_min,
                confidence_diff_max):
        new_line = Line(len(self.line_list))
        new_line.line_type = line_type
        new_line.line_width = line_width
        new_line.label = label
        new_line.fit_polyline = fit_polyline
        new_line.show_confidence_interval = show_confidence_interval
        new_line.confidence_diff_min = confidence_diff_min
        new_line.confidence_diff_max = confidence_diff_max

        self.line_list.append(new_line)
        return True

    def getBBoxXYXY(self):
        x_min = None
        y_min = None
        x_max = None
        y_max = None

        if len(self.line_list) == 0:
            return x_min, y_min, x_max, y_max

        for line in self.line_list:
            line_x_min , line_y_min, line_x_max, line_y_max = line.getBBoxXYXY()
            if line_x_min is None:
                continue

            if x_min is None:
                x_min = line_x_min
                y_min = line_y_min
                x_max = line_x_max
                y_max = line_y_max
                continue

            x_min = min(x_min, line_x_min)
            y_min = min(y_min, line_y_min)
            x_max = max(x_max, line_x_max)
            y_max = max(y_max, line_y_max)
        return x_min, y_min, x_max, y_max

    def getXYRange(self):
        x_min, y_min, x_max, y_max = self.getBBoxXYXY()
        if x_min is None:
            return 0, 0
        return x_max - x_min, y_max - y_min

    def moveUp(self, move_dist):
        if move_dist == 0:
            return True

        for line in self.line_list:
            line.moveUp(move_dist)
        return True

    def moveDown(self, move_dist):
        if move_dist == 0:
            return True

        for line in self.line_list:
            line.moveDown(move_dist)
        return True

    def moveLeft(self, move_dist):
        if move_dist == 0:
            return True

        for line in self.line_list:
            line.moveLeft(move_dist)
        return True

    def moveRight(self, move_dist):
        if move_dist == 0:
            return True

        for line in self.line_list:
            line.moveRight(move_dist)
        return True

    def scaleX(self, scale):
        x_min, _, _, _ = self.getBBoxXYXY()

        if x_min is None:
            return True

        for line in self.line_list:
            line.scaleX(x_min, scale)
        return True

    def scaleY(self, scale):
        _, y_min, _, _ = self.getBBoxXYXY()

        if y_min is None:
            return True

        for line in self.line_list:
            line.scaleY(y_min, scale)
        return True

    def getDataJson(self):
        data_json = {}
        data_json["title"] = self.title
        data_json["x_label"] = self.x_label
        data_json["y_label"] = self.y_label
        data_json["marker"] = self.marker
        data_json["fill_alpha"] = self.fill_alpha
        data_json["fig_size"] = self.fig_size
        data_json["dpi"] = self.dpi
        data_json["show_line_label"] = self.show_line_label
        data_json["show_confidence_interval_label"] = self.show_confidence_interval_label
        data_json["Lines"] = {}
        for line in self.line_list:
            line_json = {}
            line_json["line_type"] = line.line_type
            line_json["line_color"] = line.line_color
            line_json["line_width"] = line.line_width
            line_json["label"] = line.label
            line_json["point_list"] = line.getPointData()
            line_json["fit_polyline"] = line.fit_polyline
            line_json["show_confidence_interval"] = line.show_confidence_interval
            line_json["confidence_diff_min"] = line.confidence_diff_min
            line_json["confidence_diff_max"] = line.confidence_diff_max
            line_json["confidence_interval_list"] = line.confidence_interval_list
            data_json["Lines"][str(line.line_idx)] = line_json
        return data_json

    def loadDataJson(self, data_json):
        self.reset()
        self.title = data_json["title"]
        self.x_label = data_json["x_label"]
        self.y_label = data_json["y_label"]
        self.marker = data_json["marker"]
        self.fill_alpha = data_json["fill_alpha"]
        self.fig_size = data_json["fig_size"]
        self.dpi = data_json["dpi"]
        self.show_line_label = data_json["show_line_label"]
        self.show_confidence_interval_label = data_json["show_confidence_interval_label"]
        data_json["Lines"].keys()
        for line_key in data_json["Lines"].keys():
            new_line = Line(len(self.line_list))
            line_json = data_json["Lines"][line_key]
            new_line.line_type = line_json["line_type"]
            new_line.line_color = line_json["line_color"]
            new_line.line_width = line_json["line_width"]
            new_line.label = line_json["label"]
            new_line.loadPointData(line_json["point_list"])
            new_line.fit_polyline = line_json["fit_polyline"]
            new_line.show_confidence_interval = line_json["show_confidence_interval"]
            new_line.confidence_diff_min = line_json["confidence_diff_min"]
            new_line.confidence_diff_max = line_json["confidence_diff_max"]
            new_line.confidence_interval_list = line_json["confidence_interval_list"]

            self.line_list.append(new_line)
        return True

