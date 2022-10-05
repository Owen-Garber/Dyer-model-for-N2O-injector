Note by Owen Garber:

All code is based on An Investigation into Hybrid Rocket Injectors: 

https://ntnuopen.ntnu.no/ntnu-xmlui/bitstream/handle/11250/2779621/no.ntnu:inspera:57317709:20929650.pdf?sequence=1

The Problem: using a single phase, incompressible flow model is highly innacurate for nitrous oxide, which is both 2-phase flow, and compressible
The larger problem is 2-phase flow. 

Code is provided in the linked paper above, which we will attempt to adjust some inputs for our application,
to have a better model with which to design the injector around.

The Dyer model is the best model we currently have to model mass flow rate of nitrous oxide. It is based on the HEM 
(homogenous equilibrium model) and SPI (single phase incompressible) models, plus some adjustment factors.

All code is in python, most notably using cool prop, a package that gives thermodynamic properties of substances. 
***anyone who wants to use the code, do so on your own laptop, as you need packages you can't get on python on remote desktop. 
I used PyCharm, then set my python interpretter as just the filepath being the location of python in my computer, then download the packages called "coolprop", "numpy", and "matplotlib"**********


DESIGN FACTORS:
we will be designing using the following information about orrifices:
(FROM : pg 279, RPE, Table 8-2) (We will use a conical (chamfer) entrance to our hole, for ease of manufacturing)

	Cd=0.76  (given reference value from table)
	D_orriface = 1.57 mm = .00157m (given reference value from table)

We will use the following information about nitrous oxide, and our combustion chamber:

	PvaporN2O=745psig @ 70F = 5.137E6 Pa (google) - I DONT LIKE THIS, SHOULD SEE WHAT HYBRID MATLAB CODE USES SINCE WELL BE ABOVE 70F
	Operating_P2=Pcombustion chamber = 350psi = 2.413E6 pa (from MATLAB Hybrid Motor Design Tool)

	Ptank @end of burn = 550 psi = 3.792E6 Pa (according to MATLAB Hybrid Motor Design Tool)
	
	Target Mass flow rate = M_dot_avg_target = ????????????? (should be in MATLAB motor design tool)

**************The ultimate output we want from this script, the number of holes, determined by average flow rate (of oxidizer), and the targete mass flow rate, 
is given in the output of the Dyer model script******************************
**********The most relevent files to use are Dyer_model (contains the output we want), and function files, containing functions we want: SPI4Dyer_Model, SimpleHEM, SPI_model, HEM*************************** 
	
