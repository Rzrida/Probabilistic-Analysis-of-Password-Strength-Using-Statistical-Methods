import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#LOAD DATASET

df = pd.read_csv(r"C:\Users\mawac\Desktop\SEMESTER 6\Prob&Stats\password_dataset.csv")

print("Dataset Loaded!")
print(df["Category"].value_counts())
print()


# 2. BASIC SETTINGS
charset = {
    "Weak": 18,
    "Medium": 66,
    "Strong": 95
}

# Get average password lengths from dataset
avg_len = df.groupby("Category")["Password"].apply(lambda x: x.str.len().mean())

# Compute password space: N = charset^length
password_space = {}
for cat in ["Weak", "Medium", "Strong"]:
    N = charset[cat] ** avg_len[cat]
    password_space[cat] = N
    print(f"{cat}: N = {N:.2e}")

print()

# 3. PROBABILITY FUNCTION


def probability(k, N):
    return 1 - (1 - 1/N) ** k

# 4. GRAPH

plt.figure(figsize=(10, 6))

for cat in ["Weak", "Medium", "Strong"]:
    N = password_space[cat]

    #  Use fraction of N instead of raw huge values
    fraction = np.logspace(-6, 0.75, 500)   # from 0.000001*N to 100*N
    attempts = fraction * N

    probs = 1 - np.exp(-fraction)   # approximation of geometric

    plt.semilogx(attempts, probs, label=cat, linewidth=2)

plt.title("Brute Force Attack Simulation")
plt.xlabel("Number of Attempts (log scale)")
plt.ylabel("Probability of Success")
plt.ylim(0, 1.05)

plt.legend()
plt.grid(True)
plt.show()
