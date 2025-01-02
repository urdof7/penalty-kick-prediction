import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import shap
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_SINGLE_FRAME = os.path.join(DATA_DIR, 'processed', 'single_frame', 'training_data_single_frame.csv')
REPORT_DIR = os.path.join(BASE_DIR, 'report', 'single_frame')
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'single_frame_models')

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

df = pd.read_csv(PROCESSED_SINGLE_FRAME)

target_col = 'kick_direction'
non_feature_cols = ['frame_id', 'kick_direction']
features = [c for c in df.columns if c not in non_feature_cols]
X = df[features]
y = df[target_col]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

train_acc = model.score(X_train_scaled, y_train)
test_acc = model.score(X_test_scaled, y_test)
print(f"Train Accuracy: {train_acc:.2f}")
print(f"Test Accuracy: {test_acc:.2f}")

feature_importances = model.feature_importances_
fi_gini = pd.DataFrame({
    'feature': X.columns,
    'importance': feature_importances
}).sort_values('importance', ascending=False)

fi_gini_path = os.path.join(REPORT_DIR, 'feature_importances_gini_single_frame.csv')
fi_gini.to_csv(fi_gini_path, index=False)
print(f"Gini-based feature importances saved to {os.path.relpath(fi_gini_path, BASE_DIR)}")

perm_import = permutation_importance(model, X_test_scaled, y_test, n_repeats=10, random_state=42)
fi_perm = pd.DataFrame({
    'feature': X.columns,
    'importance_mean': perm_import.importances_mean,
    'importance_std': perm_import.importances_std
}).sort_values('importance_mean', ascending=False)

fi_perm_path = os.path.join(REPORT_DIR, 'feature_importances_permutation_single_frame.csv')
fi_perm.to_csv(fi_perm_path, index=False)
print(f"Permutation feature importances saved to {os.path.relpath(fi_perm_path, BASE_DIR)}")

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test_scaled)

plt.figure(figsize=(10,6))
shap.summary_plot(shap_values, X_test_scaled, feature_names=X.columns, show=False)
shap_plot_path = os.path.join(REPORT_DIR, 'shap_summary_plot_single_frame.png')
plt.savefig(shap_plot_path, bbox_inches='tight')
plt.close()
print(f"SHAP summary plot saved to {os.path.relpath(shap_plot_path, BASE_DIR)}")

model_path = os.path.join(MODELS_DIR, 'random_forest_single_frame_model.pkl')
joblib.dump(model, model_path)
print(f"Trained model saved to {os.path.relpath(model_path, BASE_DIR)}")
