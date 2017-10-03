import copy
import numpy as np
from  numpy import pi as pi

class SymmetricMol(object):
    """Build symmetric molecules"""
    def __init__(self):
        self.atoms = []
        self.names = {}

    @property
    def size(self):
        return len(self.atoms)

    def add(self, atom):
        """Add an atom without guarantee of order"""
        self.atoms.append(atom)

    def addTo(self, atom, new_atom, z_radiant_angle=0, label=None):
        new_atom.z_rotate(z_radiant_angle)
        new_pos = new_atom.pos +  atom.pos
        new_atom.pos = new_pos
        self.atoms.append(new_atom)
        if label:
            if label not in self.names.keys():
                self.names[label] = len(self.atoms)-1 # since I always append in the last
                # position, the position is the length - 1
            else:
                raise Exception("Atom with label {} already exists, I'm not adding it".format(label))

    def addToAtomNumber(self, integer, new_atom, z_radiant_angle=0, label=None):
        """integer starts counting from 1"""
        atom = self.atoms[integer-1]
        self.addTo(atom, new_atom, z_radiant_angle, label=label)

    def addToLast(self, new_atom, z_radiant_angle=0, label=None):
        self.addTo(self.atoms[-1], new_atom, z_radiant_angle, label=label)

    def addToLabeledAtom(self, name, new_atom, z_radiant_angle=0, label=None):
        atom_index = self.names[name]
        atom = self.atoms[atom_index]
        self.addTo(atom, new_atom, z_radiant_angle, label=label)

    def xz_mirror_duplicate(self, atom_label):
        """Create a copy of atom mirrored w.r.t the xz plane (invert y)"""
        atom_index = self.names[atom_label]
        atom = self.atoms[atom_index]
        x, y, z = atom.pos[:,0]
        new_atom = Atom(atom.elem, x, -y, z)
        self.atoms.append(new_atom)

    def z_rotate_duplicate(self, atom, radiant_angle):
        """Duplicate atom and rotate it around the z axis with a radiant angle"""
        new = copy.deepcopy(atom)
        new.z_rotate(radiant_angle)
        self.atoms.append(new)

    def z_rotate_duplicate_last_N_atoms(self, N, *radiant_angles):
        """Take the last N atoms and duplicate them with a rotation around the z axis
        for every radiant angle in *radiant_angles"""
        if N>len(self.atoms):
            raise Exception('N is bigger than the number of atoms available')
        last_index = len(self.atoms)
        first_index = last_index-N
        for angle in radiant_angles:
            for i in range(first_index, last_index):
                self.z_rotate_duplicate(self.atoms[i], angle)

    def save_xyz(self, filename):
        with open(filename, 'wt') as f:
            f.write(str(len(self.atoms)))
            f.write('\n\n')
            for atom in self.atoms:
                x, y, z = atom.pos[:,0]
                f.write('{}\t{:10.6f}\t{:10.6f}\t{:10.6f}\n'.format(atom.elem, x, y, z))

class Atom(object):
    def __init__(self, elem, x, y=0, z=0):
        self.elem = elem
        self.pos = np.ndarray(shape=(3,1), dtype=float)
        self.pos[0] = x
        self.pos[1] = y
        self.pos[2] = z

    def z_rotate(self, theta):
        """Rotate the atom position around the z axis, for a radiant angle theta"""
        old_pos = self.pos
        rotation_matrix = np.array(
            [[np.cos(theta), -np.sin(theta), 0],
             [np.sin(theta), np.cos(theta), 0],
             [0, 0, 1]])
        self.pos = np.dot(rotation_matrix, old_pos)
