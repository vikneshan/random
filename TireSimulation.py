# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 22:46:53 2016

@author: Vikneshan
http://vikneshan.blogspot.com/2016/09/tire-pressure-simulations.html for more information
Simulating tire pressure throughout the year, with weather data and some other assumptions

"""
#importing modules
from xlrd import open_workbook #importing lib to deal with excel workbooks
import matplotlib.pyplot as plt
import numpy as np
#------------------------------------------------------------------------------
# Defining functions
# Calculate pressure using ideal gas laws
def pressure(m,V,Rs,T):
    #m  - mass, g
    #Rs - specific gas constant, J/g-K
    #V  - volume of air, m^3
    #T  - Temperature, K
    P=m/V*Rs*T
    return P #pressure in Pa
    
# Calculate mass in grams using ideal gas laws    
def mass(P,V,Rs,T):
    m=P*V/(Rs*T)
    return m
    
# Convert from Fahrenheit to Kelvin
def TK(TF):
    Temp=(459.65+TF)*5/9
    return Temp
# Convert from PSI to kPa
def PSI2PA(PSI):
    return PSI*6894.76
    
#------------------------------------------------------------------------------
# Establishing a constant mass leakage rate - assuming average mean temperature over the year - 2013 thru 2015
# Assuming a loss of 1 PSI/month

T_ave=TK(61.7) 
V=0.018 #m^3
R=0.2869

P_i= 321.9e3 #start of month 32 PSI (units for this is kPa): gauge + atmospheric pressure (101.3 kPa)
P_f= 315.0e3 #end of month 31 PSI

m_i=mass(P_i,V,R,T_ave)
m_f=mass(P_f,V,R,T_ave)

dm_month=m_i-m_f #monthly leakage rate - g/month
dm=dm_month/30.4 #daily leakage rate - g/day

#------------------------------------------------------------------------------
#Import Weather Data from Input File
wb =open_workbook('C:\\Users\\Vikneshan\\Desktop\\Dropbox\\Tinkering\\OtherProjects\\TireThoughtExperiment\\WeatherInput.xlsx')
s=wb.sheet_by_name('Data') #assigning sheet object from workbook object

# for 3 column data - e.g.
dates=[] # initializing variables
day=[]
T=[]
    
for col in range(s.ncols): #includes zero to include all 3 columns
    for row in range(1,s.nrows): #excludes zero to exclude header
        
        if col==0:
            dates.append(s.cell(row,col).value)
        elif col==1:
            day.append(s.cell(row,col).value)
        elif col==2:
            T.append(s.cell(row,col).value)
        else:
            print('whatcha smokin bruh?')
            
#------------------------------------------------------------------------------
# Start of simulation code
Pmin=PSI2PA(30)+101.3e3 #Min threshold for tire pressure before fill again
m=[]
P=[]
f_count=[] # for each start date, what are the annual fill counts
f_day=[] # days where it is filled
diff_day=[]# difference between fill dates
sim_l=730

for i in range(365):
    count=1
    m_n=[]
    P_n=[]
    f_day_n=[]
    P0=PSI2PA(32)+101.3e3 #Always start with manufacturer recommended PSI for own car
    m0=mass(P0,V,R,TK(T[i]))
    P_n.append(P0)
    m_n.append(m0)
    
    for j in range(sim_l):
        m1=m0-dm
        P1=pressure(m1,V,R,TK(T[i+j]))
        if P1<Pmin: #to check if need to fill tire
            count=count+1
            P1=PSI2PA(32)+101.3e3
            f_day_n.append(i+j)
            m1=mass(P1,V,R,TK(T[i+j]))
        m0=m1
        m_n.append(m1)
        P_n.append(P1)
    f_count.append(count)
    m.append(m_n)
    P.append(P_n)
    f_day.append(f_day_n)
    diff_day.append(np.diff(np.array([i]+f_day_n)))

#finding the first min refill count 
print('Example of Minimum Refill Count Scenario') 
print('========================================')
daymin=f_count.index(min(f_count))#finds the index for the first minimum
plt.plot(day[daymin:daymin+sim_l+1],P[daymin],'b-')
plt.ylabel('Pressure(Pa)')
plt.xlabel('Day Number')
plt.show()

plt.plot(day[daymin:daymin+sim_l+1],m[daymin],'r-')
plt.ylabel('Mass of air in tire (g)')
plt.xlabel('Day Number')
plt.show()

plt.plot(day[daymin:daymin+sim_l+1],T[daymin:daymin+sim_l+1],'g-')
plt.ylabel('Minimum Temperature ($^\circ$F)')
plt.xlabel('Day Number')
plt.show()

#plt.plot(f_day[daymin],'g^') #when refill days were
#plt.show()

#finding the first max refill count 
print('Example of Maximum Refill Count Scenario')
print('========================================')
daymax=f_count.index(max(f_count))
plt.plot(day[daymax:daymax+sim_l+1],P[daymax],'b-')
plt.ylabel('Pressure(Pa)')
plt.xlabel('Day Number')
plt.show()

plt.plot(day[daymax:daymax+sim_l+1],m[daymax],'r-')
plt.ylabel('Mass of air in tire (g)')
plt.xlabel('Day Number')
plt.show()

plt.plot(day[daymax:daymax+sim_l+1],T[daymax:daymax+sim_l+1],'g-')
plt.ylabel('Minimum Temperature ($^\circ$F)')
plt.xlabel('Day Number')
plt.show()

#plotting refill counts for 365 different scenarios
print('Refill Count for All Scenario')
print('========================================')
plt.plot(f_count,'r^')
plt.ylabel('Refill Count (Times)')
plt.xlabel('Start Day Number')
plt.show()

