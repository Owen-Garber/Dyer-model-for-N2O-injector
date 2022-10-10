import math
print("********************hole geometry************************")

hole_number=12 #from dyer model
D_2=.00157 #[m] from RPE
thickness_of_orifice_plate=.00635 #[m] = .25 inches
countersink_max_diameter=1.2*D_2 #from nasa injector reference pg 38. assumed to be half as effective as a rounded entrance radius, 1.2 maximizes Cd.
print(hole_number, "holes needed of size", D_2, "[m] with a countersink at the entrance")
Countersink_angle = 90
print("the angle of the countersink will be", Countersink_angle, "degrees. So each side of the bore hole will be 45 degrees from perpendicular to plate surface")
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
angle_first_ring = 70 #degrees, 60 produces ideal characteristics, from https://ntrs.nasa.gov/citations/19760023196,
print("the angle of the first hole ring will be ", angle_first_ring, "degrees from the surface of the orifice plate")
impingement_point_y_coord=(diameter_hole_ring_1/2)*math.tan(math.radians(angle_first_ring)) #want to be around 5-7 * D_2
ideal_impingement_point_y_coord = 6*D_2*math.sin(math.radians(angle_first_ring)) # from https://ntrs.nasa.gov/citations/19760023196 pg 29. 
print("ideal impingement point is ", ideal_impingement_point_y_coord, "below the bottom of the orifice plate")
print("which is the y component of an angled jet ")
print("the holes will impinge at ", impingement_point_y_coord, "[m] from the **top** of the orifice plate")
angle_second_ring = math.atan(impingement_point_y_coord/(diameter_hole_ring_2/2)) #radians, just using geometry
angle_second_ring=math.degrees(angle_second_ring) #converted to degrees
print("the angle of the second hole ring will be ", angle_second_ring, "degrees from the surface of the orifice plate")
print("so that the two rings of holes impinge at the same point below the orifice plate")


print("********************diffuser geometry************************")
max_angle_diffuser=10 #degrees, from page 48 of liquid rocket engine injectors by NASA. NASA says no greater than 15 degrees, being safe. https://ntrs.nasa.gov/citations/19760023196
print("the max angle of the diffuser is ", max_angle_diffuser, "degrees from vertical plane")
