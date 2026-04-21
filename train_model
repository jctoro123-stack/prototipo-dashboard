import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Cargar dataset
df = pd.read_csv("cardio_train.csv", sep=";")

# Preprocesamiento
df["age"] = (df["age"] / 365).astype(int)

df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

# Eliminar ID
df.drop("id", axis=1, inplace=True)

# Variables
X = df.drop("cardio", axis=1)
y = df["cardio"]

# Escalado
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# División
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Modelo XGBoost
modelo = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    random_state=42
)

modelo.fit(X_train, y_train)

# Guardar modelo
joblib.dump(modelo, "modelo_xgb.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Modelo guardado correctamente")
