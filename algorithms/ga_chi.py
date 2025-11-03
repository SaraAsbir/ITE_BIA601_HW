import numpy as np
import pandas as pd
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def run_ga_chi(X, y, feature_names, target_column, unique_classes):
    from ga_selector import run_genetic_algorithm
    best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=False)
    selected_indices = [i for i, bit in enumerate(best_chromosome) if bit == 1]
    selected_features = [feature_names[i] for i in selected_indices]
    
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    chi_scores, p_values = chi2(X_scaled, y)
    
    chi_results_all = sorted(
        [(i, chi_scores[i], p_values[i]) for i in range(len(chi_scores))],
        key=lambda x: x[1],
        reverse=True
    )
    
    if len(selected_indices) > 0:
        X_selected_scaled = scaler.fit_transform(X[:, selected_indices])
        chi_selected, p_selected = chi2(X_selected_scaled, y)
        
        X_selected = X[:, selected_indices]
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=0.2, random_state=42, stratify=y
        )
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
    else:
        accuracy = 0.0
        chi_selected = []
        p_selected = []
    
    return {
        "best_fitness": float(best_fitness),
        "selected_features_count": int(len(selected_features)),
        "selected_features": selected_features,
        "selected_feature_indices": [int(idx) for idx in selected_indices],
        "accuracy": float(accuracy),
        "top_10_chi": [{"index": int(i), "chi_score": float(chi), "p_value": float(p)} 
                      for i, chi, p in chi_results_all[:10]],
        "selected_chi_scores": [{"index": int(idx), "chi_score": float(chi), "p_value": float(p)} 
                               for idx, chi, p in zip(selected_indices, chi_selected, p_selected)],
        "fitness_history": [float(fitness) for fitness in history]
    }