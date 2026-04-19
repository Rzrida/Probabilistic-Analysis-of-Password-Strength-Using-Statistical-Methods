import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# ==============================
# 1. STATISTICAL FUNCTIONS
# ==============================
def compute_statistics(data):
    mean = np.mean(data)
    variance = np.var(data)
    std_dev = np.std(data)
    return mean, variance, std_dev

# ==============================
# 2. HYPOTHESIS TEST FUNCTION
# ==============================
def perform_ttest(data1, data2, label1="Group1", label2="Group2"):
    """
    Performs independent t-test.
    Automatically applies log transform if numbers are very large to avoid precision loss.
    """
    # Check if values are extremely large
    if np.max(data1) > 1e10 or np.max(data2) > 1e10:
        print("\nNote: Large values detected, using log10 for t-test to avoid numerical errors.")
        data1 = np.log10(np.array(data1) + 1)
        data2 = np.log10(np.array(data2) + 1)

    t_stat, p_value = ttest_ind(data1, data2)
    print(f"\nT-Test between {label1} and {label2}")
    print(f"T-Statistic: {t_stat:.4f}")
    print(f"P-Value: {p_value:.6f}")
    if p_value < 0.05:
        print("Result: Significant difference (Reject H0)")
    else:
        print("Result: No significant difference (Fail to reject H0)")
    return t_stat, p_value

# ==============================
# 3. TABLE GENERATION
# ==============================
def generate_summary_table(data_dict):
    summary = []
    for category, data in data_dict.items():
        mean, var, std = compute_statistics(data)
        summary.append([category, mean, var, std])
    df = pd.DataFrame(summary, columns=["Category", "Mean Attempts", "Variance", "Std Dev"])
    print("\n=== Statistical Summary Table ===")
    print(df)
    return df

# ==============================
# 4. VISUALIZATION FUNCTION (UPDATED)
# ==============================
def plot_statistics(df, dict_percent=None, title="Password Category Analysis"):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    import numpy as np

    plt.figure(figsize=(10, 6))
    categories = df["Category"]
    mean_attempts = df["Mean Attempts"].values

    # Log scale for mean attempts if values are huge
    if np.max(mean_attempts) > 1e6:
        heights = np.log10(mean_attempts + 1)
        ylabel = "Log10(Mean Attempts)"
    else:
        heights = mean_attempts
        ylabel = "Mean Attempts"

    # Bar positions and width
    x = np.arange(len(categories))
    width = 0.35

    # Colors for Weak/Medium/Strong
    colors = ['red', 'orange', 'green']

    # Plot mean bars
    bars = plt.bar(x, heights, width=width, color=colors[:len(categories)], alpha=0.7)

    # Overlay dictionary % cracked (offset slightly to the right)
    legend_elements = []
    if dict_percent:
        dict_heights = []
        for i, cat in enumerate(categories):
            dict_val = dict_percent.get(cat, 0)
            dict_heights.append(dict_val)
        dict_scaled = np.array(dict_heights) * np.max(heights)
        plt.bar(x + width/2, dict_scaled, width=width*0.6, color='blue', alpha=0.6)
        for i, dh in enumerate(dict_scaled):
            plt.text(x[i] + width/2, dh + 0.03*np.max(heights),
                     f"{dict_heights[i]*100:.1f}%", ha='center', color='blue', fontsize=10)
        legend_elements.append(Patch(facecolor='blue', alpha=0.6, label='Dictionary % Cracked'))

    # Add mean bars to legend dynamically
    for i, cat in enumerate(categories):
        legend_elements.append(Patch(facecolor=colors[i], label=f"{cat} Mean"))

    plt.xticks(x, categories)
    plt.xlabel("Password Category")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.legend(handles=legend_elements)
    plt.show()


# ==============================
# 5. ANALYSIS FUNCTION (UPDATED TO REMOVE DICTIONARY FROM BRUTE-FORCE PLOT)
# ==============================
def analyze_attempts(name, weak, medium, strong, dict_percent=None, show_dict=True):
    print(f"\n==============================")
    print(f"Analysis for {name}")
    print(f"==============================")
    data = {"Weak": weak, "Medium": medium, "Strong": strong}
    df = generate_summary_table(data)

    # Only show dictionary % if explicitly asked
    plot_statistics(df, dict_percent=dict_percent if show_dict else None,
                    title=f"{name}: Password Category Analysis")

    # T-Test only between Weak and Strong
    perform_ttest(weak, strong, "Weak", "Strong")
    return df


# ==============================
# 6. MAIN FUNCTION
# ==============================
def main():
    # Load dataset
    df = pd.read_csv(r"password_dataset.csv")

    # ======== Tazeen's Dictionary Attack ========
    dictionary = [str(i) for i in range(100000)] + ["password", "qwerty", "abc", "admin", "login", "user", "test"]
    dict_attempts = {"Weak": [], "Medium": [], "Strong": []}
    for _, row in df.iterrows():
        pwd = str(row["Password"])
        cat = row["Category"]
        dict_attempts[cat].append(1 if pwd in dictionary else 0)

    dictionary_weak = dict_attempts["Weak"]
    dictionary_medium = dict_attempts["Medium"]
    dictionary_strong = dict_attempts["Strong"]

    # Calculate dictionary % cracked for plotting
    dict_percent = {
        "Weak": np.mean(dictionary_weak),
        "Medium": np.mean(dictionary_medium),
        "Strong": np.mean(dictionary_strong)
    }

    # Dictionary Attack plot (show dictionary %)
    analyze_attempts("Dictionary Attack",
                     dictionary_weak, dictionary_medium, dictionary_strong,
                     dict_percent=dict_percent, show_dict=True)

    # ======== Mawa's Brute-Force Attack ========
    charset = {"Weak": 18, "Medium": 66, "Strong": 95}
    avg_len = df.groupby("Category")["Password"].apply(lambda x: x.str.len().mean())

    # Generate brute-force attempts
    brute_force_weak = [charset["Weak"] ** avg_len["Weak"] for _ in df[df["Category"] == "Weak"]["Password"]]
    brute_force_medium = [charset["Medium"] ** avg_len["Medium"] for _ in df[df["Category"] == "Medium"]["Password"]]
    brute_force_strong = [charset["Strong"] ** avg_len["Strong"] for _ in df[df["Category"] == "Strong"]["Password"]]

    # Brute-Force Attack plot (do NOT show dictionary %)
    analyze_attempts("Brute-Force Attack",
                     brute_force_weak, brute_force_medium, brute_force_strong,
                     dict_percent=None, show_dict=False)

    # ======== Key Space Analysis (Brute-Force) ========
    print("\n=== Key Space Analysis (Linked to Brute-Force) ===")
    keyspace = {}
    keyspace_log = {}
    for cat in ["Weak", "Medium", "Strong"]:
        length = avg_len[cat]
        size = charset[cat]
        keyspace[cat] = size ** length
        keyspace_log[cat] = length * np.log10(size)
        print(f"{cat}: Key Space = {keyspace[cat]:.2e}, log10(Key Space) ≈ {keyspace_log[cat]:.2f}")

    # Key Space Table
    keyspace_table = pd.DataFrame({
        "Category": ["Weak", "Medium", "Strong"],
        "Charset Size": [charset["Weak"], charset["Medium"], charset["Strong"]],
        "Avg Length": [avg_len["Weak"], avg_len["Medium"], avg_len["Strong"]],
        "Key Space": [keyspace["Weak"], keyspace["Medium"], keyspace["Strong"]],
        "log10(Key Space)": [keyspace_log["Weak"], keyspace_log["Medium"], keyspace_log["Strong"]]
    })
    print("\n=== Key Space Table ===")
    print(keyspace_table)

    # ======== Combined Attack ========
    combined_weak = brute_force_weak + dictionary_weak
    combined_medium = brute_force_medium + dictionary_medium
    combined_strong = brute_force_strong + dictionary_strong

    # Combined Attack plot (optional dictionary % overlay)
    analyze_attempts("Combined Attack",
                     combined_weak, combined_medium, combined_strong,
                     dict_percent=dict_percent, show_dict=True)


if __name__ == "__main__":
    main()