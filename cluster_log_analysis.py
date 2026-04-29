import re
import matplotlib.pyplot as plt

clusters = []
counts = []

with open("cluster.log", "r") as f:
    for line in f:
        # match lines like: "  1 |  2330  0.199 |"
        match = re.match(r"\s*(\d+)\s+\|\s+(\d+)", line)
        if match:
            clusters.append(int(match.group(1)))
            counts.append(int(match.group(2)))

# Convert to percentages
total_frames = sum(counts)
percentages = [(c / total_frames) * 100 for c in counts]

# Plot
plt.figure()
plt.bar(clusters[:20], percentages[:20])  # top 20 clusters
plt.xlabel("Cluster Number (ranked)")
plt.ylabel("Population (%)")
plt.title("Cluster Population Distribution")
plt.savefig("cluster_population.png", dpi=300, bbox_inches='tight')
plt.show()