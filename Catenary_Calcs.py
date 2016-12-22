# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:28:37 2016

@author: Vikneshan

For more information refer: http://vikneshan.blogspot.com/2016/12/catenary.html

References:
https://en.wikipedia.org/wiki/Catenary
https://mysite.du.edu/~jcalvert/math/catenary.htm
http://stackoverflow.com/questions/22742951/solve-an-equation-using-a-python-numerical-solver-in-numpy    
https://docs.python.org/2/library/math.html

"""
import numpy as np
import math as mh
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.legend_handler import HandlerLine2D
 
print("Getting inputs / Establishing knowns...")
b=float(input("distance between hanging points(m):"))/2
s=float(input("length of string(m):"))/2
w=float(input("mass of string(kg):"))/(s*2)*9.81
p=float(input("height of point of support from ground(m):"))

print("\nSolving for unknowns...")

func=lambda a: s-a*mh.sinh(b/a)

a_ini=0.1 #initial guess for a
a_sol=fsolve(func,a_ini)
H=w*a_sol
V=w*s
Th=mh.atan(s/a_sol) 
F=V/mh.sin(Th)
h=a_sol*(mh.cosh(b/a_sol)-1)
d=p-h

print('H=%.2f N'%H)
print('a=%.2f'% a_sol)
print('h=%.2f m' %h)

if d>=0:
    print('d=%.2f m'% d)
elif d<0:
    print('d=%.2f m,negative-not high enough from ground, min has to be h? '% d)
else:
    print('Something is bonkers')
    
print('V=%.2f N'% V)
print('F=%.2f N'% F)
print('Th=%.2f degrees' % mh.degrees(Th))

print('\nPlotting Graph...')

x=np.linspace(-b,b,num=1e5)
y=a_sol*np.cosh(x/a_sol)
line1,=plt.plot(x,y-a_sol,'b',label='C is at origin')
line2,=plt.plot(x,y-a_sol+p-h,'r',label='At specified support point heights')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.show()