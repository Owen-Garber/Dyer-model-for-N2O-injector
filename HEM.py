# -* - coding : utf -8 -* -
"""
Created on Tue Feb 11 17:36:06 2020

@author : asus
"""
# -* - coding : utf -8 -* -
"""
Created on Tue Dec 3 18:12:56 2019

Homogenous Equillibrium Model
subscript 1 denotes upstream of injector , assumed to be equal to
tank
subscript 2 denotes downstream of injector

Note that for P_2 , the lower bound has been set to ( slightly above )
the triple point pressure as very low values caused issues with
the entropy calcs
Also , P_2 is set to go up to P1 -1 as we otherwise get a division by
0 in the Dyer model

@author : Jonas
"""

import numpy as np
import matplotlib . pyplot as plt
from CoolProp . CoolProp import PropsSI
# input example :
Cd =0.9 # Discharge Coefficient
D_2 =.00157 # Injector Orfice Diameter [m]
Fluid ='N2O' # nitrous oxide
steps =100 # Number of steps in iterations in mass flow calc for each P_1
Operating_P2 =3E6 # Operating pressure in burnchamber , the value we are interested in.
P_1 = np . linspace (6E6 ,4E6 ,100) # linear upstream pressure vector

# begin function
def HEM ( Fluid , P_1 , Cd , D_2 , steps , Operating_P2 ) :
# initilaze parameters :
    number_graphs =len( P_1 )
    rho_2 = np . zeros (( number_graphs , steps ) ) # density
    h_2 = np . zeros (( number_graphs , steps ) ) # enthalpy
    mHEM = np . zeros (( number_graphs , steps ) ) # Mass flow rate
    mHEMchoked = np . zeros (( number_graphs , steps ) ) # Mass flow rate when adjusting for choked flow
    CriticalFlowRate = np . zeros ( number_graphs ) # Track value of critical flow rate for each graph

    ActualFlowRate = np . zeros ( number_graphs ) # Track value of flow rate at Operating_P2 for each graph
    A_2 =( np . pi /4) * D_2 **2 # injector area

    for j in range ( number_graphs ) :
# Initial calculations :
        s_1 = PropsSI ('S','P', P_1 [ j ] ,'Q' ,0 , Fluid ) # Using saturated liquid upstream (Q=0 in coolProp )
        s_2 = s_1 # follow line of constant entropy
        h_1 = PropsSI ('H','P', P_1 [ j ] ,'Q' ,0 , Fluid )
#P_2=np. linspace (100000 , P_1[j] -1 , steps )
        if Fluid == 'CO2': #See text on top of code for explaination of if statement
            P_2 = np . linspace (5.2E5 , P_1 [ j ] -1 , steps )
        else:
            P_2 = np . linspace (1E5 , P_1 [ j ] -1 , steps )

#for loop for graph that follows model exactly
        for i in range ( steps ) :
            rho_2 [j , i ]= PropsSI ('D','P', P_2 [ i ] ,'S',s_2 , Fluid ) #use downstream pressure & entropy to find density
            h_2 [j , i ]= PropsSI ('H','P', P_2 [ i ] ,'S',s_2 , Fluid ) #use downstream pressure & entropy to find enthalpy
            mHEM [j , i ]= Cd * A_2 * rho_2 [j , i ]* np . sqrt (2*( h_1 - h_2 [j , i ]) ) #mass flow rate

        flow_tracker = mHEM [j ,:]
        criticalIndex = np . where ( flow_tracker == np .max( flow_tracker )) # find index location of max flow rate

#for loop for graph where the choked flow will show
        for i in range ( steps ) :
            if i > criticalIndex [0]:
                mHEMchoked [j , i ]= mHEM [j , i ]
            else :
                mHEMchoked [j , i ]= np .max( flow_tracker )

# plot results : (can also plot flow rate vs p_2 if desired )
        plt . plot ( P_1 [ j ] - P_2 , mHEMchoked [j ,:] , 'b', label ='P1 =%.2 f [MPa]'%( P_1 [ j ]/(1E6 ) ) )
        plt . plot ( P_1 [ j ] - P_2 , mHEM [j ,:] , 'b- -')
        plt . title ('Homogenous Equillibrium Model')
        plt . xlabel ('P1 -P2 [Pa]')
        plt . ylabel ('Mass Flow Rate [kg/s]')
        plt . grid ()
        plt . legend ()
        plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0))
        plt . show ()

        ActualFlowRate [ j ]= np . interp ( Operating_P2 , P_2 , mHEMchoked [j,:])
        CriticalFlowRate [ j ]= np .max ( mHEM [j ,:])
        if ActualFlowRate [ j ]!= CriticalFlowRate [ j ]:
            print ('Flow not choked')
 # plot operating & critical flow rate vs p1 after all iterations are complete
        plt . plot ( P_1 , ActualFlowRate , label ='P_2 =%.2 f [Mpa]'%(Operating_P2 /(1E6 ) ) )
        plt . plot ( P_1 , CriticalFlowRate ,'r- -', label ='Choked , P_2 =%.2 f [Mpa]'%( Operating_P2 /(1E6 ) ) )
        plt . title ('Homogenous Equillibrim model for linear upstreampressure')
        plt . xlabel ('P_1 [Pa]')
        plt . ylabel ('Mass Flow Rate [kg/s]')
        plt . grid ()
        plt . legend ()
        plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
        plt . show ()

        AverageFlowRate = np . average ( ActualFlowRate )
        return CriticalFlowRate , ActualFlowRate , AverageFlowRate