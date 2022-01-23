#!/usr/bin/env python
# -*- coding: utf-8 -*-

from LineMethod.line import Line

class LineManager(object):
    def __init__(self):
        self.line_list = []
        self.show_line_label = True
        self.show_confidence_interval_label = False
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

    def setPoint(self, line_idx, x, y):
        if not self.line_list[line_idx].setPoint(x, y):
            print("LineManager::setPoint :")
            print("setPoint for line " + str(line_idx) + " failed!")
            return False

        if self.line_list[line_idx].show_confidence_interval:
            if not self.line_list[line_idx].updateConfidenceInterval():
                print("LineManager::setPoint :")
                print("updateConfidenceInterval for line " + str(line_idx) + " failed!")
                return False
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
            x_max = max(x_max, line_x_max)
            y_min = min(y_min, line_y_min)
            y_max = max(y_max, line_y_max)
        return x_min, x_max, y_min, y_max

    def getXYRange(self):
        x_min, x_max, y_min, y_max = self.getBBoxXYXY()
        if x_min is None:
            return 0, 0
        return x_max - x_min, y_max - y_min

    def getDataJson(self):
        data_json = {}
        data_json["show_line_label"] = self.show_line_label
        data_json["show_confidence_interval_label"] = self.show_confidence_interval_label
        data_json["Lines"] = {}
        line_json = {}
        for line in self.line_list:
            line_json["line_type"] = line.line_type
            line_json["line_width"] = line.line_width
            line_json["label"] = line.label
            line_json["point_list"] = line.getPointData()
            line_json["fit_polyline"] = line.fit_polyline
            line_json["show_confidence_interval"] = line.show_confidence_interval
            line_json["confidence_diff_min"] = line.confidence_diff_min
            line_json["confidence_diff_max"] = line.confidence_diff_max
            line_json["confidence_interval_list"] = line.confidence_interval_list
            data_json["Lines"][line.label] = line_json
        return data_json

    def loadDataJson(self, data_json):
        self.reset()
        self.show_line_label = data_json["show_line_label"]
        self.show_confidence_interval_label = data_json["show_confidence_interval_label"]
        for line_label in data_json["Lines"].keys():
            new_line = Line(len(self.line_list))
            line_json = data_json["Lines"][line_label]
            new_line.line_type = line_json["line_type"]
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

