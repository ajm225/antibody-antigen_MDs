import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

input_file = "structure.dat"

# DSSP codes mapped to numbers
ss_map = {
    "~": 0,  # coil/none
    "C": 0,
    "H": 1,  # alpha helix
    "G": 2,  # 3-10 helix
    "I": 3,  # pi helix
    "E": 4,  # beta sheet
    "B": 5,  # beta bridge
    "T": 6,  # turn
    "S": 7   # bend
}

data = []

with open(input_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith(("#", "@")):
            continue

        # Each line is usually one time frame of DSSP assignments
        row = [ss_map.get(char, 0) for char in line if char.strip()]
        if row:
            data.append(row)

data = np.array(data)

plt.figure(figsize=(12, 6))
plt.imshow(data.T, aspect="auto", origin="lower", interpolation="nearest")

plt.xlabel("Frame")
plt.ylabel("Residue Index")
plt.title("Secondary Structure Over Time")

cbar = plt.colorbar()
cbar.set_ticks([0, 1, 2, 3, 4, 5, 6, 7])
cbar.set_ticklabels([
    "Coil",
    "α-helix",
    "3-10 helix",
    "π-helix",
    "β-sheet",
    "β-bridge",
    "Turn",
    "Bend"
])

plt.tight_layout()
plt.savefig("secondary_structure_heatmap.png", dpi=300)
plt.show()