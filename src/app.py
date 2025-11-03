from flask import Flask
from flask_cors import CORS
from api.ga_pca import ga_pca_bp
from api.ga_rfe import ga_rfe_bp
from api.ga_chi import ga_chi_bp
from api.ga_mi import ga_mi_bp
from api.ga_only import ga_only_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(ga_pca_bp, url_prefix='/api')
app.register_blueprint(ga_rfe_bp, url_prefix='/api')
app.register_blueprint(ga_chi_bp, url_prefix='/api')
app.register_blueprint(ga_mi_bp, url_prefix='/api')
app.register_blueprint(ga_only_bp, url_prefix='/api')

@app.route('/')
def home():
    return {
        "message": "Feature Selection Algorithms API",
        "available_endpoints": {
            "genetic_algorithm_only": "/api/ga",
            "genetic_algorithm_pca": "/api/ga_pca",
            "genetic_algorithm_rfe": "/api/ga_rfe",
            "genetic_algorithm_chi": "/api/ga_chi", 
            "genetic_algorithm_mi": "/api/ga_mi"
        }
    }

if __name__ == '__main__':
    app.run(debug=True)