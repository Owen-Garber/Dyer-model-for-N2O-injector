def inputs():
    Cd = 0.76 #coefficient of discharge, a factor in flow rate through oriface. From table 8-2 RPE
    D_2 = 0.00157 #[m] diameter of each orifiace
    P_upstream =  5.137E6 # [Pa] Vapor pressure of nitrous at 70F. I DONT LIKE THIS, SHOULD SEE WHAT HYBRID MATLAB CODE USES SINCE WE'LL BE ABOVE 70F AT COMPETITION
    P_downstream = 2.413E6 #[pP] (from MATLAB Hybrid Motor Design Tool) (our combustion chamber pressure, 350 psi)
    steps = 1000 #steps in the iterative integration process, to be kept common in each file to be used
    Fluid = 'N2O'# to be put into coolprop, must be entered like this
    Pressure_Drop= ?????
    Rings_of_Holes = 2 #arbitrary
    ID_of_oriface_plate = 0.3 # [m] arbitrary
    return Cd,D_2, P_upstream, P_downstream, steps, Fluid, Pressure_Drop, Hole_Ring_1_Radius, Hole_Ring_2_Radius, Hole_Ring_3_Radius, Spacing_Btwn_Each_Hole
