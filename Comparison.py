import pandas as pd
import numpy as np
from src.ga_selector import run_genetic_algorithm
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from sklearn.model_selection import  StratifiedKFold
import numpy as np

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

# Traditional Algorithm Recursive Feature Elimination
print("\n Run the Traditional Algorithm (RFE)")

# LogisticRegression 
base_model = LogisticRegression(max_iter=50000, random_state=42)

Rfe_Model = RFECV(
    estimator=base_model,
    step=1,
    cv=StratifiedKFold(5),
    scoring='accuracy',
    min_features_to_select=1
)

Rfe_Model = Rfe_Model.fit(X, y)

selected_features_selector = Rfe_Model.support_
selected_features_indices = np.where(selected_features_selector)[0].tolist()
num_selected_features= len(selected_features_indices)

Rfe_best_fitness = Rfe_Model.cv_results_['mean_test_score'][Rfe_Model.n_features_]

print("\n" + "="*50)
print("Best solution :")
print(f"- Number of selected features: {num_selected_features} / {total_features}")
print(f"- Fitness score: {Rfe_best_fitness:.4f}")
print(f"- Indices of selected features (first 10): {selected_features_indices[:10]}")
if num_selected_features > 10:
    print(f"  ... (and {num_selected_features - 10} Other features")
print("="*50)

print("Comparison between the Genetic Algorithm and the Recursive Feature Elimination : ")
print(f" Number of selected features of GA : {num_selected}/{total_features} ,  Fitness score  = {best_fitness:.4f}")
print(f" Number of selected features of RFE  : {num_selected_features}/{total_features} , Fitness score = {Rfe_best_fitness:.4f}")
print("\n" + "=" * 50)