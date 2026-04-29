import numpy as np
import matplotlib.pyplot as plt

print("RMSF script is running")

def load_xvg(filename):
    x = []
    y = []

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#") or line.startswith("@"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    x.append(float(parts[0]))
                    y.append(float(parts[1]))
                except ValueError:
                    continue

    return np.array(x), np.array(y)

rmsf_ab_file = "rmsf_ab.xvg"
rmsf_antigen_file = "rmsf_antigen.xvg"

rmsf_ab_x, rmsf_ab_y = load_xvg(rmsf_ab_file)
rmsf_antigen_x, rmsf_antigen_y = load_xvg(rmsf_antigen_file)

plt.figure(figsize=(8, 5))
plt.plot(rmsf_ab_x, rmsf_ab_y)
plt.xlabel("Residue Number")
plt.ylabel("RMSF (nm)")
plt.title("Antibody RMSF")
plt.tight_layout()
plt.savefig("RMSF_antibody.png", dpi=300)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(rmsf_antigen_x, rmsf_antigen_y)
plt.xlabel("Residue Number")
plt.ylabel("RMSF (nm)")
plt.title("Antigen RMSF")
plt.tight_layout()
plt.savefig("RMSF_antigen.png", dpi=300)
plt.close()