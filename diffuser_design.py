def diffuser_design():
    ID_nozzle_injector = # at inlet
    orifface_plate_ID = # edge of plate itself that is exposed to flow
    max_angle_of_diffuser = #in order to not cause flow seperation, want to keep low turbulence
    height_of_diffuser = (orrifface_plate_ID-ID_nozzle_injector)/tan(max_angle_of_diffuser) #y-axis
    return height_of_diffuser