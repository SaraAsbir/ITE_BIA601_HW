import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def run_ga_only(X, y, feature_names, target_column, unique_classes):
    """Clean GA-only algorithm"""
    from ga_selector import run_genetic_algorithm
    best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=False)
    selected_indices = [i for i, bit in enumerate(best_chromosome) if bit == 1]
    selected_features = [feature_names[i] for i in selected_indices]
    
    if len(selected_indices) > 0:
        X_selected = X[:, selected_indices]
        X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42, stratify=y)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
    else:
        accuracy = 0.0
    
    total_features = X.shape[1]
    selected_count = len(selected_indices)
    reduction_percentage = ((total_features - selected_count) / total_features) * 100
    
    return {
        "best_fitness": float(best_fitness),
        "selected_features_count": int(selected_count),
        "selected_features": selected_features,
        "selected_feature_indices": [int(idx) for idx in selected_indices],
        "accuracy": float(accuracy),
        "total_features": int(total_features),
        "reduction_percentage": f"{reduction_percentage:.1f}%",
        "fitness_history": [float(fitness) for fitness in history],
        "chromosome": [int(bit) for bit in best_chromosome]
    }