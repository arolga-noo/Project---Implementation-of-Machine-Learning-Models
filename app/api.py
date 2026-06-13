import time
import json
import pandas as pd
from flask import Flask, request, jsonify
from app.model_handler import load_model_for_inference

app = Flask(__name__)
model_pipeline = None

def get_model():
    global model_pipeline
    if model_pipeline is None:
        model_pipeline = load_model_for_inference()
    return model_pipeline

with app.app_context():
    try:
        get_model()
    except Exception as e:
        app.logger.error(f"Ошибка при стартовой загрузке модели: {e}")

@app.route('/health', methods=['GET'])
def health():
    if model_pipeline is None:
        return jsonify({
            "status": "unhealthy", 
            "error": "Модель не загружена"
        }), 503
    return jsonify({
        "status": "healthy", 
        "model_version": "v1.0"
    }), 200

@app.route('/predict', methods=['POST'])
def predict():   
    start_time = time.time()
    try:
        data = request.get_json(force=True)
      
        if not data or 'features' not in data:
            return jsonify({"error": "Отсутствует обязательный ключ 'features' в теле запроса"}), 400
            
        features_list = data['features']
        df_input = pd.DataFrame(features_list)
        
        pipeline = get_model()
        pipeline.named_steps['classifier'].multi_class = 'deprecated'
        probabilities = pipeline.predict_proba(df_input)[:, 1]
        predictions = pipeline.predict(df_input)
     
        response_results = []
        for pred, prob in zip(predictions, probabilities):
            response_results.append({
                "default_probability": round(float(prob), 4),
                "prediction": int(pred),
                "verdict": "Reject (High Risk)" if pred == 1 else "Approve"
            })
        
        log_metrics = {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "batch_size": len(features_list)
        }
        print(json.dumps(log_metrics))
            
        return jsonify({"results": response_results}), 200

    except Exception as e:
        return jsonify({"error": f"Внутренняя ошибка сервера при инференсе: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
