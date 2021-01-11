import numpy as np
import sys
import re

#python2
# program to extract computational timing info from geometry optimization files
# works on one file or multiple files
# BUT file data will be printed in order that files are read into the script 
# (e.g. so if you have opt_1, opt_2...opt_10, and just input opt*
# they won't be in the right order since `ls` will order it opt_1, opt_10, opt_2...)

# usage: extract_timing.py [output file(s) from geom opt] > [timing file].csv 

inputs = sys.argv[1:]

grad_cpu = []
grad_wall = []
scf_cpu = []
scf_wall = []
inps=[]
for inp in inputs:
    with open(inp,'r') as inputfile:
        for line in inputfile.readlines():
            if re.search('Gradient time',line):
                inps.append(inp)
                try:
                    grad_cpu.append(float(line.split()[3]))
                    grad_wall.append(float(line.split()[6]))
                except ValueError:
                    grad_cpu.append(float(line.split()[3][:-1]))
                    grad_wall.append(float(line.split()[5][:-1]))
            elif re.search('SCF time',line):
                try:
                    scf_cpu.append(float(line.split()[3]))
                    scf_wall.append(float(line.split()[6]))
                except ValueError:
                    scf_cpu.append(float(line.split()[3][:-1]))
                    scf_wall.append(float(line.split()[5][:-1]))

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


print 'opt cycle,filename,scf cpu time (s),scf cpu time (hr),scf wall time (s),scf wall time (hr),scf cpu:wall ratio,grad cpu time (s),grad cpu time (hr),grad wall time (s),grad wall time (hr),grad cpu:wall ratio'

l = len(grad_rat)
for i in range(0,l):
    print i,',',inps[i],',',scf_cpu[i], ',', scf_cpu_hr[i],',',scf_wall[i],',',scf_wall_hr[i],',',scf_rat[i],',',grad_cpu[i],',',grad_cpu_hr[i],',',grad_wall[i],',',grad_wall_hr[i],',',grad_rat[i]
