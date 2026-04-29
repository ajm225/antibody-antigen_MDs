import matplotlib.pyplot as plt
import numpy as np
import re

input_file = "contact_map.xpm"

matrix_lines = []
inside_matrix = False

with open(input_file, "r") as f:
    for line in f:
        line = line.strip()

        # Start reading actual XPM matrix after the header line
        if line.startswith('"') and re.match(r'^"\d+\s+\d+\s+\d+\s+\d+', line):
            inside_matrix = True
            continue

        if inside_matrix and line.startswith('"'):
            row = line.strip('",')
            
            # Keep only rows that look like matrix data
            if row and not (" c " in row) and not row.startswith("/*"):
                matrix_lines.append(row)

# Remove any rows that are different lengths
lengths = [len(row) for row in matrix_lines]
common_length = max(set(lengths), key=lengths.count)
matrix_lines = [row for row in matrix_lines if len(row) == common_length]

symbols = sorted(set("".join(matrix_lines)))
symbol_to_value = {symbol: i for i, symbol in enumerate(symbols)}

matrix = np.array([
    [symbol_to_value[char] for char in row]
    for row in matrix_lines
])

plt.figure(figsize=(8, 7))
plt.imshow(matrix, origin="lower", aspect="auto", interpolation="nearest")
plt.xlabel("Residue Index")
plt.ylabel("Residue Index")
plt.title("Contact Map")

cbar = plt.colorbar()
cbar.set_label("Contact intensity / frequency")

plt.tight_layout()
plt.savefig("contact_map_heatmap.png", dpi=300)
plt.show()