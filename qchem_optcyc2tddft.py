from qchem_helper import get_geom_cycle,write_input
import sys

'''
USAGE: python3 qchem_optcyc2tddft.py [geom opt output] [cycle to get geom from] [number of excitations] [tda or tddft or both]

builds a TDDFT/TDA input from a geometry in a geometry Optimization
note: assumes 120 GB of RAM on 24 coress--adjust mem_total if this isn't true
'''

outputfile = sys.argv[1] #geometry opt output
Nopt = sys.argv[2] # opt cycle to get geometry from
Nex = sys.argv[3] # number of excitations
rpa = sys.argv[4] #rpa keyword--either tda, or tddft, or both
if len(sys.argv)>4:
    path = sys.argv[5]
    savename = sys.argv[6] +'_cycle'+ str(Nopt)
    new_input_name = path+savename 
    submit = True 
else: 
    new_input_name = '.'.join(outputfile.split('.')[0:-1]) + '_cycle' + str(Nopt) 

if rpa == 'tda' or rpa == 'TDA':
    rpa = 'false'
elif rpa == 'both':
    rpa = 'true'
elif rpa == 'tddft' or 'TDDFT':
    rpa = '2\ncis_guess_disk true'

atoms,xyz=get_geom_cycle(outputfile,Nopt)


comment = 'TDDFT input from {} cycle {}'.format(outputfile,Nopt)

spcharge='0 1\n'
rem ='$rem\nmethod pbe0\nbasis lanl2dz\necp fit-lanl2dz\nmem_total 5000\nmem_static 1000\nithrsh_dft 15\nCIS_N_ROOTS {}\nRPA {}\nxc_grid     000075000302\n$end'.format(Nex,rpa)
write_input(new_input_name+'.in',atoms,xyz,rem,spcharge,comment=comment)

if submit:
    with open(path+'submit.sh','w') as submitfile:
        submitfile.write('#!/bin/bash\n\n')
        submitfile.write('#SBATCH -J {}\n#SBATCH -o {}.log\n#SBATCH -e {}.log\n#SBATCH --partition=compute\n#SBATCH --nodes=1\n#SBATCH --ntasks-per-node=24\n#SBATCH --mem-per-cpu 5000\n#SBATCH -t 2-00:00:00\n\n'.format(savename,savename,savename))
        submitfile.write('module load qchem\nexport QCSCRATCH=/scratch/$USER/$SLURM_JOBID\n\n')
        submitfile.write('SCRATCH="scratch_cycle{}"\ncurr_d=$PWD\n\n'.format(Nopt))
        submitfile.write('rm -r $QCSCRATCH/$SCRATCH\ncp -r $SCRATCH $QCSCRATCH\n\n')
        submitfile.write('qchem -save -np 1 -nt 24 {}.in {}.out $SCRATCH\n\n'.format(savename,savename))
        submitfile.write('cp -r $QCSCRATCH/$SCRATCH $curr_d')
        
        
        
