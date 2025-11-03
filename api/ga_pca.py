from flask import Blueprint, request, jsonify
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.data_loader import process_csv_data, load_sample_data
from algorithms.ga_pca import run_ga_pca

ga_pca_bp = Blueprint('ga_pca', __name__)

@ga_pca_bp.route('/ga_pca', methods=['POST'])
def genetic_algorithm_pca():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        X, y, df, feature_names, target_column, unique_classes = process_csv_data(file.stream)
        result = run_ga_pca(X, y, feature_names, target_column, unique_classes)
        
        return jsonify({
            "status": "success",
            "algorithm": "genetic_algorithm_pca_comparison",
            "data_info": {
                "rows": int(len(df)),
                "total_features": int(len(feature_names)),
                "target_column": str(target_column),
                "target_classes": [str(cls) for cls in unique_classes]
            },
            **result
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

@ga_pca_bp.route('/ga_pca/test', methods=['GET'])
def test_genetic_algorithm_pca():
    try:
        X, y, df, feature_names, target_column, unique_classes = load_sample_data()
        result = run_ga_pca(X, y, feature_names, target_column, unique_classes)
        
        return jsonify({
            "status": "success",
            "algorithm": "genetic_algorithm_pca_comparison",
            "sample_data_used": "sample_data.csv",
            "data_info": {
                "rows": int(len(df)),
                "total_features": int(len(feature_names)),
                "target_column": str(target_column),
                "target_classes": [str(cls) for cls in unique_classes]
            },
            **result
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500