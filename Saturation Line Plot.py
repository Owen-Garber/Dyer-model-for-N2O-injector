# -* - coding : utf -8 -* -
"""
Created on Sat Apr 25 15:34:42 2020
code for generating N2O Saturation Line
@author : asus
"""

import numpy as np
import matplotlib.pyplot as plt
import CoolProp
from CoolProp.CoolProp import PropsSI
from CoolProp.Plots import PropertyPlot


T = np.linspace(182.23,309.52,1000)# limits are triple point and critical point temperatures
P = np.zeros (1000)
for i in range(len(T)) :
    currentP = PropsSI('P','T',T [i],'Q',1,'N2O')
    P [i]= currentP

tripPoint =( T [0] , P [0])
critPoint =( T [ -1] , P [ -1])

plt.plot (T , P )
plt.scatter ( tripPoint [0] , tripPoint [1])
plt.scatter ( critPoint [0] , critPoint [1])
plt.annotate (" Triple Point " ,( tripPoint [0] -5 , tripPoint [1]+600000) )
plt.annotate (" Critical Point " ,( critPoint [0] -30 , critPoint [1]) )
plt.title ('Vapor - liquid saturation curve of N2O ')
plt.xlabel ('T [K]')
plt.ylabel ('P [Pa]')
plt.grid ()
plt.legend ()
#plt.ticklabel_format ( axis ="x" , style =" sci" , scilimits =(0 ,0))
plt.show ()
