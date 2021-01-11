import sys

# script to manage job resubmission on Comet
# DOES NOT READ IN SCRATCH

# USAGE:
# python3 make_submit_script.py [sample submit script] [first job number] [last job number]

# takes a sample submit script, and makes submit scripts for several jobs, where each is dependent
# on the previous job and will only start once it finishes.

# designed to be used for restarting geometry optimizations
# e.g. if you have a starting geometry in geom_1.in and a submit script job1.sh
# you would do python3 make_submit_script.py job1.sh 1 10
# that would replicate job1.sh to make 10 successive submit scripts with equivalent parameters
# but different input/output files (and in each script, it makes a new geometry from the last 
# geometry of the previous output file)

sample_script=sys.argv[1]
start_n = int(sys.argv[2])
end_n = int(sys.argv[3])

with open(sample_script,'r') as sample_file:
    sample_lines =sample_file.readlines()

sbatch_options = []

for i,line in enumerate(sample_lines):
    splitline=line.split()
    if line.find('-J') != -1: # extract base job name (without _1, _2, etc)
        keyword = splitline[-1]
        keyword_split = keyword.split('_') 
        job_prefix = '_'.join(keyword_split[:-1])
    elif line.find('SBATCH') != -1 and line.find('-J') == -1 and line.find('-o') == -1 and line.find('-e') == -1: # extract sbatch options besides jobname
        sbatch_options.append(' '.join(splitline[1:]))
    elif line.find('qchem -np') != -1: # get qchem commands (all lines after module load qchem) 
        run_qchem=' '.join(splitline[0:-2])  

sbatch = ' '.join(sbatch_options)

# write line in submit_dep.sh to submit first job
sub_dep_lines="#submit job {}\njid{}=$(sbatch job{}.sh | grep -Eo \'[0-9]{{1,}}\')\n\n".format(start_n,start_n,start_n)

# write submit scripts & dependencies into submit_dep
for n in range(start_n+1,end_n+1):
    print(n)
    jobname = job_prefix + '_{}'.format(n)
    prev_out = job_prefix + '_{}.out'.format(n-1)
    sbatch_n = ' -J {} -e {}.log -o {}.log '.format(jobname,jobname,jobname) + sbatch
    
    python_commands = '\n'.join(['module load python','python3 ~/code/opt_out2in_comet.py {}'.format(prev_out)])
    qchem_commands = '\n'.join(['module load qchem','export QCSCRATCH=/scratch/$USER/$SLURM_JOBID',run_qchem + ' {}.in {}.out'.format(jobname,jobname)])

    with open('job{}.sh'.format(n),'w') as subn:
        subn.write('#!/bin/bash\n')
        subn.write('\n')
        subn.write(python_commands)
        subn.write('\n\n')
        subn.write(qchem_commands)

    sub_dep_lines += "#submit job {}\njid{}=$(sbatch {} --dependency=afterany:$jid{} job{}.sh | grep -Eo \'[0-9]{{1,}}\')\n\n".format(n,n,sbatch_n,n-1,n)

with open('submit_dep_{}to{}.sh'.format(start_n,end_n),'w') as subdep:
    subdep.write('#!/bin/bash\n\n')
    subdep.write(sub_dep_lines)
