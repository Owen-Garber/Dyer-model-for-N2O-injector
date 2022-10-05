# -* - coding : utf -8 -* -
"""
Created on Mon Dec 9 15:24:27 2019
Dyer Model

 Made for use with N2O or CO2

 This basic version is meant to be used for saturated liquid
upstream , no supercharge .
 To get supercharged , some changes would have to be made to SPI and
HEM models , but this is not currently relevant for Propulse

 Note that P_2 ranges from 1/5.2 bar . this is because the CoolProp
fails in HEM model for very small values of P2.
 This has to do with the triple point of the fluid , see HEM for
details .

 Also note that P_2 ends at P_1 - 1 instead of P_1 . This is because
we otherwise divide by 0 in the calculation of k.

~~ means OWEN EDITED
** Needs to be edited still maybe
 @author : Jonas
 """
import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
from SPI4Dyer_Model import SPI4Dyer_Model
from SimpleHEM import simpleHEM
from SPI_Model import SPI_Model
from HEM import HEM

# Example Input :
Cd =0.76 # ~~Discharge Coefficient from RPE
D_2 =.00157 # ~~Injector Orfice Diameter to be designed around (la( should be 1 -2 mm) [m]
Fluid ='N2O'# ~~Fluid - both N2O and CO2 can be used .
steps =1000 # Number of steps in each iteration of mHEM & mSPI
P1 = np.linspace(6E6 ,2.416E6 ,10) # ~~linear upstream pressure drop from 60 bar to 40 bar [Pa] **Not sure what the 10 is ** not sure if the 2.416e6 is right, that is 350PSI
Operating_P2 =2.413E6 # ~~operating pressure in burn chamber ( assumed constant )
M_dot_avg_target = 2 #[kg/s]
#-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

FlowTracker = np.zeros(len(P1)) # tracks of flowrate at P2= Operating P2 for different P1 iterations
ChokedValue = np.zeros(len(P1)) # tracks value of critical flow for different P1 iterations

for j in range (len( P1 ) ) :
 P_1 = P1 [ j ] # #~~ tabbed it, Upstream pressure for this iteration
#Get mSPI
 mSPI = SPI4Dyer_Model ( Fluid , P_1 , Cd , D_2 , steps ) #~~ tabbed it
#Get mHEM
 mHEM = simpleHEM ( Fluid , P_1 , Cd , D_2 , steps ) #~~ tabbed it
#An Investigation into Hybrid Rocket Injectors
# Initialize parameters
 P_v = P_1 # saturated case #~~ tabbed it
 P_2 = np . linspace (100000 , P_1 -1 , steps ) #~~ tabbed it # matches what we used in HEM

 if Fluid == 'N2O':# See introduction text above for explaination
  DeltaP = np . linspace ( P_1 -1E5 ,1 , steps ) #~~ tabbed it
  P_2 = np . linspace (1E5 , P_1 -1 , steps )#~~ tabbed it
 else :
  DeltaP = np . linspace ( P_1 -5.2E5 ,1 , steps )#~~ tabbed it
  P_2 = np . linspace (5.2E5 , P_1 -1 , steps )#~~ tabbed it
 mDyer = np . zeros ( steps )#~~ tabbed it
 k =0#~~ tabbed it
 mDyerChoked = np . zeros ( steps )#~~ tabbed it

 #for loop for Dyer model
 for i in range ( steps ) :
  k = np . sqrt (( P_1 - P_2 [ i ]) /( P_v - P_2 [ i ]) ) ##~~ tabbed it, In saturated case this will always be 1...
  mDyer [ i ]=((( k * mSPI [ i ]) /(1+ k ) ) +( mHEM [ i ]/(1+ k ) ) )

 criticalIndex = np . where ( mDyer == np .max( mDyer ) ) # index where critical value occurs .

 ChokedValue [j]= np.max(mDyer)
 #for loop for choked flow
 for i in range ( steps ) :
  if i > criticalIndex [0]:
   mDyerChoked [ i ]= mDyer [ i ]
  else :
   mDyerChoked [ i ]= np .max( mDyer )
 """
plot against P2 if desired :

plt . plot (P_2 , mDyerChoked , ’b ’,label = ’P1 =%.2 f [MPa ] ’%( P_1 /(1 e6)))
plt . plot (P_2 ,mDyer , ’b- - ’)
plt . title ( ’ Dyer Model ’)
plt . xlabel ( ’P2[Pa ] ’)
plt . ylabel ( ’ Mass Flow Rate [kg/s] ’)
plt . grid ()
plt . legend ()
plt . ticklabel_format ( axis ="x" , style =" sci" , scilimits =(0 ,0))
plt . show ()
print (np.max( mDyer ))
"""

 # plt.plot(DeltaP,mDyerChoked,'b', label='P1 =%.2f [MPa]' %(P_1/(1E6)))
 # plt.plot(DeltaP,mDyer,'b--')
 # plt.title('Dyer Model')
 # plt.xlabel ('P1 -P2 [Pa]')
 # plt.ylabel ('Mass Flow Rate [kg/s]')
 # plt . grid ()
 # plt . legend ()
 # plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
 # plt . show ()
 FlowTracker [ j ]= np . interp ( Operating_P2 , P_2 , mDyerChoked )


# plt.plot(P1,FlowTracker,label='P_2=%.2f [Mpa]'%(Operating_P2/(1E6)))
# plt.plot(P1,ChokedValue,label='Choked, P_2=%.2 f [Mpa]'%(Operating_P2/(1E6)))
# plt . title ('Dyer model with linear upstream pressure drop')
# plt . xlabel ('P_1 [Pa]')
# plt . ylabel ('Mass Flow Rate [kg/s]')
# plt . grid ()
# plt . legend ()
# plt.ticklabel_format(axis ="x",style ="sci", scilimits =(0,0))
# plt . show ()
AverageFlowRate = np . average ( FlowTracker )
print ( "chocked flow value is [kg/s] : ",ChokedValue )
print ( "FlowTracker is [kg/s] : ",FlowTracker )
print ("AverageFlowRate is [kg/s] : ", AverageFlowRate )
print ("*****Needed Number of Holes of Given Diameter: ", D_2, " [m]  to achieve target oxidizer mass flow rate is: ", M_dot_avg_target/AverageFlowRate, "holes*****")

########################HAVE IT RETURN THE NUMBER OF HOLES, hole_number####################################
