import numpy as np
import sys
import re
import os

# Script to extract timing info from all geometry optimization
# output files in the current directory.
# Designed for opts that are restarted frequently, with 
# files that have a common prefix and a number at the end, 
# such as geom_opt_1.out, geom_opt_2.out, geom_opt_3.out ...

# USAGE:
# python3 extract_timing_optrs.py > [timing file].csv

# Assuming output files follow naming convention above, the
# script will automatically get all of the file names, and 
# operate in numerical order (e.g. not in the order of `ls`) 

inputs = []
ns = []
for f in os.listdir('.'):
    if f.endswith('.out'):
        try: 
            ns.append(int(f.split('_')[-1].split('.')[0]))

            inputs.append(f)
        except ValueError:
            pass
ns.sort()
inpfile = '_'.join(inputs[0].split('_')[0:-1])


grad_cpu = []
grad_wall = []
scf_cpu = []
scf_wall = []
inps=[]
for n in ns:
    inp = inpfile+'_'+str(n)+'.out'
    with open(inp,'r') as inputfile:
        for line in inputfile.readlines():
            if re.search('Gradient time',line):
                inps.append(inp)
                scf_cpu.append(scf_cpu_x)
                scf_wall.append(scf_wall_x)
                try:
                    grad_cpu.append(float(line.split()[3]))
                    grad_wall.append(float(line.split()[6]))
                except ValueError:
                    grad_cpu.append(float(line.split()[3][:-1]))
                    grad_wall.append(float(line.split()[5][:-1]))
            elif re.search('SCF time',line):
                try:
                    scf_cpu_x = (float(line.split()[3]))
                    scf_wall_x =(float(line.split()[6]))
                except ValueError:
                    scf_cpu_x=(float(line.split()[3][:-1]))
                    scf_wall_x=(float(line.split()[5][:-1]))

grad_cpu = np.array(grad_cpu)
grad_wall = np.array(grad_wall)
scf_cpu = np.array(scf_cpu)
scf_wall = np.array(scf_wall)

grad_cpu_hr = grad_cpu/60.0/60.0
grad_wall_hr = grad_wall/60.0/60.0
scf_cpu_hr = scf_cpu / 60.0 / 60.0
scf_wall_hr = scf_wall/60.0/60.0

grad_rat = grad_cpu/grad_wall
scf_rat = scf_cpu/scf_wall

print(len(inps),grad_rat.shape,scf_rat.shape)

print( 'opt cycle,filename, scf cpu time (s),scf cpu time (hr),scf wall time (s),scf wall time (hr),scf cpu:wall ratio,grad cpu time (s),grad cpu time (hr),grad wall time (s),grad wall time (hr),grad cpu:wall ratio')

l = len(grad_rat)
for i in range(0,l):
    print(i,',',inps[i],',', scf_cpu[i], ',', scf_cpu_hr[i],',',scf_wall[i],',',scf_wall_hr[i],',',scf_rat[i],',',grad_cpu[i],',',grad_cpu_hr[i],',',grad_wall[i],',',grad_wall_hr[i],',',grad_rat[i])
