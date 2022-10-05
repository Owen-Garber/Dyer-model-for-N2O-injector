Cd = 0.76 #coefficient of discharge, a factor in flow rate through oriface. From table 8-2 RPE
D_2 = 0.00157 #[m] diameter of each orifiace
P_upstream =  5.137E6 # [Pa] Vapor pressure of nitrous at 70F. I DONT LIKE THIS, SHOULD SEE WHAT HYBRID MATLAB CODE USES SINCE WE'LL BE ABOVE 70F AT COMPETITION
P_downstream = 2.413E6 #[pP] (from MATLAB Hybrid Motor Design Tool) (our combustion chamber pressure, 350 psi)
steps = 1000 #steps in the iterative integration process, to be kept common in each file to be used
Fluid = 'N2O'