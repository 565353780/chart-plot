#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
 
name_list = ['Monday','Tuesday','Friday','Sunday']
num_list = [1.5,0.6,7.8,6]
num_list1 = [1,2,3,1]
x =list(range(len(num_list)))
total_width, n = 0.8, 2
width = total_width / n
 
plt.bar(x, num_list, width=width, label='boy')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list1, width=width, label='girl',tick_label = name_list)
plt.legend()
plt.show()

