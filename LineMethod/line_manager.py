#!/usr/bin/env python
# -*- coding: utf-8 -*-

from LineMethod.line import Line

class LineManager(object):
    def __init__(self):
        self.line_list = []
        return

    def reset(self):
        self.line_list.clear()
        return True

    def addLine(self,
                x_start,
                x_num,
                x_step,
                line_type,
                line_width,
                label,
                fit_polyline,
                show_confidence_interval,
                confidence_diff_min,
                confidence_diff_max):
        new_line = Line(len(self.line_list))
        if not new_line.setLineProperty(line_type, line_width, label):
            print("LineManager::addLine :")
            print("setLineProperty for line " + str(new_line.line_idx) + " failed!")
            return False

        if not new_line.setXRange(x_start, x_num, x_step):
            print("LineManager::addLine :")
            print("setXRange for line " + str(new_line.line_idx) + " failed!")
            return False

        new_line.fit_polyline = fit_polyline
        new_line.show_confidence_interval = show_confidence_interval
        new_line.confidence_diff_min = confidence_diff_min
        new_line.confidence_diff_max = confidence_diff_max

        self.line_list.append(new_line)
        return True

    def setXRange(self, line_idx, x_start, x_num, x_step):
        if line_idx >= len(self.line_list):
            print("LineManager::setXRange :")
            print("line_idx out of range!")
            return False

        if not self.line_list[line_idx].setXRange(x_start, x_num, x_step):
            print("LineManager::setXRange :")
            print("setXRange for line " + str(line_idx) + " failed!")
            return False
        return True

    def addPoint(self, line_idx, x_idx, y_value):
        if line_idx >= len(self.line_list):
            print("LineManager::addPoint :")
            print("line_idx out of range!")
            return False

        if not self.line_list[line_idx].addPoint(x_idx, y_value):
            print("LineManager::addPoint :")
            print("addPoint for line " + str(line_idx) + " failed!")
            return False

        if self.line_list[line_idx].show_confidence_interval:
            if not self.line_list[line_idx].updateConfidenceInterval():
                print("LineManager::addLine :")
                print("updateConfidenceInterval for line " + str(line_idx) + " failed!")
                return False
        return True

    def getYRange(self):
        y_min = 0
        y_max = 0

        if len(self.line_list) == 0:
            return y_max - y_min

        y_min = min(self.line_list[0].y_list)
        y_max = max(self.line_list[0].y_list)

        for line in self.line_list:
            y_min = min(y_min, min(line.y_list))
            y_max = max(y_max, max(line.y_list))
        return y_max - y_min

    def getDataJson(self):
        data_json = {}
        line_json = {}
        for line in self.line_list:
            line_json["line_type"] = line.line_type
            line_json["line_width"] = line.line_width
            line_json["label"] = line.label
            line_json["x_list"] = line.x_list
            line_json["point_list"] = line.getPointData()
            line_json["y_list"] = line.y_list
            line_json["fit_polyline"] = line.fit_polyline
            line_json["show_confidence_interval"] = line.show_confidence_interval
            line_json["confidence_diff_min"] = line.confidence_diff_min
            line_json["confidence_diff_max"] = line.confidence_diff_max
            line_json["confidence_interval_list"] = line.confidence_interval_list
            data_json[line.label] = line_json
        return data_json

    def loadDataJson(self, data_json):
        self.reset()
        for line_label in data_json.keys():
            new_line = Line(len(self.line_list))
            line_json = data_json[line_label]
            new_line.line_type = line_json["line_type"]
            new_line.line_width = line_json["line_width"]
            new_line.label = line_json["label"]
            new_line.x_list = line_json["x_list"]
            new_line.loadPointData(line_json["point_list"])
            new_line.y_list = line_json["y_list"]
            new_line.fit_polyline = line_json["fit_polyline"]
            new_line.show_confidence_interval = line_json["show_confidence_interval"]
            new_line.confidence_diff_min = line_json["confidence_diff_min"]
            new_line.confidence_diff_max = line_json["confidence_diff_max"]
            new_line.confidence_interval_list = line_json["confidence_interval_list"]
            self.line_list.append(new_line)
        return True

