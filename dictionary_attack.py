import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r"C:\Users\tazee\Downloads\password_dataset.csv")

# Show first 5 rows
print(df.head())

# Show summary
print("\nDataset Info:")
print(df["Category"].value_counts())

#  Dictionary Attack

# Common passwords (dictionary)
# Improved dictionary
dictionary = []

# Add common weak patterns
for i in range(100000):   # numbers like 12345, 67890
    dictionary.append(str(i))

# Add simple words
dictionary += [
    "password", "qwerty", "abc", "admin",
    "login", "user", "test"
]

# Counters
cracked = {"Weak": 0, "Medium": 0, "Strong": 0}
total = {"Weak": 0, "Medium": 0, "Strong": 0}

# Attack simulation
for _, row in df.iterrows():
    pwd = str(row["Password"])
    cat = row["Category"]

    total[cat] += 1

    if pwd in dictionary:
        cracked[cat] += 1

# Results
print("\nCracked Counts:")
print(cracked)

print("\nTotal Counts:")
print(total)

Percentage

percent_cracked = {}

for cat in cracked:
    percent_cracked[cat] = (cracked[cat] / total[cat]) * 100

print("\nPercentage Cracked:")
print(percent_cracked)



categories = list(percent_cracked.keys())
values = list(percent_cracked.values())

plt.figure(figsize=(8, 5))
plt.bar(categories, values)

plt.title("Dictionary Attack Success Rate")
plt.xlabel("Password Category")
plt.ylabel("Percentage Cracked (%)")

# Show values on top
for i, v in enumerate(values):
    plt.text(i, v + 1, f"{v:.1f}%", ha='center')

plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.show()
