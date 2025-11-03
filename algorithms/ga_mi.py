import numpy as np
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def run_ga_mi(X, y, feature_names, target_column, unique_classes):
    """Clean GA + Mutual Information algorithm"""
    from ga_selector import run_genetic_algorithm
    best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=False)
    selected_indices_ga = [i for i, bit in enumerate(best_chromosome) if bit == 1]
    selected_features_ga = [feature_names[i] for i in selected_indices_ga]
    
    mi_scores = mutual_info_classif(X, y, random_state=42)
    mi_results_all = sorted([(i, mi_scores[i]) for i in range(len(mi_scores))], key=lambda x: x[1], reverse=True)
    
    k_selected = min(len(selected_indices_ga), X.shape[1])
    if k_selected == 0:
        k_selected = min(10, X.shape[1])
    
    feature_selector = SelectKBest(mutual_info_classif, k=k_selected)
    selected_indices_mi = feature_selector.get_support(indices=True).tolist()
    selected_features_mi = [feature_names[i] for i in selected_indices_mi]
    
    # Calculate accuracies
    if len(selected_indices_ga) > 0:
        X_ga = X[:, selected_indices_ga]
        X_train_ga, X_test_ga, y_train, y_test = train_test_split(X_ga, y, test_size=0.2, random_state=42, stratify=y)
        model_ga = RandomForestClassifier(random_state=42)
        model_ga.fit(X_train_ga, y_train)
        y_pred_ga = model_ga.predict(X_test_ga)
        accuracy_ga = accuracy_score(y_test, y_pred_ga)
    else:
        accuracy_ga = 0.0
    
    X_mi = X[:, selected_indices_mi]
    X_train_mi, X_test_mi, y_train_mi, y_test_mi = train_test_split(X_mi, y, test_size=0.2, random_state=42, stratify=y)
    model_mi = RandomForestClassifier(random_state=42)
    model_mi.fit(X_train_mi, y_train_mi)
    y_pred_mi = model_mi.predict(X_test_mi)
    accuracy_mi = accuracy_score(y_test_mi, y_pred_mi)
    
    overlap_indices = list(set(selected_indices_ga) & set(selected_indices_mi))
    overlap_features = [feature_names[i] for i in overlap_indices]
    overlap_count = len(overlap_indices)
    overlap_percentage_ga = (overlap_count / len(selected_indices_ga)) * 100 if len(selected_indices_ga) > 0 else 0
    overlap_percentage_mi = (overlap_count / len(selected_indices_mi)) * 100 if len(selected_indices_mi) > 0 else 0
    
    return {
        "best_fitness": float(best_fitness),
        "selected_features_count_ga": int(len(selected_features_ga)),
        "selected_features_ga": selected_features_ga,
        "selected_indices_ga": [int(idx) for idx in selected_indices_ga],
        "accuracy_ga": float(accuracy_ga),
        "selected_features_count_mi": int(len(selected_features_mi)),
        "selected_features_mi": selected_features_mi,
        "selected_indices_mi": [int(idx) for idx in selected_indices_mi],
        "accuracy_mi": float(accuracy_mi),
        "mi_scores_selected": [{"index": int(idx), "mi_score": float(mi_scores[idx]), "feature_name": feature_names[idx]} for idx in selected_indices_mi],
        "top_10_mi": [{"index": int(i), "mi_score": float(score), "feature_name": feature_names[i]} for i, score in mi_results_all[:10]],
        "overlap_count": int(overlap_count),
        "overlap_features": overlap_features,
        "overlap_percentage_ga": f"{overlap_percentage_ga:.1f}%",
        "overlap_percentage_mi": f"{overlap_percentage_mi:.1f}%",
        "fitness_history": [float(fitness) for fitness in history],
        "selected_features_count": int(len(selected_features_mi)),
        "accuracy": float(accuracy_mi),
    }