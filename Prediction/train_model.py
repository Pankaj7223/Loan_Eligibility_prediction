import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_and_save_model():
    # 1. Load Dataset
    print("Loading dataset...")
    try:
        df = pd.read_csv('loan_dataset.csv')
    except FileNotFoundError:
        print("Error: loan_dataset.csv not found.")
        return

    # 2. Clean Column Names
    df.columns = df.columns.str.strip()
    
    # 3. Drop Unused Columns
    # 'loan_id': ID column
    # 'commercial_assets_value': Not present in frontend form
    drop_cols = ['loan_id', 'commercial_assets_value']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # 4. Clean String Values (remove spaces)
    obj_cols = df.select_dtypes(include=['object']).columns
    for col in obj_cols:
        df[col] = df[col].str.strip()

    # 5. Define Features and Target
    target = 'loan_status'
    X = df.drop(target, axis=1)
    y = df[target].map({'Approved': 1, 'Rejected': 0}) # Encode target

    # 6. Identify Feature Types
    numeric_features = [
        'no_of_dependents', 'income_annum', 'loan_amount', 'loan_term', 
        'cibil_score', 'residential_assets_value', 'luxury_assets_value', 
        'bank_asset_value'
    ]
    categorical_features = ['education', 'self_employed']

    # Verify all columns exist
    missing_cols = [col for col in numeric_features + categorical_features if col not in X.columns]
    if missing_cols:
        print(f"Error: Missing columns in CSV: {missing_cols}")
        return

    print(f"Numeric features: {numeric_features}")
    print(f"Categorical features: {categorical_features}")

    # 7. Build Preprocessing Pipeline
    # Numeric: Impute missing with Median, Scale
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical: Impute missing with Mode, OneHotEncode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Combine
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # 8. Create Full Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # 9. Train Model
    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    # Print Feature Importance
    try:
        rf = pipeline.named_steps['classifier']
        importances = rf.feature_importances_
        # Get feature names from preprocessor
        # Note: This can be tricky with pipelines, simplified attempt:
        print("\nFeature Importances (Indices):")
        for i, v in enumerate(importances):
            print(f"Feature {i}: {v:.4f}")
    except Exception as e:
        print(f"Could not print feature importance: {e}")

    # 10. Evaluate
    score = pipeline.score(X_test, y_test)
    print(f"Model Accuracy: {score:.4f}")

    # 11. Save Model
    save_dir = 'ML_model'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    save_path = os.path.join(save_dir, 'loanprediction_model.sav')
    joblib.dump(pipeline, save_path)
    print(f"Model saved to {save_path}")

    # Save feature structure for backend validation
    feature_info = {
        'numeric': numeric_features,
        'categorical': categorical_features
    }
    joblib.dump(feature_info, os.path.join(save_dir, 'model_features.pkl'))

if __name__ == "__main__":
    train_and_save_model()
