# -* - coding : utf -8 -* -
"""
3 Created on Tue Dec 3 18:12:56 2019
4 THIS IS ALL PRE CHANGE BY OWEN
5 Homogenous Equillibrium Model
6
7 Only one case at a time here for simplicity
8
9 ----- -------- --------- -------- --------- -------- -------- ----
10 Note that for P_2 , the lower value has been set to 1 & 5.2 bar (for
N2O and CO2 respectively ) as very low values
11 caused issues with the entropy calcs .
12
13 "It should be noted that CO2 , due to it ’s high triple point
pressure cannot exist in
14 liquid phase at pressures below that of it ’s triple point pressure
of 517.95 kPa . At any
15 pressure below this value , the CO2
16 ow would consist of solid - vapor mixture . It is for this
17 reason that CO2 exists as a "Dry Ice " at atmospheric pressure and
temperature ."
18
19 Presumably similar story for N2O. ( triplepoint at 87.85 kPa)
20 --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- --
21
22 P_2 is set to go up to P1 -1 as we otherwise get a division by 0
when implemented in the Dyer model
23
24 @author : Jonas
25 """

"""changed things to be N2O properties"""

import numpy as np
import matplotlib . pyplot as plt
from CoolProp . CoolProp import PropsSI

# input example :
Cd =0.76 # Discharge Coefficient
D_2 =.00157 # Injector Orfice Diameter
P_1 =5.137E6 # Upstream pressure (vapor pressure of N2O at 70F) [Pa]
Fluid ='N2O'# Fluid
steps =1000 # Number of steps in iteration below

# begin function
def simpleHEM ( Fluid , P_1 , Cd , D_2 , steps ) :
# initilaze parameters :
    rho_2 = np . zeros ( steps ) # downstream density
    h_2 = np . zeros ( steps ) # downstream enthalpy
    if Fluid == 'CO2': # See green text on top for explaination of if statement. DONT DELETE THIS PLS, EVEN IF USING N2O
        P_2 = np . linspace (5.2E5 , P_1 -1 , steps )
    else :
        P_2 = np . linspace (1E5 , P_1 -1 , steps )

    mHEM = np . zeros ( steps )
    mHEMchoked = np . zeros ( steps )
# Initial calculations :
    A_2 =( np . pi /4) * D_2 **2
    s_1 = PropsSI ('S','P',P_1 ,'Q' ,0 , Fluid ) # Using saturated liquid upstream (Q=0 in coolProp, no heat transfer )
    s_2 = s_1 # follow line of constant entropy
    h_1 = PropsSI ('H','P',P_1 ,'Q' ,0 , Fluid )
#for loop for graph that follows model exactly
    for i in range ( steps ) :
        rho_2 [ i ]= PropsSI ('D','P', P_2 [ i ] ,'S',s_2 , Fluid )
        h_2 [ i ]= PropsSI ('H','P', P_2 [ i ] ,'S',s_2 , Fluid )
        mHEM [ i ]= Cd * A_2 * rho_2 [ i ]* np . sqrt (2*( h_1 - h_2 [ i ]) )
    criticalIndex = np . where ( mHEM == np .max( mHEM ) ) # find index location of max flow rate
#for loop for graph where the choked flow will show
    for i in range ( steps ) :
        if i > criticalIndex [0]:
            mHEMchoked [ i ]= mHEM [ i ]
        else :
            mHEMchoked [ i ]= np .max( mHEM )
    return mHEM
# plot results :
    plt . plot ( P_2 , mHEMchoked ,'b', label ='P1 =%.2 f [MPa]'%( P_1 /(1E6) ) )
    plt . plot ( P_2 , mHEM ,'b- -')
    plt . title ('Homogenous Equillibrium Model')
    plt . xlabel ('P2 [Pa]')
    plt . ylabel ('Mass Flow Rate [kg/s]')
    plt . grid ()
    plt . legend ()
    plt . show ()
    print ( np .max( mHEM ) )
