import matplotlib.pyplot as plt

filename = "numstruc.xvg"

time = []
structure_count = []

with open(filename, "r") as file:
    for line in file:
        if line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        if len(parts) >= 2:
            time.append(float(parts[0]))
            structure_count.append(float(parts[1]))

plt.figure(figsize=(8, 5))
plt.plot(time, structure_count, linewidth=1.5)

plt.xlabel("Time (ps)")
plt.ylabel("Secondary Structures")
plt.title("Number of Secondary Structures")

plt.tight_layout()
plt.savefig("secondary_structure_plot.png", dpi=300)
plt.show()