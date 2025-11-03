import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def run_ga_pca(X, y, feature_names, target_column, unique_classes):
    """Clean GA + PCA algorithm"""
    from ga_selector import run_genetic_algorithm
    best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=False)
    selected_indices = [i for i, bit in enumerate(best_chromosome) if bit == 1]
    selected_features = [feature_names[i] for i in selected_indices]
    
    if len(selected_indices) > 0:
        X_ga = X[:, selected_indices]
        
        scaler = StandardScaler()
        X_ga_scaled = scaler.fit_transform(X_ga)
        pca = PCA(n_components=0.95)
        X_pca = pca.fit_transform(X_ga_scaled)
        
        X_train_ga, X_test_ga, y_train, y_test = train_test_split(X_ga, y, test_size=0.2, random_state=42, stratify=y)
        X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(X_pca, y, test_size=0.2, random_state=42, stratify=y)
        
        model_ga = RandomForestClassifier(random_state=42)
        model_ga.fit(X_train_ga, y_train)
        y_pred_ga = model_ga.predict(X_test_ga)
        accuracy_ga = accuracy_score(y_test, y_pred_ga)
        
        model_pca = RandomForestClassifier(random_state=42)
        model_pca.fit(X_train_pca, y_train_pca)
        y_pred_pca = model_pca.predict(X_test_pca)
        accuracy_pca = accuracy_score(y_test_pca, y_pred_pca)
    else:
        accuracy_ga = 0.0
        accuracy_pca = 0.0
        pca = PCA(n_components=0.95)
        pca.fit(StandardScaler().fit_transform(X))
    
    return {
        "best_fitness": float(best_fitness),
        "selected_features_count": int(len(selected_features)),
        "selected_features": selected_features,
        "selected_feature_indices": [int(idx) for idx in selected_indices],
        "accuracy_ga": float(accuracy_ga),
        "accuracy_pca": float(accuracy_pca),
        "pca_components": int(pca.n_components_) if 'pca' in locals() else 0,
        "variance_ratio": [float(x) for x in pca.explained_variance_ratio_.tolist()] if 'pca' in locals() else [],
        "total_variance_explained": float(np.sum(pca.explained_variance_ratio_)) if 'pca' in locals() else 0.0,
        "fitness_history": [float(fitness) for fitness in history]
    }