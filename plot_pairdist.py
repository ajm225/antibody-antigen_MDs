import matplotlib.pyplot as plt

x = []
y = []

filename = "pairdist.xvg"

with open(filename, "r") as file:
    for line in file:
        # Skip metadata/header lines
        if line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        if len(parts) >= 2:
            x.append(float(parts[0]))
            y.append(float(parts[1]))

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, linewidth=1.5)

# Labels (adjust depending on what your file represents)
plt.xlabel("Time (ps)")
plt.ylabel("Distance (nm)")
plt.title("Minimum Pairwise Distance")

plt.tight_layout()
plt.savefig("pairdist_plot.png", dpi=300)
plt.show()