import json
import random
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset_agricola_colombia.json"
MODEL_PATH = BASE_DIR / "model.pkl"

REGIONES = ["Boyacá", "Cundinamarca"]


def random_float(min_value: float, max_value: float, decimals: int = 2) -> float:
    return round(random.uniform(min_value, max_value), decimals)


def create_record(cultivo: int) -> dict:
    region = random.choice(REGIONES)

    if cultivo == 0:
        return {
            "ph": random_float(5.0, 6.2),
            "humedad": random_float(65, 90, 1),
            "temperatura": random_float(10, 18, 1),
            "tipo_suelo": random.choice([1, 2]),
            "region": region,
            "cultivo": cultivo,
        }

    if cultivo == 1:
        return {
            "ph": random_float(5.8, 6.8),
            "humedad": random_float(50, 70, 1),
            "temperatura": random_float(18, 26, 1),
            "tipo_suelo": 2,
            "region": region,
            "cultivo": cultivo,
        }

    return {
        "ph": random_float(6.0, 7.5),
        "humedad": random_float(40, 60, 1),
        "temperatura": random_float(12, 22, 1),
        "tipo_suelo": random.choice([0, 2]),
        "region": region,
        "cultivo": cultivo,
    }


def generate_dataset(total_records: int = 1200) -> pd.DataFrame:
    random.seed(42)
    records_per_crop = total_records // 3
    records = []

    for crop_code in [0, 1, 2]:
        records.extend(create_record(crop_code) for _ in range(records_per_crop))

    random.shuffle(records)

    with DATASET_PATH.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

    return pd.DataFrame(records)


def train_model() -> RandomForestClassifier:
    dataframe = generate_dataset()

    features = dataframe[["ph", "humedad", "temperatura", "tipo_suelo"]]
    target = dataframe["cultivo"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(model, MODEL_PATH)

    print(f"Dataset generado en: {DATASET_PATH}")
    print(f"Modelo guardado en: {MODEL_PATH}")
    print(f"Accuracy de prueba: {accuracy:.4f}")
    print(classification_report(y_test, predictions))

    return model


if __name__ == "__main__":
    train_model()
