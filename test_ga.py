import pandas as pd
from src.ga_selector import run_genetic_algorithm

# 1. Data Loading
print("Loading data...")
df = pd.read_csv("data/sample_data.csv")
X = df.drop(columns=["target"]).values  # All columns except 'target'
y = df["target"].values                 # Target column

print(f"Data shape: {X.shape[0]} samples, {X.shape[1]} features")

# 2. Run Genetic Algorithm
print("\nRunning Genetic Algorithm...")
best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=True)

# 3. Display results
selected_features = [i for i, bit in enumerate(best_chromosome) if bit == 1]
num_selected = len(selected_features)
total_features = X.shape[1]

print("\n" + "="*50)
print("Best solution:")
print(f"- Number of selected features: {num_selected} / {total_features}")
print(f"- Fitness score: {best_fitness:.4f}")
print(f"- Indices of selected features (first 10): {selected_features[:10]}")
if num_selected > 10:
    print(f"  ... (and{num_selected - 10} other features)")
print("="*50)
