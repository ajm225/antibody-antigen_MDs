import matplotlib.pyplot as plt

filename = "mindist.xvg"

time = []
mindist = []

with open(filename, "r") as file:
    for line in file:
        if line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        if len(parts) >= 2:
            time.append(float(parts[0]))
            mindist.append(float(parts[1]))

plt.figure(figsize=(8, 5))
plt.plot(time, mindist, linewidth=1.5)

plt.xlabel("Time (ps)")
plt.ylabel("Minimum Distance (nm)")
plt.title("Minimum Distance Over Time")

plt.tight_layout()
plt.savefig("mindist_plot.png", dpi=300)
plt.show()