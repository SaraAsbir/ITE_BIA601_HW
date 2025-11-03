import pandas as pd
from src.ga_selector import run_genetic_algorithm
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler

# 1. Data Loading
print("Data Loading")
df = pd.read_csv("data/sample_data.csv")
X = df.drop(columns=["target"]).values  # All columns except 'target'
y = df["target"].values                 # Target column

print(f"Data Shape: {X.shape[0]} Samples × {X.shape[1]} Features")

# Chi-Square before running algorithm
print("\nChi-Square before running algorithm:")
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

chi_scores, p_values = chi2(X_scaled, y)
chi_results_all = sorted(
    [(i, chi_scores[i], p_values[i]) for i in range(len(chi_scores))],
    key=lambda x: x[1],
    reverse=True
)

print("\nTop ten features according to Chi-Square:")
print("Index | Chi2 | p-value")
for i, chi, p in chi_results_all[:10]:
    print(f"{i:5d} | {chi:.4f} | {p:.4e}")

# 2. Genetic Algorithm
print("\n Running the genetic algorithm...")
best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=True)

# 3. Display the results
selected_features = [i for i, bit in enumerate(best_chromosome) if bit == 1]
num_selected = len(selected_features)
total_features = X.shape[1]

print("\n" + "=" * 50)
print("Best Solution:")
print(f"- Number of selected features: {num_selected} / {total_features}")
print(f"- Fitness score: {best_fitness:.4f}")
print(f"- Indices of selected features (first 10): {selected_features[:10]}")
if num_selected > 10:
    print(f"  ... (and {num_selected - 10} other features)")
print("=" * 50)

# Chi-Square after running algorithm
print("\nChi-Square after running algorithm:")
X_selected_scaled = scaler.fit_transform(X[:, selected_features])
chi_selected, p_selected = chi2(X_selected_scaled, y)

print("\nTop features according to Chi-Square after selection:")
print("Index | Chi2 | p-value")
for idx, chi, p in zip(selected_features, chi_selected, p_selected):
    print(f"{idx:5d} | {chi:.4f} | {p:.4e}")
