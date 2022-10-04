# -* - coding : utf -8 -* -
2 """
3 Created on Tue May 5 15:59:24 2020
4 Transient Equilibrium with regression rate modeling
5 @author : asus
6 """
7
8 # -* - coding : utf -8 -* -
9 """
10 Created on Tue Mar 31 18:05:53 2020
11
12
13 @author : asus
14 """
15 import numpy as np
16 import matplotlib . pyplot as plt
17 from CoolProp . CoolProp import PropsSI
18 from SPI4Dyer_Model import SPI4Dyer_Model
19 from SimpleHEM import simpleHEM
20
21 # input :
22 Cd =0.75 # discharge coefficient
23 Fluid =’N2O ’
24 D_2 =0.002 # injector orifice diameter [m]
25 NumOrifices =28 # number of orifices on injector plate ( Few orifices
will cause long run times )
26 steps =100 # iteration steps for mDyer ( negligable difference from
100 to 1000)
27 timestep =0.010 # seconds for each iteration of outer while loop
28 V =0.03255 # tank volume [m^3]
29 M =20 # mass of tank contents , [kg]
30 T1 =300.86 # Initial Upstream Temperature [K]
92
An Investigation into Hybrid Rocket Injectors
31 Operating_P2 =3 e6 # Operating P2
32 r =50 e -3 # radius of fuel grain port [m]
33 L =0.48 # fuel grain length [m]
34 a =15.5 e -5 # regression rate constant n2o/ paraffin ( from Waxman et al
. , adjusted so regression rate is given in m/s by multiplication
with 10^ -3)
35 n =0.5 # regression rate exponent n2o/ paraffin ( from Waxman et al .)
36 rho_f =900 # fuel density ( paraffin ) [kg/m^3]
37 # --------------------------
38
39 # initial calcs :
40 rho = M / V # overall density ( vapor and liquid )
41 u = PropsSI (’U’,’T’,T1 ,’D’,rho , Fluid ) # specific Internal energy (
vapor and liquid mixture )
42 U = u * M # Internal energy ( vapor and liquid )
43 #A_2 =( np.pi /4)*D_2 **2 # injector orifice cross - sectional area
44 x =( U / M - PropsSI (’U’,’T’,T1 ,’Q’ ,0 , Fluid ) ) /( PropsSI (’U’,’T’,T1 ,’Q’
,1 , Fluid ) - PropsSI (’U’,’T’,T1 ,’Q’ ,0 , Fluid ) ) # initial vapor
quality
45
46
47 Time =0 # start at time =0
48
49 j =0 # initialize iteration counter j for while loop
50 ChokedValue = np . array ([]) # initialize choked flow rate tracker
51 FlowTracker = np . array ([]) # initialize operating flow rate tracker (
flow rate with Operating P_2 )
52 TempVector = np . array ([]) # initialize upstream temperature tracker
53 PressureVector = np . array ([]) # initialize upstream pressure tracker
54 MassVector = np . array ([]) # initialize tank mass tracker
55 TimeVector = np . array ([]) # initialize Time tracker
56
57 # initialize regression rate , fuel flow rate vectors :
58 regRateVector = np . array ([])
59 mdot_fuel_Vector = np . array ([])
60 while x <0.95: # while vapor quality is less than 0.95 , i.e. so long
there is liquid in tank
61 TempVector = np . insert ( TempVector ,j , T1 ) # record temperature in
TempVector
62 TimeVector = np . insert ( TimeVector ,j , Time ) # record Time in
TimeVector
63 MassVector = np . insert ( MassVector ,j , M ) # record mass in MassVector
64
65 P_1 = PropsSI (’P’,’T’,T1 ,’Q’ ,0 , Fluid ) # saturated liquid pressure
66 PressureVector = np . insert ( PressureVector ,j , P_1 ) # record pressure
in PressureVector
67
68 # start solving for mDyer by finding mSPI and mHEM :
69 mSPI = SPI4Dyer_Model ( Fluid , P_1 , Cd , D_2 , steps ) #SPI mass flow rate
70 mHEM = simpleHEM ( Fluid , P_1 , Cd , D_2 , steps ) #HEM mass flow rate
71
72 # Initialize parameters
73 P_2 = np . linspace (100000 , P_1 -1 , steps ) # matches what we used in
HEM
74 DeltaP = np . linspace ( P_1 -100000 ,1 , steps )
75 mDyer = np . zeros ( steps )
76 k =1 # Always = 1 in saturated case
77 mDyerChoked = np . zeros ( steps )
93
An Investigation into Hybrid Rocket Injectors
78
79 #for loop for Dyer model
80 for i in range ( steps ) :
81
82 mDyer [ i ]=((( k * mSPI [ i ]) /(1+ k ) ) +( mHEM [ i ]/(1+ k ) ) )
83
84 criticalIndex = np . where ( mDyer == np .max( mDyer ) ) # index where
critical value occurs .
85 ChokedValue = np . insert ( ChokedValue ,j , np . max( mDyer ) ) # add the
choked value for this j iteration to ChokedValue
86
87 #for loop to account for choked flow
88 for i in range ( steps ) :
89 if i > criticalIndex [0]:
90 mDyerChoked [ i ]= mDyer [ i ]
91 else :
92 mDyerChoked [ i ]= np . max( mDyer )
93
94 #add the operating flow rate for this j iteration to
FlowTracker
95 FlowTracker = np . insert ( FlowTracker ,j , np . interp ( Operating_P2 , P_2 ,
mDyerChoked ) )
96
97
98 #Get the new values of U and M:
99 mDyerTotal = NumOrifices * FlowTracker [ j ]
100 h1 = PropsSI (’H’,’P’,P_1 ,’Q’ ,0 , Fluid ) # calculate enthalpy
101 U =U - mDyerTotal * h1 * timestep # update internal energy ( neglecting
wall heat transfer etc .)
102 M =M - mDyerTotal * timestep # update mass
103
104 # regression rate calcs :
105 A_p = np . pi * r **2 # fuel grain port cross - sectional area
106 A_d =2* np . pi * r * L # fuel grain port surface area ( area available
to heat transfer with flame )
107 G_ox = mDyerTotal / A_p # oxidizer mass flux through port
108 regRate = a *( G_ox **( n ) ) # regression rate equation
109 regRateVector = np . insert ( regRateVector ,j , regRate ) # record
regression rate in vector
110 mdot_fuel = rho_f * A_d * regRate # calculate fuel mass flow rate
111 mdot_fuel_Vector = np . insert ( mdot_fuel_Vector ,j , mdot_fuel ) #
record fuel flow rate
112 r = r + regRate * timestep # update radius
113
114
115 # Start iteration for new T1 , " First round " must be outside
while loop :
116 Tguess = T1 #use previous T as an initial guess for calculating
new T
117 u_l = PropsSI (’U’,’T’, Tguess ,’Q’ ,0 , Fluid ) # liquid specific
internal energy
118 u_v = PropsSI (’U’,’T’, Tguess ,’Q’ ,1 , Fluid ) # vapor specific
internal energy
119 rho_l = PropsSI (’D’,’T’, Tguess ,’Q’ ,0 , Fluid ) # liquid density
120 rho_v = PropsSI (’D’,’T’, Tguess ,’Q’ ,1 , Fluid ) # vapor density
121 x =(( U / M ) - u_l ) /( u_v - u_l ) # vapor quality
122 Vguess = M *(((1 - x ) / rho_l ) + x / rho_v ) # volume constraint
123
94
An Investigation into Hybrid Rocket Injectors
124 error =V - Vguess
125 oldError =1000 # chose some random large value , to force into
oldError > error case for first iteration below ....
126 #... as we expect T1 to drop
127
128
129 while error >0.000001: #Set small enough so that no issues of
T_1 not updating
130 if oldError > error :
131 oldError = error # prepare the current error to be next
iteration ’s oldError
132 Tguess = Tguess -0.01 #- update Tguess .
133 u_l = PropsSI (’U’,’T’, Tguess ,’Q’ ,0 , Fluid ) # liquid
specific internal energy
134 u_v = PropsSI (’U’,’T’, Tguess ,’Q’ ,1 , Fluid ) # vapor specific
internal energy
135 rho_l = PropsSI (’D’,’T’, Tguess ,’Q’ ,0 , Fluid ) # liquid
density
136 rho_v = PropsSI (’D’,’T’, Tguess ,’Q’ ,1 , Fluid ) # vapor
density
137 x =(( U / M ) - u_l ) /( u_v - u_l ) # vapor quality
138 Vguess = M *(((1 - x ) / rho_l ) + x / rho_v ) # volume constraint
139
140 error =V - Vguess # update error
141
142 else :
143 oldError = error # prepare the current error to be next
iteration ’s oldError
144 Tguess = Tguess +0.004 # update Tguess the other way , as
our error has increased .
145 u_l = PropsSI (’U’,’T’, Tguess ,’Q’ ,0 , Fluid ) # liquid
specific internal energy
146 u_v = PropsSI (’U’,’T’, Tguess ,’Q’ ,1 , Fluid ) # vapor specific
internal energy
147 rho_l = PropsSI (’D’,’T’, Tguess ,’Q’ ,0 , Fluid ) # liquid
density
148 rho_v = PropsSI (’D’,’T’, Tguess ,’Q’ ,1 , Fluid ) # vapor
density
149 x =(( U / M ) - u_l ) /( u_v - u_l ) # vapor quality
150 Vguess = M *(((1 - x ) / rho_l ) + x / rho_v ) # volume constraint
151
152 error =V - Vguess # update error
153
154 T1 = Tguess # update T1 for next iteration
155
156 # update vapor quality :
157 u_l = PropsSI (’U’,’T’,T1 ,’Q’ ,0 , Fluid ) # liquid specific internal
energy
158 u_v = PropsSI (’U’,’T’,T1 ,’Q’ ,1 , Fluid ) # vapor specific internal
energy
159 rho_l = PropsSI (’D’,’T’,T1 ,’Q’ ,0 , Fluid ) # liquid density
160 rho_v = PropsSI (’D’,’T’,T1 ,’Q’ ,1 , Fluid ) # vapor density
161 x =(( U / M ) - u_l ) /( u_v - u_l ) # vapor quality te vapor quality
162
163 Time = Time + timestep # update Time
164 j = j +1 # update iteration counter j
165
166 # Remember to include last iteration into our tracking vectors :
95
An Investigation into Hybrid Rocket Injectors
167 TempVector = np . insert ( TempVector ,j , T1 ) # record final temperature in
TempVector
168 TimeVector = np . insert ( TimeVector ,j , Time ) # record final Time in
TimeVector
169 MassVector = np . insert ( MassVector ,j , M ) # record final mass in
MassVector
170 P_1 = PropsSI (’P’,’T’,T1 ,’Q’ ,0 , Fluid ) # record final pressure in
PressureVector :
171 PressureVector = np . insert ( PressureVector ,j , P_1 )
172
173 OFratioVector =( NumOrifices * FlowTracker ) / mdot_fuel_Vector
174
175
176 # Plot flow rate vs time , all orifices combined :
177 plt . plot ( TimeVector [: -1] , NumOrifices * FlowTracker , label =’P_2 =%.2 f [
Mpa]’%( Operating_P2 /(1 e6 ) ) )
178 plt . plot ( TimeVector [: -1] , NumOrifices * ChokedValue , label =’Choked ,
P_2 =%.2 f [Mpa]’%( Operating_P2 /(1 e6 ) ) )
179 plt . title (’Dyer mass flow rate time history for Transient
Equilibrium Model ’)
180 plt . xlabel (’Time [s]’)
181 plt . ylabel (’Mass Flow Rate [kg/s]’)
182 plt . grid ()
183 plt . legend ()
184 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
185 plt . show ()
186
187 # Plot flow rate vs upstream pressure (for comparisons etc .)
188 plt . figure
189 plt . plot ( PressureVector [: -1] , FlowTracker , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
190 plt . plot ( PressureVector [: -1] , ChokedValue , label =’Choked , P_2 =%.2 f [
Mpa]’%( Operating_P2 /(1 e6 ) ) )
191 plt . title (’Dyer mass flow rate plotted against P1 for Transient
Equilibrium Model ’)
192 plt . xlabel (’P_1 [Pa]’)
193 plt . ylabel (’Mass Flow Rate [kg/s]’)
194 plt . grid ()
195 plt . legend ()
196 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
197 plt . show ()
198
199 # plot Pressure vs time
200 plt . figure
201 plt . plot ( TimeVector , PressureVector , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
202 plt . title (’Pressure time history for Transient equillibrium model ’)
203 plt . ylabel (’P_1 [Pa]’)
204 plt . xlabel (’Time [s]’)
205 plt . grid ()
206 plt . legend ()
207 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
208 plt . show ()
209
210 # plot Temperature vs time
211 plt . figure
212 plt . plot ( TimeVector , TempVector , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
96
An Investigation into Hybrid Rocket Injectors
213 plt . title (’ Temperature time history for Transient equillibrium
model ’)
214 plt . ylabel (’T_1 [K]’)
215 plt . xlabel (’Time [s]’)
216 plt . grid ()
217 plt . legend ()
218 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
219 plt . show ()
220 # plot mass vs time
221 plt . figure
222 plt . plot ( TimeVector , MassVector , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
223 plt . title (’Mass plotted against time using Transient equillibrium
model ’)
224 plt . xlabel (’Time [s]’)
225 plt . ylabel (’Mass [kg]’)
226 plt . grid ()
227 plt . legend ()
228 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
229 plt . show ()
230
231 # plot regression rate vs time :
232 plt . figure
233 plt . plot ( TimeVector [: -1] , regRateVector , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
234 plt . title (’Regression rate plotted against time using Transient
equillibrium model ’)
235 plt . xlabel (’Time [s]’)
236 plt . ylabel (’Regression rate [m/s]’)
237 plt . grid ()
238 plt . legend ()
239 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
240 plt . show ()
241
242 # plot fuel flow rate vs time :
243 plt . figure
244 plt . plot ( TimeVector [: -1] , mdot_fuel_Vector , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
245 plt . title (’Fuel mass flow rate plotted against time using Transient
equillibrium model ’)
246 plt . xlabel (’Time [s]’)
247 plt . ylabel (’Fuel mass flow rate [kg/s]’)
248 plt . grid ()
249 plt . legend ()
250 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
251 plt . show ()
252
253 # plot O/F ratio vs time :
254 plt . figure
255 plt . plot ( TimeVector [: -1] , OFratioVector , label =’P_2 =%.2 f [Mpa]’%(
Operating_P2 /(1 e6 ) ) )
256 plt . title (’O/F ratio plotted against time using Transient
equillibrium model ’)
257 plt . xlabel (’Time [s]’)
258 plt . ylabel (’O/F ratio ’)
259 plt . grid ()
260 plt . legend ()
261 plt . ticklabel_format ( axis ="x", style ="sci", scilimits =(0 ,0) )
97
An Investigation into Hybrid Rocket Injectors
262 plt . show ()
263
264 # Calculate and print average flow rate , regression rate
265 AverageFlowRate = np . average ( FlowTracker ) # single orifice
266 TotalAverageFlowRate = NumOrifices * AverageFlowRate #all orifices
combined
267 AvgFuelFlowrate = np . average ( mdot_fuel_Vector ) # fuel flow rate
268 AvgRegrate = np . average ( regRateVector ) # average regression rate
269 print (’the average oxidizer flow rate is [per orifice , total ]: ’)
270 print ( AverageFlowRate , TotalAverageFlowRate )
271 print (’The average fuel mass flow rate is:’)
272 print ( AvgFuelFlowrate )
273 print (’the average regression rate is:’)
274 print ( AvgRegrate )
