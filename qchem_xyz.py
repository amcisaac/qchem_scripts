import numpy as np
from qchem_helper import *
import sys

'''
Script that rips a molecular geometry from qchem input/output and writes to .xyz

Looks for geometry from $molecule block

Usage: python3 qchem_xyz.py [qchem input/output] [optional: name of file for xyz output]
'''

inputfile = sys.argv[1]
if len(sys.argv) > 2:
    xyz_name = sys.argv[2]
else:
    xyz_name = '.'.join(inputfile.split('.')[0:-1])+'_'+inputfile.split('.')[-1]+'.xyz'

atom_names, coords = get_geom_io(inputfile)
write_xyz(xyz_name,atom_names, coords, comment='generated from {} via {}'.format(inputfile, sys.argv[0]))
