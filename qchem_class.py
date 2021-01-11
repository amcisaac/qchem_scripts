import numpy as np
import sys

'''
Helper functions for qchem file analysis

python3 compatible

TO DO: combine all into some kind of class or function so that it doesn't have to loop multiple times for each function
'''

class qchem_file:
    def __init__(self,inputfile,geom_opt=False):
        with open(inputfile,'r') as inpfile:
            self.lines = inpfile.readlines()
        self.typ = inputfile.split('.')[-1]
        self.filename = inputfile
        self.get_opt_geom=geom_opt


    def get_input_info(self):  # self.molecule, self.rem, self.comment (?)
        flag_comment=False
        flag_mol = False
        flag_rem = False
        flag_plots = False
        self.comment=[]
        self.mol=[]
        self.rem=[]
        self.plots=[]
        for i,line in enumerate(self.lines):

            if line.find('$comment') != -1:
                flag_comment = True
            if line.find('$molecule') != -1:
                flag_mol = True
            if line.find('$rem') != -1:
                flag_rem = True
            if line.find('$plots') != -1:
                flag_plots = True
            if flag_comment:
                self.comment.append(line)
            if flag_mol:
                self.mol.append(line)
            if flag_rem:
                self.rem.append(line)
            if flag_plots:
                self.plots.append(line)
            if line.find('$end') != -1: # last so that $end will get appended to the blocks
                flag_comment=False
                flag_mol = False
                flag_rem = False
                flag_plots = False

   # def get_geom_xyz(self):
   #
   #     return
   # def get_geom_opt(self):
   #     return

inputfile=sys.argv[1]
test=qchem_file(inputfile)
test.get_input_info()
 




def read_xyz(input_xyz):
    '''
    Function that reads xyz file into arrays

    Inputs: input_xyz -- .xyz file with the QD coordinates
    Outputs: xyz_coords -- np array with the coordinates of all the atoms (float)
             atom_names -- np array with the atom names (str)
    '''
    xyz_coords = np.loadtxt(input_xyz,skiprows=2,usecols=(1,2,3))
    atom_names = np.loadtxt(input_xyz,skiprows=2,usecols=(0,),dtype=str)
    return xyz_coords, atom_names

def write_geom(xyz_file,atom_names,atom_xyz):
    '''
    Function to write the geometry part of an xyz/input file

    Inputs: xyz_file   -- file object, open for writing, to write xyz to
            atom_names -- np array or list of atom names (str)
            atom_xyz   -- np array or list of atom xyz coordinates (float)

    Outputs: Writes to out_file
    '''

    for i, atom in enumerate(atom_names):
        xyz_file.write('{:2}     {:15.10f}     {:15.10f}    {:15.10f}\n'.format(atom, atom_xyz[i][0], atom_xyz[i][1], atom_xyz[i][2]))
    return

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
        xyz_file.write(str(len(atom_names))+'\n')
        xyz_file.write(comment+'\n')
        write_geom(xyz_file,atom_names,atom_xyz)
    return

def write_input(inpfile,atom_names,atom_xyz,rem,spcharge,comment=''):
    '''
    Function that writes qchem input file given geom and $rem

    Inputs: inpfile   -- name of the file to write info to
            atom_names -- np array or list of atom names (str)
            atom_xyz   -- np array or list of atom xyz coordinates (float)
            comment    -- comment line to write in the input file
            rem        -- string with the $rem section (one string with \n for line breaks)
            spcharge   -- string with the spin and charge

    Outputs: Writes to inpfile
    '''

    with open(inpfile,'w') as inputfile:
        inputfile.write('$comment\n')
        inputfile.write(comment+'\n')
        inputfile.write('$end\n')
        inputfile.write('\n')
        inputfile.write('$molecule\n')
        inputfile.write(spcharge)
        write_geom(inputfile,atom_names,atom_xyz)
        inputfile.write('$end\n')
        inputfile.write('\n')
        inputfile.write(rem)
    return

def get_geom_io(inputfile):
    '''
    Function to extract geometry from qchem input/output

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: atom_names -- np array with the atom names (str)
             coords     -- np array with the xyz coords (float)
    '''
    with open(inputfile,'r') as inp:
        flag = 0
        geom = []
        for i,line in enumerate(inp):
            if line.find('$end') != -1:
                break
            if flag > 1:
                geom.append(line.strip().split())
            if flag > 0:
                flag += 1
            if line.find('$molecule') != -1:
                flag = 1

    geom = np.array(geom)
    atom_names = geom[:,0]
    coords = geom[:,1:].astype(float)
    return atom_names, coords

def get_geom_e_opt_cts(lines):
    '''
    Function to extract lowest E geometry from qchem geom opt

    Inputs:  lines  -- readlines(opt file)
    Outputs: lowest_e -- energy of lowest E structure
             lowest_g -- np array with the geom (str with atom name and coords)
             low_i    -- index of lowest energy cycle
    '''
    flag = 0
    lowest_e = 0
    low_i = 0
    lowest_g = []
    energies=[]
    geoms=[]
    for i,line in enumerate(lines):
        if line.find("Energy is") != -1:
            e = float(line.split()[-1])
            if e < lowest_e:
                lowest_e = e
                lowest_g = geom

            energies.append(e)
        if line.find('Point Group') != -1:
            flag=0
            geoms.append(geom)
        if flag > 0:
            geom.append(line.strip().split()[1:])
        if line.find('ATOM') != -1:
            geom = []
            flag = 1

    return lowest_e, np.array(lowest_g), np.argmin(energies)

def get_rem_sp(lines):
    '''
    Function to extract $rem section and spin/charge from qchem input/output

    Inputs:  lines  -- readlines(qchem input/output file)
    Outputs: rem -- string with the rem section separated by \n
             spcharge     -- string with charge and spin
    '''
    flag = 0
    rem = []
    for i,line in enumerate(lines):
        if line.find('$molecule') != -1:
            spcharge = lines[i+1]
        if line.find('$rem') != -1:
            flag += 1
        if flag > 1:
            rem.append(line)
        if flag>1 and line.find('$end') != -1:
            break

    return ''.join(rem), spcharge

# def get_geom_e_opt_argmin(lines):
#     flag = 0
#     lowest_e = 0
#     lowest_g = []
#     energies=[]
#     geoms=[]
#     for i,line in enumerate(lines):
#         if line.find("Energy is") != -1:
#             e = float(line.split()[-1])
#             energies.append(e)
#         if line.find('Point Group') != -1:
#             flag=0
#             geoms.append(geom)
#         if flag > 0:
#             geom.append(line.strip().split()[1:])
#         if line.find('ATOM') != -1:
#             geom = []
#             flag = 1
#
#     low_i = np.argmin(energies)
#     lowest_e = energies[low_i]
#     lowest_g = np.array(geoms[low_i])
#     return lowest_e, lowest_g
