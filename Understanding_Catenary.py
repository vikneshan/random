# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 22:25:55 2016

@author: Vikneshan

Reference:  
http://matplotlib.org/users/legend_guide.html
"""
#for next step use, remove from this script once done: http://stackoverflow.com/questions/22742951/solve-an-equation-using-a-python-numerical-solver-in-numpy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

b=-0.5 #- d/2 -> lower limit
c=-b #d/2 -> upper limit

x=np.linspace(b,c,num=1e7)

a=[0.5,1,1.5,2]
#a=[1]
color=['r','g','b','k']
count=int(0)

for a_n in a:
    y=a_n*np.cosh(x/a_n)
    line1,=plt.plot(x,y,color[count],label=str(a_n))
    count+=1
    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

plt.show()
