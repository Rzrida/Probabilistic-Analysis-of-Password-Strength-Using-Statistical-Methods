import random
import string
import csv
import matplotlib.pyplot as plt
import numpy as np

"""
SECTION 1: Character Set Definitions
Mirroring the theoretical framework: |P| = N^L
"""
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()"
ALL_CHARS = string.ascii_letters + string.digits + string.punctuation

"""
SECTION 2: Generation Logic
Defining Weak, Medium, and Strong generation rules.
"""

def generate_weak():
    # Rule: Only lowercase or only digits, short length (5-8)
    use_chars = random.choice([LOWERCASE, DIGITS])
    length = random.randint(5, 8)
    return "".join(random.choice(use_chars) for _ in range(length))

def generate_medium():
    # Rule: Mix of cases and digits, moderate length (9-12)
    use_chars = string.ascii_letters + string.digits + "@#$%"
    length = random.randint(9, 12)
    # Ensuring at least one uppercase and one digit for "medium" policy
    pwd = [random.choice(string.ascii_uppercase), random.choice(string.digits)]
    pwd += [random.choice(use_chars) for _ in range(length - 2)]
    random.shuffle(pwd)
    return "".join(pwd)

def generate_strong():
    # Rule: Full printable ASCII, long length (14-16), truly random
    length = random.randint(14, 16)
    return "".join(random.choice(ALL_CHARS) for _ in range(length))

"""
SECTION 3: Dataset Creation and CSV Export
Generating 100 passwords per category (Total: 300)
"""

dataset = []

# Generate 100 of each
for _ in range(100):
    dataset.append({"Password": generate_weak(), "Category": "Weak"})
for _ in range(100):
    dataset.append({"Password": generate_medium(), "Category": "Medium"})
for _ in range(100):
    dataset.append({"Password": generate_strong(), "Category": "Strong"})

# Save to CSV 
with open('password_dataset.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Password", "Category"])
    writer.writeheader()
    writer.writerows(dataset)

print("Dataset generated: password_dataset.csv (300 entries)")

"""
SECTION 4: Statistical Visualization
Creating the Bar Chart for Password Length Distribution
"""

# Group lengths by category
lengths = {"Weak": [], "Medium": [], "Strong": []}
for entry in dataset:
    lengths[entry["Category"]].append(len(entry["Password"]))

# Calculate averages for the plot
categories = list(lengths.keys())
avg_lengths = [np.mean(lengths[cat]) for cat in categories]
colors = ["#E74C3C", "#F39C12", "#27AE60"] # Red, Orange, Green

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, avg_lengths, color=colors, edgecolor="black", alpha=0.8)

# Add labels on top of bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{yval:.1f} chars', ha='center', fontweight='bold')

ax.set_title("Average Password Length Distribution per Category", fontsize=14, fontweight='bold')
ax.set_ylabel("Average Length (Number of Characters)", fontsize=12)
ax.set_xlabel("Password Category", fontsize=12)
ax.set_ylim(0, 20)

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("length_distribution.png", dpi=150)
plt.show()

print("Chart saved: length_distribution.png")
