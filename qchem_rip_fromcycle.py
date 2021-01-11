from qchem_helper import get_geom_cycle,write_xyz
import sys

outputfile = sys.argv[1]
Nopt = sys.argv[2]

atoms,xyz=get_geom_cycle(outputfile,Nopt)


new_xyz_name = '.'.join(outputfile.split('.')[0:-1]) + '_cycle' + str(Nopt) + '.xyz'
comment = 'XYZ file from {} cycle {}'.format(outputfile,Nopt)
write_xyz(new_xyz_name,atoms,xyz,comment=comment)
