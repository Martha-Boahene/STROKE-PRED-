import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
import joblib  

df = pd.read_csv("../data/dat.csv")

# Drop rows with missing target
df = df.dropna(subset=["stroke"])

# Define features and target
X = df.drop(columns=["stroke", "id"])
y = df["stroke"]

# --- Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Preprocessing ---
numeric_features = ["age", "avg_glucose_level", "bmi"]
categorical_features = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# --- Model pipeline ---
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# --- Train ---
model.fit(X_train, y_train)

# --- Save model ---
joblib.dump(model, "log_reg_model.joblib")

# --- Predict on test set ---
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # probability of stroke=1

# --- Accuracy ---
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.3f}")

# --- Confusion matrix ---
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# --- Classification report ---
print("Classification Report:")
print(classification_report(y_test, y_pred))

# --- ROC-AUC ---
roc_auc = roc_auc_score(y_test, y_proba)
print(f"ROC-AUC: {roc_auc:.3f}")