from qchem_helper import get_geom_cycle,write_input
import sys

'''
USAGE: python3 qchem_optcyc2tddft.py [geom opt output] [cycle to get geom from] [number of excitations] [tda or tddft or both]

builds a TDDFT/TDA input from a geometry in a geometry Optimization
note: assumes 128 GB of RAM on 16 coress--adjust mem_total if this isn't true
'''

outputfile = sys.argv[1] #geometry opt output
Nopt = sys.argv[2] # opt cycle to get geometry from
Nex = sys.argv[3] # number of excitations
rpa = sys.argv[4] #rpa keyword--either tda, or tddft, or both

if rpa == 'tda' or rpa == 'TDA':
    rpa = 'false'
elif rpa == 'both':
    rpa = 'true'
elif rpa == 'tddft' or 'TDDFT':
    rpa = '2\ncis_guess_disk true'

atoms,xyz=get_geom_cycle(outputfile,Nopt)


new_input_name = '.'.join(outputfile.split('.')[0:-1]) + '_cycle' + str(Nopt) + '.in'
comment = 'TDDFT input from {} cycle {}'.format(outputfile,Nopt)

spcharge='0 1\n'
rem ='$rem\nmethod pbe0\nbasis lanl2dz\necp fit-lanl2dz\nmem_total 8000\nmem_static 1000\nithrsh_dft 15\nCIS_N_ROOTS {}\nRPA {}\n$end'.format(Nex,rpa)
write_input(new_input_name,atoms,xyz,rem,spcharge,comment=comment)
