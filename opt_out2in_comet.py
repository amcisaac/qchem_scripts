import sys
import numpy as np
from qchem_helper import *

output = sys.argv[1]

with open(output,'r',errors='replace') as outfile:
    lines = outfile.readlines()

last_geom = get_geom_e_opt_last(lines)
print(last_geom)
atom_names = last_geom[:,0]
atom_xyz = last_geom[:,1:].astype(float)
rem,spcharge=get_rem_sp(lines)
#print(rem)
input_prefix='.'.join(output.split('.')[0:-1])
n_opt = int(input_prefix.split('_')[-1])
new_input_name = '_'.join(input_prefix.split('_')[0:-1]) +'_'+ str(n_opt+1) + '.in'
comment = 'Continuing geom opt {}'.format(output)
write_input(new_input_name,atom_names,atom_xyz,rem,spcharge,comment=comment)
