# -* - coding : utf -8 -* -
"""
@author : Jonas

Perfect gas model

Calculates mass flow rates using the Perfect Gas model
"""

import numpy as np
import matplotlib . pyplot as plt
from CoolProp . CoolProp import PropsSI


# Input Example :
Cd =0.9 # Discharge Coefficient
D_2 =0.00157 #[m]
P_1 = np.array ([5.05E6 , 4.6E6 ,3E6 ]) #[ Pascal ] NOTE : MAX 6 plots can be displayed !
T_1 =293 #[ Kelvin ] Care : pick such that fluid is in gaseous region for your pressure , see phase diagram .
Fluid ='N2O' # Must be such that CoolProp understands !
steps = 100 # iteration steps in mass flow calc
# Function starts here #
def PerfectGasModel ( Fluid , T_1 , P_1 , D_2 , Cd ) :

    number_graphs =len( P_1 )
    P_ratio = np . linspace (0 ,1 , steps )
    size =len (P_ratio)

# initialize mass flow , critical values and property arrays :
    mModel = np . zeros (( size , number_graphs ) ) # will be shown in dashed line , follows PG mass flow model
    mPG = np . zeros (( size , number_graphs ) ) #" actual " mass flow using PG model but taking choked flow into account
    P_ratio_crit = np . zeros ( number_graphs ) # critical pressure ratio
    mCrit = np . zeros ( number_graphs ) # critical mass flow ratio
    rho_1 = np . zeros ( number_graphs ) # density upstream

# heat capacities and ratio :
    Cp = np . zeros ( number_graphs )
    Cv = np . zeros ( number_graphs )
    k = np . zeros ( number_graphs )

    A_2 =( np . pi /4) * D_2 **2 # Calculate orifice Area

# begin first for loop - each iteration gives mass flow for a new P_1
    for j in range ( number_graphs ) :
# Calculate remaining thermodynamic properties , enforcing gaseous phase .
        rho_1 [ j ]= PropsSI ('D','T',T_1 , 'P|gas', P_1 [ j ] , Fluid )
        Cp [ j ]= PropsSI ('C','T',T_1 , 'P|gas',P_1 [ j ] , Fluid )
        Cv [ j ]= PropsSI ('O','T',T_1 , 'P|gas', P_1 [ j ] , Fluid )
        k [ j ]= Cp [ j ]/ Cv [ j ]


# find critical values
        P_ratio_crit [ j ]=(2/( k [ j ]+1) ) **( k [ j ]/( k [ j ] -1) )
        mCrit [ j ]= Cd * A_2 * rho_1 [ j ]* np . sqrt (2* Cp [ j ]* T_1 *(( P_ratio_crit[ j ]) **(2/ k [ j ]) -( P_ratio_crit [ j ]) **(( k [ j ]+1) / k [ j ]) ) )

# begin for loop for each P_ratio to calculate mass flow rate
        for i in range ( size ) :
            if P_ratio [ i ] > P_ratio_crit [ j ]:
                mPG [i , j ]= Cd * A_2 * rho_1 [ j ]* np . sqrt (2* Cp [ j ]* T_1 *((P_ratio [ i ]) **(2/ k [ j ]) -( P_ratio [ i ]) **(( k [ j ]+1) / k [ j ]) ) )
            else :
                mPG [i , j ]= mCrit [ j ]
            mModel [i , j ]= Cd * A_2 * rho_1 [ j ]* np . sqrt (2* Cp [ j ]* T_1 *((P_ratio [ i ]) **(2/ k [ j ]) -( P_ratio [ i ]) **(( k [ j ]+1) / k [ j ]) ) )

# Begin plot
        colors =[ 'r','b','g','m','y','c']
        dashcolors =[ 'r- -','b- -','g- -','m- -','y- -','c- -']
        plt . plot ( P_ratio , mPG [: , j ] , colors [ j ] , label ='P1 =%.2 f [MPa]'%( P_1 [ j ]/(1E6 ) ) )
    plt . plot ( P_ratio , mModel [: , j ] , dashcolors [ j ])
# finish plot
    plt . title ('Perfect Gas Model')
    plt . xlabel ('P2/P1')
    plt . ylabel ('Mass Flow Rate [kg/s]')
    plt . grid ()
    plt . legend ()

    plt . show ()
