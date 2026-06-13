import os
import pickle

def load_model_for_inference():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.abspath(os.path.join(current_dir, '../models/model_v1.pkl'))

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Ошибка"
        )

    with open(model_path, 'rb') as f:
        loaded_pipeline = pickle.load(f)
        
    print("Пайплайн  успешно загружен")
    return loaded_pipeline
