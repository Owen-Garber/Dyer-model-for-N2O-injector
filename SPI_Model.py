# -* - coding : utf -8 -* -
"""
 Created on Mon Nov 11 11:51:51 2019

 @author : Jonas

 Single - Phase Incompressible Model
 """
import numpy as np
import matplotlib . pyplot as plt
from CoolProp . CoolProp import PropsSI

# Input example :
Cd =0.9 # discharge coeff .
D_2 =0.00157 # diameter of orifice [m] ~~from RPE
P_1 = np . linspace (6E6 ,4E6 ,100) # Upstream pressure , each new value provides a new graph
Fluid ='N2O' # Must be such that CoolProp understands
steps = 100 # number of iterations used to generate each graph , i.e. size of delta P
Operating_P2 =2.413E6 # downstream pressure of interest ( needs to match P_1 ?)

# Function starts here
def SPI_Model ( Fluid , P_1 , Cd , D_2 , steps , Operating_P2 ) :
 A_2 =( np . pi /4) * D_2 **2 # calculate area of orifice
 number_graphs =len( P_1 ) # number of graphs , new graph for each value of P_1

 # initialize arrays for rho , T_1 , DeltaP , mSPI , Operating values
 rho = np . zeros ( number_graphs )
 T_1 = np . zeros ( number_graphs )
 mSPI = np . zeros (( steps , number_graphs ) )
 DeltaP = np . zeros (( steps , number_graphs ) )
 Operating_DeltaP = np . zeros ( number_graphs )
 Operating_FlowRate = np . zeros ( number_graphs )
#P_2=np. zeros (( steps , number_graphs ))

# calculate values for different P_1 cases
 for j in range ( number_graphs ) :
  #P_2=np. linspace (P_1[j] ,0 , steps )
  DeltaP [: , j ]= np.linspace(0 , P_1 [ j ] , steps )
  # DeltaP [: ,j]= P_1[j] -P_2 [: ,j]
  rho [ j ]= PropsSI ('D','P', P_1 [ j ] ,'Q' ,0 , Fluid ) # Saturated liquid density
  T_1 [ j ]= PropsSI ('T','P', P_1 [ j ] ,'Q' ,0 , Fluid ) # Saturated liquid temperature (not used )
# print (T_1)

  for i in range (steps) :
   mSPI [i , j]= Cd * A_2 * np.sqrt(2* rho [ j ]* DeltaP [i , j ])

   Operating_DeltaP [ j ]= P_1 [ j ] - Operating_P2
   Operating_FlowRate [ j ]= np . interp ( Operating_DeltaP [ j ] , DeltaP[: , j ] , mSPI [: , j ])


#An Investigation into Hybrid Rocket Injectors

   plt.plot ( DeltaP [: , j ] , mSPI [: , j ] , label ='P1 =%.2 f [MPa]'%( P_1 [ j]/(1E6)))

 Average_FlowRate = np . average ( Operating_FlowRate )

 plt.title ('Single - Phase Incompressible Model ')
 plt.xlabel ('P1 -P2[Pa]')
 plt.ylabel ('Mass Flow Rate [kg/s]')
 plt.grid ()
 plt.legend ()
 plt.show ()

 plt.figure ()
 plt.plot ( P_1 , Operating_FlowRate , label ='P2 =%.2 f [MPa]'%(Operating_P2 /(1E6)))
 plt.title ('Single - Phase Incompressible Model' )
 plt.xlabel ('P1[Pa]')
 plt.ylabel ('Mass Flow Rate [kg/s]')
 plt.grid ()
 plt.legend ()
 plt.ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
 plt.show ()

 print ('The average flow rate is:')
 print ( Average_FlowRate )

 return mSPI , Operating_FlowRate , Operating_DeltaP