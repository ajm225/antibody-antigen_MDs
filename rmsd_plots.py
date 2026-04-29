import numpy as np
import matplotlib.pyplot as plt

print("RMSD script is running")

def load_xvg(filename):
    x = []
    y = []

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#") or line.startswith("@"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                x.append(float(parts[0]))
                y.append(float(parts[1]))

    return np.array(x), np.array(y)

# FILES
rmsd_protein_file = "rmsd_antigen_rel_to_ab_protein.xvg"
rmsd_backbone_file = "rmsd_antigen_rel_to_ab_backbone.xvg"

print("Loading files...")

rmsd_protein_x, rmsd_protein_y = load_xvg(rmsd_protein_file)
rmsd_backbone_x, rmsd_backbone_y = load_xvg(rmsd_backbone_file)

print("Data loaded:", len(rmsd_protein_x), len(rmsd_backbone_x))

plt.figure()
plt.plot(rmsd_protein_x, rmsd_protein_y)
plt.plot(rmsd_backbone_x, rmsd_backbone_y)

plt.savefig("test_rmsd.png")

print("Saved test_rmsd.png")