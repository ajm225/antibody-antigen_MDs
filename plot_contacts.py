import matplotlib.pyplot as plt

filename = "num_contact.xvg"

time = []
contacts = []

with open(filename, "r") as file:
    for line in file:
        if line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        if len(parts) >= 2:
            time.append(float(parts[0]))
            contacts.append(float(parts[1]))

plt.figure(figsize=(8, 5))
plt.plot(time, contacts, linewidth=1.5)

plt.xlabel("Time (ps)")
plt.ylabel("Number of Contacts <0.5nm")
plt.title("Number of Contacts Over Time")

plt.tight_layout()
plt.savefig("contacts_plot.png", dpi=300)
plt.show()