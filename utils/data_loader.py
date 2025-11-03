import pandas as pd
import numpy as np
from io import StringIO
import os

def process_csv_data(file_stream):
    try:
        if hasattr(file_stream, 'seek'):
            file_stream.seek(0)
            
        stream = StringIO(file_stream.read().decode("UTF8"), newline=None)
        df = pd.read_csv(stream)
        
        if df.shape[0] < 10:
            raise ValueError("CSV must have at least 10 rows for meaningful analysis")
            
        if df.shape[1] < 2:
            raise ValueError("CSV must have at least 2 columns (features + target)")
        
        if df.isnull().any().any():
            df = df.dropna()
            if len(df) < 10:
                raise ValueError("Too many missing values. After cleaning, less than 10 rows remain.")
        
        X = df.iloc[:, :-1].values 
        y = df.iloc[:, -1].values  
        
        unique_classes = np.unique(y)
        if len(unique_classes) < 2:
            raise ValueError("Target variable must have at least 2 classes")
        
        target_dtype = df.iloc[:, -1].dtype
        if not (np.issubdtype(target_dtype, np.number) or len(unique_classes) <= 20):
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            y = le.fit_transform(y)
            unique_classes = np.unique(y)
        
        feature_names = df.columns[:-1].tolist()
        target_column = df.columns[-1]
        
        feature_names = [str(name) for name in feature_names]
        target_column = str(target_column)
        unique_classes = [str(cls) for cls in unique_classes.tolist()]
        
        return X, y, df, feature_names, target_column, unique_classes
        
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except pd.errors.ParserError:
        raise ValueError("CSV file could not be parsed. Please check the file format.")
    except UnicodeDecodeError:
        raise ValueError("CSV file encoding issue. Please use UTF-8 encoding.")
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {str(e)}")


def load_sample_data():
    possible_paths = [
        'data/sample_data.csv',
        '../data/sample_data.csv',
        './data/sample_data.csv',
        'sample_data.csv'
    ]
    
    sample_path = None
    for path in possible_paths:
        if os.path.exists(path):
            sample_path = path
            break
    
    if not sample_path:
        raise FileNotFoundError(
            f"Sample data file not found. Tried: {', '.join(possible_paths)}"
        )
    
    try:
        df = pd.read_csv(sample_path)
        
        if df.shape[0] < 10:
            raise ValueError("Sample data must have at least 10 rows")
            
        if df.shape[1] < 2:
            raise ValueError("Sample data must have at least 2 columns (features + target)")
        
        if df.isnull().any().any():
            df = df.dropna()
            if len(df) < 10:
                raise ValueError("Sample data has too many missing values")
        
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        
        unique_classes = np.unique(y)
        if len(unique_classes) < 2:
            raise ValueError("Target variable must have at least 2 classes")
        
        target_dtype = df.iloc[:, -1].dtype
        if not (np.issubdtype(target_dtype, np.number) or len(unique_classes) <= 20):
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            y = le.fit_transform(y)
            unique_classes = np.unique(y)
        
        feature_names = df.columns[:-1].tolist()
        target_column = df.columns[-1]
        
        feature_names = [str(name) for name in feature_names]
        target_column = str(target_column)
        unique_classes = [str(cls) for cls in unique_classes.tolist()]
        
        return X, y, df, feature_names, target_column, unique_classes
        
    except pd.errors.EmptyDataError:
        raise ValueError("Sample data file is empty")
    except pd.errors.ParserError:
        raise ValueError("Sample data file could not be parsed")
    except Exception as e:
        raise ValueError(f"Error loading sample data: {str(e)}")


def validate_data(X, y, feature_names):
    validation_results = {
        "is_valid": True,
        "warnings": [],
        "errors": []
    }
    
    if not isinstance(X, (np.ndarray, list)):
        validation_results["errors"].append("Features must be a numpy array or list")
        validation_results["is_valid"] = False
    
    if not isinstance(y, (np.ndarray, list)):
        validation_results["errors"].append("Target must be a numpy array or list")
        validation_results["is_valid"] = False
    
    if len(X) != len(y):
        validation_results["errors"].append("Number of samples in X and y must match")
        validation_results["is_valid"] = False
    
    if len(feature_names) != X.shape[1]:
        validation_results["warnings"].append(
            f"Number of feature names ({len(feature_names)}) doesn't match number of features ({X.shape[1]})"
        )
    
    constant_features = []
    for i in range(X.shape[1]):
        if len(np.unique(X[:, i])) == 1:
            constant_features.append(feature_names[i] if i < len(feature_names) else f"Feature_{i}")
    
    if constant_features:
        validation_results["warnings"].append(
            f"Constant features detected: {', '.join(constant_features[:5])}"
            + ("..." if len(constant_features) > 5 else "")
        )
    
    return validation_results


def get_data_summary(df, target_column):
    summary = {
        "dataset_info": {
            "total_rows": int(len(df)),
            "total_columns": int(len(df.columns)),
            "features_count": int(len(df.columns) - 1),
            "target_column": str(target_column)
        },
        "target_distribution": {},
        "data_types": {},
        "missing_values": {}
    }
    
    target_series = df[target_column]
    target_counts = target_series.value_counts()
    summary["target_distribution"] = {
        str(cls): int(count) for cls, count in target_counts.items()
    }
    
    for col in df.columns:
        summary["data_types"][str(col)] = str(df[col].dtype)
    
    missing_counts = df.isnull().sum()
    summary["missing_values"] = {
        str(col): int(count) for col, count in missing_counts.items() if count > 0
    }
    
    return summary