import pandas as pd
from src.ga_selector import run_genetic_algorithm
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler

# 1. Data Loading
print(" Data Loading")
df = pd.read_csv("data/sample_data.csv")
X = df.drop(columns=["target"]).values  # All columns except 'target'
y = df["target"].values                 # Target column

print(f" Data Shape: {X.shape[0]} Sample {X.shape[1]} Feature")

#Chi-Square befor run algorithm
print("\Chi-Square befor run algorithm :")
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

chi_scores, p_values = chi2(X_scaled, y)
chi_results_all = sorted(
    [(i, chi_scores[i], p_values[i]) for i in range(len(chi_scores))],
    key=lambda x: x[1],
    reverse=True
)
print("\n Top ten features according to choice Chi-Square :")
print("pointer| Chi2 | p-value")
for i, chi, p in chi_results_all[:10]:
    print(f"{i:7d} | {chi:.4f} | {p:.4e}")
    
# 2. Genetic Algorithm
print("\n Run the genetic algorithm")
best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=True)

# 3. Display the results
selected_features = [i for i, bit in enumerate(best_chromosome) if bit == 1]
num_selected = len(selected_features)
total_features = X.shape[1]

print("\n" + "="*50)
print("Best solution :")
print(f"- Number of selected features: {num_selected} / {total_features}")
print(f"- Fitness score: {best_fitness:.4f}")
print(f"- Indices of selected features (first 10): {selected_features[:10]}")
if num_selected > 10:
    print(f"  ... (and{num_selected - 10} Other features)")
print("="*50)

#Chi-Square after run algorithm
print("\Chi-Square after run algorithm:")
X_selected_scaled = scaler.fit_transform(X[:, selected_features])
chi_selected, p_selected = chi2(X_selected_scaled, y)

print("\n  Top ten features according to choice Chi-Square :")
print("pointer| Chi2 | p-value")
for idx, chi, p in zip(selected_features, chi_selected, p_selected):
    print(f"{idx:14d} | {chi:.4f} | {p:.4e}")