import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def run_ga_rfe(X, y, feature_names, target_column, unique_classes):
    """Clean GA + RFE algorithm - just processes data"""
    from ga_selector import run_genetic_algorithm
    best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=False)
    selected_indices_ga = [i for i, bit in enumerate(best_chromosome) if bit == 1]
    selected_features_ga = [feature_names[i] for i in selected_indices_ga]
    
    base_model = LogisticRegression(max_iter=50000, random_state=42)
    rfe_model = RFECV(
        estimator=base_model,
        step=1,
        cv=StratifiedKFold(5),
        scoring='accuracy',
        min_features_to_select=1
    )
    rfe_model.fit(X, y)
    
    selected_indices_rfe = np.where(rfe_model.support_)[0].tolist()
    selected_features_rfe = [feature_names[i] for i in selected_indices_rfe]
    rfe_best_score = rfe_model.cv_results_['mean_test_score'][rfe_model.n_features_ - 1]
    
    if len(selected_indices_ga) > 0:
        X_ga = X[:, selected_indices_ga]
        X_train_ga, X_test_ga, y_train, y_test = train_test_split(
            X_ga, y, test_size=0.2, random_state=42, stratify=y
        )
        model_ga = RandomForestClassifier(random_state=42)
        model_ga.fit(X_train_ga, y_train)
        y_pred_ga = model_ga.predict(X_test_ga)
        accuracy_ga = accuracy_score(y_test, y_pred_ga)
    else:
        accuracy_ga = 0.0
    
    X_rfe = X[:, selected_indices_rfe]
    X_train_rfe, X_test_rfe, y_train_rfe, y_test_rfe = train_test_split(
        X_rfe, y, test_size=0.2, random_state=42, stratify=y
    )
    model_rfe = RandomForestClassifier(random_state=42)
    model_rfe.fit(X_train_rfe, y_train_rfe)
    y_pred_rfe = model_rfe.predict(X_test_rfe)
    accuracy_rfe = accuracy_score(y_test_rfe, y_pred_rfe)
    
    overlap_indices = list(set(selected_indices_ga) & set(selected_indices_rfe))
    overlap_features = [feature_names[i] for i in overlap_indices]
    overlap_count = len(overlap_indices)
    
    return {
        "best_fitness": float(best_fitness),
        "selected_features_count": int(len(selected_features_rfe)),
        "selected_features": selected_features_rfe,
        "accuracy": float(accuracy_rfe),       
        "selected_features_count_ga": int(len(selected_features_ga)),
        "selected_features_ga": selected_features_ga,
        "selected_indices_ga": [int(idx) for idx in selected_indices_ga],
        "accuracy_ga": float(accuracy_ga),
        "rfe_best_score": float(rfe_best_score),
        "selected_features_count_rfe": int(len(selected_features_rfe)),
        "selected_features_rfe": selected_features_rfe,
        "selected_indices_rfe": [int(idx) for idx in selected_indices_rfe],
        "accuracy_rfe": float(accuracy_rfe),
        "optimal_features_rfe": int(rfe_model.n_features_),
        "overlap_count": int(overlap_count),
        "overlap_features": overlap_features,
        "fitness_history": [float(fitness) for fitness in history]
    }