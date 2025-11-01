import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from src.ga_selector import run_genetic_algorithm  

# 1. Data Loading
print(" Data Loading")
df = pd.read_csv("data/sample_data.csv")
X = df.drop(columns=["target"]).values  # All columns except 'target'
y = df["target"].values                 # Target column

print(f" Data Shape: {X.shape[0]} Sample {X.shape[1]} Feature")

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

# ========================================
# 4. Apply PCA
print("\nApplying PCA...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Let PCA choose number of components to retain 95% of variance
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

# Train model using PCA
X_train_pca, X_test_pca, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)
model_pca = RandomForestClassifier(random_state=42)
model_pca.fit(X_train_pca, y_train)
y_pred_pca = model_pca.predict(X_test_pca)
accuracy_pca = accuracy_score(y_test, y_pred_pca)

# Display PCA results
print("\n" + "="*50)
print("Model results after PCA:")
print(f"- Number of components selected: {pca.n_components_}")
print(f"- Model accuracy: {accuracy_pca:.4f}")
print("="*50)