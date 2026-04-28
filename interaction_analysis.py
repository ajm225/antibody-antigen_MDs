import MDAnalysis as mda
from MDAnalysis.lib.distances import capped_distance
import numpy as np

# ---------- USER SETTINGS ----------
TPR = "md_rep1.tpr"
XTC = "rep1_noPBC.xtc"   # use your trajectory file here
INDEX_IN = "index.ndx"
INDEX_OUT = "interacting_residues_cogs.ndx"

GROUP1_NAME = "Antibody"
GROUP2_NAME = "Antigen"

CUTOFF_A = 5.0   # 5 Angstrom = 0.5 nm
STRIDE = 10      # analyze every 10th frame; use 1 for every frame
# -----------------------------------


def read_ndx_group(filename, group_name):
    atoms = []
    in_group = False

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("[") and line.endswith("]"):
                current = line.strip("[]").strip()
                in_group = current == group_name
                continue

            if in_group and line:
                atoms.extend([int(x) for x in line.split()])

    if not atoms:
        raise ValueError(f"Group '{group_name}' not found or empty in {filename}")

    # GROMACS atom numbers are 1-based; MDAnalysis uses 0-based
    return np.array(atoms) - 1


def write_ndx_group(f, name, atom_numbers):
    f.write(f"[ {name} ]\n")
    atom_numbers = sorted(atom_numbers)

    for i in range(0, len(atom_numbers), 15):
        line = atom_numbers[i:i+15]
        f.write(" ".join(str(x) for x in line) + "\n")
    f.write("\n")


print("Loading universe...")
u = mda.Universe(TPR, XTC)

print(f"Reading groups from {INDEX_IN}...")
group1_atoms_idx = read_ndx_group(INDEX_IN, GROUP1_NAME)
group2_atoms_idx = read_ndx_group(INDEX_IN, GROUP2_NAME)

group1 = u.atoms[group1_atoms_idx]
group2 = u.atoms[group2_atoms_idx]

print(f"{GROUP1_NAME}: {len(group1)} atoms")
print(f"{GROUP2_NAME}: {len(group2)} atoms")

interacting_residues_1 = set()
interacting_residues_2 = set()

print("Scanning trajectory for interacting residues...")

for ts in u.trajectory[::STRIDE]:
    pairs, distances = capped_distance(
        group1.positions,
        group2.positions,
        max_cutoff=CUTOFF_A,
        box=u.dimensions,
        return_distances=True
    )

    for i, j in pairs:
        interacting_residues_1.add(group1[i].residue)
        interacting_residues_2.add(group2[j].residue)

    print(f"Frame {ts.frame}, time {ts.time:.1f} ps: total residues found so far = "
          f"{len(interacting_residues_1)} + {len(interacting_residues_2)}")

# Convert interacting residues back to GROMACS atom numbers
atoms1 = []
for res in interacting_residues_1:
    atoms1.extend((res.atoms.indices + 1).tolist())

atoms2 = []
for res in interacting_residues_2:
    atoms2.extend((res.atoms.indices + 1).tolist())

print(f"Writing {INDEX_OUT}...")

with open(INDEX_OUT, "w") as f:
    write_ndx_group(f, "Interacting_Protein1", atoms1)
    write_ndx_group(f, "Interacting_Protein2", atoms2)

print("Done.")
print(f"Interacting {GROUP1_NAME} residues: {len(interacting_residues_1)}")
print(f"Interacting {GROUP2_NAME} residues: {len(interacting_residues_2)}")
print(f"Output written to: {INDEX_OUT}")
