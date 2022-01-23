#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BarMethod.bar import Bar

class BarManager(object):
    def __init__(self):
        self.bar_list = []
        return

    def reset(self):
        self.bar_list.clear()
        return True

