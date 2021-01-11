#!/bin/bash

# bash script to extract convergence information from geometry optimization
# designed for optimizations with many restarts, where files have a common
# prefix folowed by a number.
# e.g. geom_opt_1.out geom_opt_2.out 

#USAGE:
# ./grep_convergence.sh [number of opt file #1] [number of final opt file] [prefix that all files share]

for ((i=$1;i<=$2;i++)); do grep -H "Energy change" $3_$i.out >> $3_deltae.txt; done
for ((i=$1;i<=$2;i++)); do grep -H "Displacement  " $3_$i.out >> $3_disp.txt; done
for ((i=$1;i<=$2;i++)); do grep -H "Gradient  " $3_$i.out >> $3_grad.txt; done
for ((i=$1;i<=$2;i++)); do grep -H "Energy is" $3_$i.out >> $3_energyis.txt; done
for ((i=$1;i<=$2;i++)); do grep -H "Total energy in the final basis set" $3_$i.out >> $3_scfe.txt; done
