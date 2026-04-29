import matplotlib.pyplot as plt

x = []
y = []

filename = "hbondsnew.xvg"

with open(filename, "r") as file:
    for line in file:
        if line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        if len(parts) >= 2:
            x.append(float(parts[0]))
            y.append(float(parts[1]))

plt.figure(figsize=(8, 5))
plt.plot(x, y, linewidth=1.5)

plt.xlabel("Time (ps)")
plt.ylabel("Hbonds")
plt.title("Number of Hydrogen Bonds")

plt.tight_layout()
plt.savefig("hbonds_plot.png", dpi=300)
plt.show()