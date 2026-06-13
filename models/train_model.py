import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def train_and_save():
    print("Загрузка датасета из репозитория GitHub...")
    raw_csv_url = "https://github.com/arolga-noo/Project---Implementation-of-Machine-Learning-Models/blob/main/data/UCI_Credit_Card.csv"
    
    try:
        df = pd.read_csv(raw_csv_url)
        print(f"Данные успешно загружены! Размерность: {df.shape}")
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return

    X = df.drop(columns=['ID', 'default.payment.next.month'])
    y = df['default.payment.next.month']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    all_features = X.columns.tolist()
    preprocessor = ColumnTransformer(
        transformers=[('scale', StandardScaler(), all_features)],
        remainder='drop'
    )
  
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            C=1.0, 
            solver='lbfgs', 
            max_iter=1000, 
            random_state=42, 
            class_weight='balanced'  # Компенсация дисбаланса классов
        ))
    ])
    
    print("Обучение модели Логистической Регрессии...")
    pipeline.fit(X_train, y_train)
    
    # Расчет метрики на обучении
    train_acc = pipeline.score(X_train, y_train)
    print(f"Обучение завершено. Точность (Accuracy) на Train: {train_acc:.4f}")
    
    # Сохранение весов строго по вашей архитектуре (в папку models/)
    os.makedirs('models', exist_ok=True)
    model_output_path = 'models/model_v1.pkl'
    
    with open(model_output_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"Модель LogisticRegression успешно сохранена в: {model_output_path}")

# ТОЧКА ВХОДА: Именно эта строка заставит скрипт работать при запуске из консоли
if __name__ == '__main__':
    train_and_save()
