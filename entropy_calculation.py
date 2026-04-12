
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

"""**SECTION 1: Character set definitions**"""

CHARSET_SIZES = {
    "lowercase only (a–z)":           26,
    "lowercase + digits":              36,
    "lower + upper + digits":          62,
    "lower + upper + digits + symbols":94,
}

"""**SECTION 2: Shannon Entropy helper functions**"""

def shannon_entropy_password(password: str) -> float:
    """
    Compute the empirical Shannon entropy of a password string.

    Formula:  H = -Σ p(x) * log₂(p(x))
    where p(x) = frequency of character x / total length

    Returns entropy in bits.
    """
    if not password:
        return 0.0

    freq = {}
    for ch in password:
        freq[ch] = freq.get(ch, 0) + 1

    n = len(password)
    entropy = 0.0
    for count in freq.values():
        p_x = count / n                          # probability of symbol x
        entropy -= p_x * math.log2(p_x)         # –p(x) log₂ p(x)

    return round(entropy, 4)

def theoretical_entropy(password_length: int, charset_size: int) -> float:
    """
    Compute theoretical maximum entropy assuming uniform distribution.

    Formula:  H_max = L × log₂(N)
    where L = password length, N = charset size.

    This is the upper bound — a truly random password of length L
    drawn uniformly from N characters achieves this entropy.
    """
    return round(password_length * math.log2(charset_size), 4)

"""**SECTION 3: Sample password sets (weak / medium / strong)**"""

weak_passwords = [
    "password",   # dictionary word
    "123456",     # numeric sequence
    "qwerty",     # keyboard pattern
    "abc123",     # trivial mix
    "iloveyou",   # common phrase
    "111111",     # repeated digit
    "letmein",    # dictionary word
    "admin",      # default credential
    "welcome",    # common word
    "monkey",     # top-10 common password
]

medium_passwords = [
    "Pass@123",       # word + symbol + digits
    "Hello#2024",     # proper + symbol + year
    "Blue$Sky7",      # mixed word + symbol
    "Tiger!99",       # animal + symbol + number
    "sun&Moon5",      # nature word + symbol
    "Cube_2025",      # noun + year
    "Jazz#Beats3",    # two words + symbol
    "River@Wave4",    # two words + symbol
    "Fox!Run88",      # word + symbol + double digit
    "Storm#Night6",   # two words + symbol
]

strong_passwords = [
    "Xk9#mP2@qR!vL5z",     # 16-char fully random
    "3Bw!Yq@8zL$rN6p",     # 16-char fully random
    "G7&mVx!2Kp@Rn9eQ",    # 17-char
    "jT!4Lr@Pz#8nWs2Y",    # 17-char
    "Kp8#Tz@Vn!5mRqLb",    # 16-char
    "9Xr!Lq#Bm@Tz5Yp2",    # 17-char
    "W3@kVn!8Rp#Lz7Tq",    # 17-char
    "Mj4!Yz@Xp#8nRvL3",    # 17-char
    "Qr7#Tn!Lm@5Yz8Vp",    # 17-char
    "Bp!9Zx#Lv@3nTrQm",    # 16-char
]

"""**SECTION 4: Compute & display entropy for each category**"""

categories = {
    "Weak":   weak_passwords,
    "Medium": medium_passwords,
    "Strong": strong_passwords,
}

print("=" * 65)
print("  PASSWORD ENTROPY ANALYSIS — RIDA ZAHRA (DE-45-CE-A)")
print("  Formula: H = −Σ p(x) log₂(p(x))")
print("=" * 65)

category_avg_entropy = {}

for cat_name, pwd_list in categories.items():
    print(f"\n{'─'*65}")
    print(f"  Category: {cat_name.upper()} PASSWORDS")
    print(f"{'─'*65}")
    print(f"  {'Password':<22}  {'Length':>6}  {'Empirical H (bits)':>20}")
    print(f"  {'─'*22}  {'─'*6}  {'─'*20}")

    entropies = []
    for pwd in pwd_list:
        h = shannon_entropy_password(pwd)
        entropies.append(h)
        print(f"  {pwd:<22}  {len(pwd):>6}  {h:>20.4f}")

    avg_h = round(sum(entropies) / len(entropies), 4)
    category_avg_entropy[cat_name] = avg_h
    print(f"\n  ► Average Empirical Entropy  : {avg_h} bits")
    print(f"  ► Min Entropy                : {min(entropies)} bits")
    print(f"  ► Max Entropy                : {max(entropies)} bits")

"""**SECTION 5: Theoretical entropy table**"""

print(f"\n\n{'=' * 65}")
print("  THEORETICAL MAX ENTROPY  H_max = L × log₂(N)")
print(f"{'=' * 65}")
print(f"  {'Category':<10} {'Avg Len':>8} {'Charset Size':>13} {'H_max (bits)':>14}")
print(f"  {'─'*10} {'─'*8} {'─'*13} {'─'*14}")

category_params = {
    "Weak":   (avg_len := round(sum(len(p) for p in weak_passwords)   / 10, 1), 26),
    "Medium": (avg_len := round(sum(len(p) for p in medium_passwords) / 10, 1), 62),
    "Strong": (avg_len := round(sum(len(p) for p in strong_passwords) / 10, 1), 94),
}

# Recalculate properly
theo_rows = {
    "Weak":   (round(sum(len(p) for p in weak_passwords)   / 10, 1), 26),
    "Medium": (round(sum(len(p) for p in medium_passwords) / 10, 1), 62),
    "Strong": (round(sum(len(p) for p in strong_passwords) / 10, 1), 94),
}

for cat, (avg_l, N) in theo_rows.items():
    h_max = theoretical_entropy(int(avg_l), N)
    print(f"  {cat:<10} {avg_l:>8.1f} {N:>13} {h_max:>14.4f}")

print(f"\n{'=' * 65}\n")

"""**SECTION 6: Bar chart — Average Empirical Entropy per Category**

**Plot 2: Per-password entropy scatter**
"""

colors = ["#E74C3C", "#F39C12", "#27AE60"]   # red/orange/green
labels = list(category_avg_entropy.keys())
values = list(category_avg_entropy.values())

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle(
    "Password Entropy Analysis\n"
    r"$H = -\sum p(x)\,\log_2 p(x)$",
    fontsize=14, fontweight="bold", y=1.01
)

#  Plot 1: Average Empirical Entropy 
ax1 = axes[0]
bars = ax1.bar(labels, values, color=colors, edgecolor="white",
               linewidth=1.5, width=0.5)

for bar, val in zip(bars, values):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.03,
        f"{val:.4f} bits",
        ha="center", va="bottom", fontsize=11, fontweight="bold"
    )

ax1.set_title("Avg Empirical Entropy per Category", fontsize=12, pad=10)
ax1.set_xlabel("Password Category", fontsize=11)
ax1.set_ylabel("Shannon Entropy H (bits)", fontsize=11)
ax1.set_ylim(0, max(values) * 1.25)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.tick_params(labelsize=11)

ax2 = axes[1]

all_x, all_y, all_c = [], [], []
offset = {"Weak": 0, "Medium": 1, "Strong": 2}

for cat, pwd_list in categories.items():
    for pwd in pwd_list:
        h = shannon_entropy_password(pwd)
        jitter = np.random.uniform(-0.15, 0.15)
        all_x.append(offset[cat] + jitter)
        all_y.append(h)
        all_c.append(colors[offset[cat]])

ax2.scatter(all_x, all_y, c=all_c, s=70, alpha=0.75, edgecolors="white", linewidths=0.5)

# Add mean lines
for cat, avg in category_avg_entropy.items():
    xi = offset[cat]
    ax2.hlines(avg, xi - 0.3, xi + 0.3,
               colors=colors[xi], linewidths=2.5, linestyles="--")
    ax2.text(xi + 0.32, avg, f"μ={avg:.2f}", va="center", fontsize=9,
             color=colors[xi], fontweight="bold")

ax2.set_xticks([0, 1, 2])
ax2.set_xticklabels(["Weak", "Medium", "Strong"], fontsize=11)
ax2.set_title("Entropy Distribution (all passwords)", fontsize=12, pad=10)
ax2.set_xlabel("Password Category", fontsize=11)
ax2.set_ylabel("Shannon Entropy H (bits)", fontsize=11)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.tick_params(labelsize=11)

patch_w = mpatches.Patch(color=colors[0], label="Weak")
patch_m = mpatches.Patch(color=colors[1], label="Medium")
patch_s = mpatches.Patch(color=colors[2], label="Strong")
ax2.legend(handles=[patch_w, patch_m, patch_s], fontsize=10, framealpha=0.4)

plt.tight_layout()
plt.savefig("entropy_chart.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: entropy_chart.png")
