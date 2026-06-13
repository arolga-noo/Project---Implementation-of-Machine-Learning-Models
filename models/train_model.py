import os
import pickle

def save_model_artifact(pipeline, directory='models', filename='model_v1.pkl'):
    os.makedirs(directory, exist_ok=True)

    filepath = os.path.join(directory, filename)
  
    with open(filepath, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"Модель успешно сериализована и сохранена: {filepath}")
