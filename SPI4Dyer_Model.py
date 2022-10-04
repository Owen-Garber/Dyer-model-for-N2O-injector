# -* - coding : utf -8 -* -
"""
Created on Mon Dec 9 15:30:26 2019
SPI for Dyer
Changed to only calculate for one upstream pressure .
Also changed so that the minimum P_2 ( given by deltaP below ) is 1
bar , to match HEM .
NOTE FOR CO2 : minimum P_2 =5.2 bar
Start from highest deltaP to match HEM as well .

 Furthermore , DeltaP cannot be 0 as this will cause a division by 0
in
the Dyer model ’s calculation of k, so has been set to stop at 1.
@author : asus
"""
import numpy as np
import matplotlib . pyplot as plt
from CoolProp . CoolProp import PropsSI

# Input example :
Cd =0.76
D_2 =.00157 # diameter of orifice [m]
P_1 =5.05E6 # Upstream pressure , each new value provides a new graph
Fluid ='N2O' # Must be such that CoolProp understands
steps =1000 # number of iterations used to generate each graph , i.e. size of delta P

# Function starts here
def SPI4Dyer_Model ( Fluid , P_1 , Cd , D_2 , steps ) :
 A_2 =(np.pi/4) * D_2 **2 # calculate area of orifice

 mSPI = np.zeros(steps)
 if Fluid == 'N2O':# See introduction text above for explaination
  DeltaP = np.linspace(P_1-1E5,1,steps)
 else:
  DeltaP = np.linspace(P_1-5.2E5,1,steps)
 rho = PropsSI ('D','P',P_1 ,'Q' ,0 , Fluid ) # Saturated liquid density

 for i in range ( steps ) :
   mSPI [ i ]= Cd * A_2 * np . sqrt (2* rho * DeltaP [ i ])
 return mSPI

# plt.plot (DeltaP ,mSPI , label = 'P1 =%.2 f [MPa ] '%( P_1 /(1E6)))
# # plt.title ( 'Single - Phase Incompressible Model ')
# # plt.xlabel ( 'P1 -P2[Pa ] ')
# # plt.ylabel ( ' Mass Flow Rate [kg/s]')
# # plt.grid ()
# # plt.legend ()
# # plt.show ()
