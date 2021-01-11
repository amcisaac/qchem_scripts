import sys
import numpy as np

def get_geom_e_opt_cts(lines):
    '''
    Function to extract lowest E geometry from qchem geom opt

    Inputs:  lines  -- readlines(opt file)
    Outputs: lowest_e -- energy of lowest E structure
             lowest_g -- np array with the geom (str with atom name and coords)
             low_i    -- index of lowest energy cycle
    '''
    flag = 0      # will indicate whether we're in the geometry block or not
    lowest_e = 0  # will keep track of the lowest E 
    lowest_g = [] # will keep track of geom with the lowest E 
    energies=[]   # list of all energies
    geoms=[]      # list of all geometries
    for i,line in enumerate(lines):
        # get the energy of each structure from the line that says "Energy is XXXX"
        if line.find("Energy is") != -1:   # True when the line contains "Energy is" 
            e = float(line.split()[-1])    # the energy is the last "word" on the line

            if e < lowest_e:               # if the energy is the lowest so far, update the geometry
                lowest_e = e
                lowest_g = geom

            energies.append(e)

        # finds where the geometry ends. 'Point group' is the first thing printed once the geometry ends
        if line.find('Point Group') != -1: # True when line contains "Point Group" 
            flag=0                         # reset the flag
            geoms.append(geom)             # save the geometry

        # flag > 0 means we're in the geometry block
        if flag > 0:
            geom.append(line.strip().split()[1:])  # save each line in this block to the 'geom' list

        # finds where the geometry starts. 'ATOM' is the last line before the geometry starts
        if line.find('ATOM') != -1:        # True if the line contains "ATOM" 
            geom = []                      # reset the geometry to prepare to save the new one
            flag = 1                       # flag indicates that we're in the geometry block, and so save the next lines

    return lowest_e, np.array(lowest_g), np.argmin(energies)


def write_xyz(out_file, atom_names, atom_xyz, comment=''):
    '''
    Function that writes xyz coordinate arrays to .xyz file

    Inputs: out_file   -- name of the file to write coordinates to
            atom_names -- np array or list of atom names (str)
            atom_xyz   -- np array or list of atom xyz coordinates (float)
            comment    -- comment line to write in the xyz file

    Outputs: Writes to xyz_file
    '''
    with open(out_file,'w') as xyz_file:
        xyz_file.write(str(len(atom_names))+'\n') # first line-- # atoms
        xyz_file.write(comment+'\n')              # second line-- comment
        # loops through and writes the coordinates of each atom
        for i, atom in enumerate(atom_names):     
            xyz_file.write('{:2}     {:15.10f}     {:15.10f}    {:15.10f}\n'.format(atom, atom_xyz[i][0], atom_xyz[i][1], atom_xyz[i][2]))

    return

inputfile = sys.argv[1] # this is the first command line argument--here, qchem opt file

# read the file
with open(inputfile,'r') as inpfile:
    lines = inpfile.readlines()


low_e1, low_g1,low_i = get_geom_e_opt_cts(lines) # gets the lowest E geometry (low_g1)
atom_names = low_g1[:,0]  # atom names
atom_xyz = low_g1[:,1:].astype(float)  # atom coordinates

new_xyz_name = '.'.join(inputfile.split('.')[0:-1]) + '_cycle' + str(low_i+1) + '.xyz'  # name of the file to save the geometry to
comment = 'XYZ file from {} cycle {}'.format(inputfile,low_i+1)  # comment for the xyz file
write_xyz(new_xyz_name,atom_names,atom_xyz,comment=comment)      # save the geometry as an xyz file
