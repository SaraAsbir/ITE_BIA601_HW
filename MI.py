import pandas as pd
from src.ga_selector import run_genetic_algorithm
from sklearn.feature_selection import chi2, SelectKBest, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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
# Traditional Algorithm (Mutual Information)
print("\n Run the Traditional Algorithm (Mutual Information)")
feature_selector = SelectKBest(mutual_info_classif, k=min(20, X.shape[1]))
X_features_selected = feature_selector.fit_transform(X, y)
selected_feature_indices = feature_selector.get_support(indices=True)


X_train_set, X_test_set, y_train_labels, y_test_labels = train_test_split(X_features_selected, y, test_size=0.3, random_state=42)
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train_set, y_train_labels)
y_predictions = rf_classifier.predict(X_test_set)

model_accuracy = accuracy_score(y_test_labels, y_predictions)

print(f"\n =================================================")
print(f"\n Best solution :")
print(f"- Number of selected features of mutual information: {len(selected_feature_indices)}")
print(f"- Fitness score: {model_accuracy:.4f}")
print(f"- Indices of selected features: {selected_feature_indices[:10]}")
if len(selected_feature_indices) > 10:
    print(f"  ... (and {len(selected_feature_indices) - 10} more features)")    
print(f"\n =================================================") 

#Comparison between genetic algorithm and Mutual Information
print(f"\n comparison between the Genetic Algorithm and mutual information")
print(f"- Number of selected features of genetic algorithm: {num_selected} / {total_features} , Fitness score: {best_fitness:.4f}") 
print(f"- Number of selected features of mutual information: {len(selected_feature_indices)} , Fitness score: {model_accuracy:.4f}")
print(f"\n =================================================") 