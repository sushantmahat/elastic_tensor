# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 12:09:56 2019


A new scan surface with limited functionality that goes over a range of elastic 
constant values.

modelled heavily after the scansurface.py code
@author: Sushant Mahat
"""



import christoffel
import numpy as np
import ConfigParser



print 'Reading data and settings from the sound2.in file.'
config = ConfigParser.ConfigParser()
config.read('sound2.in')

#Takes in a different file called sound2.






stiffness_tensor = map(float, config.get('SCAN', 'stiffness').split())
stiffness_tensor = np.reshape(stiffness_tensor, (6, 6))


stepC11 = config.getfloat('SCAN', 'stepC11')
stepC12 = config.getfloat('SCAN', 'stepC12')
stepC44 = config.getfloat('SCAN', 'stepC44')

C11Rng = config.getfloat('SCAN', 'C11Range')
C44Rng = config.getfloat('SCAN', 'C44Range')
C12Rng = config.getfloat('SCAN', 'C12Range')

velExp = map(float, config.get('SCAN', 'velocity').split())
#Gets the experimental velocity to compare against calculated values


#experimental velocity


numC11 = int(C11Rng/stepC11)
numC44 = int(C44Rng/stepC44)

# An error in reading the tensor or density should crash the script.
# Can't do anything without a stiffness tensor.
stiffness_tensor = map(float, config.get('SCAN', 'stiffness').split())
stiffness_tensor = np.reshape(stiffness_tensor, (6, 6))

#stiffness_tensor[2,2] = 500



density = config.getfloat('SCAN', 'density') #kg/m^3

# Creation of the central Christoffel object
chris = christoffel.Christoffel(stiffness_tensor, density)


#the next few section for direction and theta will be zero for my purpose.
#keeping them in in case the rest of the code is dependent on thse definitions.
#Read in rotation information if present
try:
    zdir = map(float, config.get('SCAN', 'zdir').split())
except:
    zdir = None
try:
    xdir = map(float, config.get('SCAN', 'xdir').split())
except:
    xdir = None

#Read special directions if present
try:
    directions = map(float, config.get('SCAN', 'directions').split())
    directions = np.reshape(directions, (len(directions)/3, 3))
except:
    directions = []

#Read grid density for the scan
try:
    num_theta = config.getint('SCAN', 'numtheta')
    total_num_phi = config.getint('SCAN', 'numphi')
except:
    num_theta = 0
    total_num_phi = 0

print 'Data read and Christoffel object created.\n'



print 'Calculating phase velocities in user-defined directions.'
#Loop over user-defined directions


C11_old =  stiffness_tensor[0,0]
C44_old =  stiffness_tensor[4,4]

direction_plt_name = 'C11_' + str(C11_old) + 'C44_' + str(C44_old) + '_direction_plt'

direction_file = open('C11_directions', 'w')
direction_curtailed = open('C11_fit_directions_lim', 'w')
direction_plt = open(direction_plt_name, 'w')
#name of the output file

compare_val = 1

for i in range(numC11):
    C11 = C11_old + i * stepC11 
    stiffness_tensor[0,0] = C11
    stiffness_tensor[1,1] = C11
    stiffness_tensor[2,2] = C11
#    stiffness_tensor[1,2] = C12
#    stiffness_tensor[2,0]  =C12
#    stiffness_tensor[2,1] = C12
      
    for j in range(numC44):
        C44 = C44_old + j * stepC44
        
        stiffness_tensor[3,3] = C44
        stiffness_tensor[4,4] = C44
        stiffness_tensor[5,5] = C44
        #print stiffness_tensor
        chris = christoffel.Christoffel(stiffness_tensor, density)
        direction_file.write('C11:\t' + str(C11) + '  \t C44:\t' + str(C44) + '\n' + '\n')
        direction_curtailed.write('C11:' + str(C11) + ' \t C44:' + str(C44) + '\n')
        
        count = 0
        average_val = 0
        
        for q in directions:
            
            chris.set_direction_cartesian(q)
            velocity = chris.get_phase_velocity()
            direction_curtailed.write('Direction\t' + str(count+1)+ '\t' + str(velocity[2]) + '\t' + str(velocity[2]-velExp[count])+ '\n')
            average_val = average_val + abs(velocity[2]-velExp[count])
            direction_file.write('Direction:\t' + str(q[0]) + '\t' + str(q[1]) + '\t' + str(q[2]) + '\n')
            direction_file.write(' Primary 1:\t ' + str(velocity[2]) + '\tkm/s\n')
            direction_file.write(' Secondary 1:\t' + str(velocity[1]) + '\tkm/s\n')
            direction_file.write(' Secondary 2:\t' + str(velocity[0]) + '\tkm/s\n')
            direction_file.write(' Secondary avg:\t ' + str(0.5*(velocity[0]+velocity[1])) + '\tkm/s\n\n')
            count = count + 1
            
        direction_plt.write(str(C11)+'\t'+ str(C44)+ '\t'+ str(average_val) +'\n')
        if compare_val > average_val:
            compare_val = average_val 
            min_point = [C11,C44]

print('minimum value for fit is ' + str(compare_val) + 'for ' + 'C11 ' + str(min_point[0]) +'and C44 ' + str(min_point[1]))        

direction_file.close()
direction_curtailed.close()
direction_plt.close()        
 
      







print 'The directions.dat file has been successfully written.'




























