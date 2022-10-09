import math
print("********************hole geometry************************")

hole_number=12 #from dyer model
D_2=.00157 #[m] from RPE
print(hole_number, "holes needed of size", D_2, "[m] with a countersink at the entrance")
outer_diameter_of_orifice_plate=0.0381 #[m] = 1.5 [in]
diameter_hole_ring_1=outer_diameter_of_orifice_plate/3
print("the diameter of the most inner ring of holes will be ", diameter_hole_ring_1, "[m]")
diameter_hole_ring_2=(2*outer_diameter_of_orifice_plate)/3
print("the diameter of the second most inner ring of holes will be ", diameter_hole_ring_2, "[m]")
circumference_hole_ring_1 = math.pi*diameter_hole_ring_1
circumference_hole_ring_2 =math.pi*diameter_hole_ring_2
ratio_of_circumferences = circumference_hole_ring_2/circumference_hole_ring_1
print("the ratio of circumferences of the two inner hole rings is", ratio_of_circumferences)
number_holes_ring_1 = 4
print("the number of holes in the most inner ring of holes will be ", number_holes_ring_1)
print("thus, there will be two times as many holes in the 2nd most inner ring of holes to keep enough spacing")
number_holes_ring_2=8
print("the number of holes in the most inner ring of holes will be ", number_holes_ring_2)
angle_first_ring = 60 #degrees, from NASA injector reference.pdf, 
print("the angle of the first hole ring will be ", angle_first_ring, "degrees from the surface of the orifice plate")
impingement_point_y_coord=(diameter_hole_ring_1/2)*math.tan(angle_first_ring)
print("the holes will impinge at ", impingement_point_y_coord, "[m] from the **top** of the orifice plate")
angle_second_ring = math.atan(impingement_point_y_coord/(diameter_hole_ring_2/2)) #radians, just using geometry
angle_second_ring=math.degrees(angle_second_ring) #converted to degrees
print("the angle of the second hole ring will be ", angle_second_ring, "degrees from the surface of the orifice plate")
print("so that the two rings of holes impinge at the same point below the orifice plate")


print("********************diffuser geometry************************")
max_angle_diffuser=5 #degrees, arbitrary currently
ID_inlet_injector= .00635 #[m]
height_of_diffuser=(outer_diameter_of_orifice_plate-ID_inlet_injector)/(math.degrees(math.tan(max_angle_diffuser)))
print("the required height from bottom of inlet to top of orifice plate at ", max_angle_diffuser, "degrees from vertical is ", height_of_diffuser, "[m]")
print(outer_diameter_of_orifice_plate-ID_inlet_injector)
print(math.degrees(math.tan(max_angle_diffuser)))
