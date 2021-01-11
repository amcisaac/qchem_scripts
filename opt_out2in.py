import sys
import numpy as np
from qchem_helper import *
import timeit


inputfile = sys.argv[1]

with open(inputfile,'r') as inpfile:
    lines = inpfile.readlines()


low_e1, low_g1,low_i = get_geom_e_opt_cts(lines)
atom_names = low_g1[:,0]
atom_xyz = low_g1[:,1:].astype(float)
rem,spcharge=get_rem_sp(lines)

new_input_name = '.'.join(inputfile.split('.')[0:-1]) + 'ctd_fromc_' + str(low_i+1) + '.in'
comment = 'Continuing geom opt {} from cycle {}'.format(inputfile,low_i+1)
write_input(new_input_name,atom_names,atom_xyz,rem,spcharge,comment=comment)
