# Внедрение модели прогнозирования дефолта по кредитным картам

## 📌 Описание проекта и его целей
**Цель проекта:** Разработка, контейнеризация и подготовка к промышленной эксплуатации веб-сервиса машинного обучения для оценки кредитных рисков в реальном времени (Online Scoring). 

Сервис анализирует демографические показатели и историю платежей клиента, прогнозируя вероятность дефолта по кредитной карте в следующем месяце.
*   **Бизнес-контекст:** Снижение финансовых потерь банка от невозврата средств за счет точечной фильтрации высокорисковых заявок (вердикт `Reject`).
*   **Датасет:** Default of Credit Card Clients Dataset (UCI Machine Learning Repository).
*   **Модель:** Пайплайн логистической регрессии (`LogisticRegression`) со сквозным масштабированием признаков (`StandardScaler`).

---

## 🛠️ Инструкция по запуску

### Вариант 1. Локальный запуск (в изолированном окружении)
1. Склонируйте репозиторий и перейдите в его корень:
   ```bash
   git clone https://github.com
   cd Project---Implementation-of-Machine-Learning-Models
   ```
2. Создайте и активируйте виртуальное окружение `venv`:
   * **Для Linux / macOS / Git Bash:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Для Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
3. Установите зафиксированные зависимости проекта:
   ```bash
   pip install -r requirements.txt
   ```
4. Обучите модель (скрипт скачает датасет с GitHub и создаст файл `models/model_v1.pkl`):
   ```bash
   python models/train_model.py
   ```
5. Запустите Flask веб-сервис:
   ```bash
   python app/api.py
   ```
Приложение станет доступно по адресу: `http://localhost:5000`

### Вариант 2. Запуск в Docker-контейнере
1. Соберите Docker-образ из корня репозитория:
   ```bash
   docker build -f docker/Dockerfile -t credit-card-ml-service:v1.0 .
   ```
2. Запустите изолированный контейнер:
   ```bash
   docker run -d -p 5000:5000 --name credit_app_container credit-card-ml-service:v1.0
   ```

### Вариант 3. Промышленный запуск через Docker Compose (с Nginx)
Разверните весь контур (Flask-сервис + прокси-сервер Nginx для логирования трафика) одной командой:
```bash
docker-compose up -d
```
В этом режиме сервис будет доступен на стандартном веб-порту `80`: `http://localhost/`

---

## 🌐 Формат запросов, ответов и примеры (curl-команды)

### 1. Проверка работоспособности сервиса (GET /health)
Используется для мониторинга статуса приложения и прогрева модели в памяти.

*   **Пример curl-команды:**
    ```bash
    curl http://localhost:5000/health
    ```
*   **Формат ответа (JSON, Status 200):**
    ```json
    {
      "model_version": "v1.0",
      "status": "healthy"
    }
    ```

### 2. Пакетный инференс модели (POST /predict)
Принимает массив словарей с признаками клиентов в ключе `"features"`. Поддерживает батч-скоринг.

*   **Пример curl-команды:**
    ```bash
    curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [{"LIMIT_BAL": 50000, "SEX": 1, "EDUCATION": 1, "MARRIAGE": 2, "AGE": 37, "PAY_0": 2, "PAY_2": 2, "PAY_3": 0, "PAY_4": 0, "PAY_5": 0, "PAY_6": 0, "BILL_AMT1": 46990, "BILL_AMT2": 48233, "BILL_AMT3": 49291, "BILL_AMT4": 28314, "BILL_AMT5": 28959, "BILL_AMT6": 29547, "PAY_AMT1": 0, "PAY_AMT2": 2000, "PAY_AMT3": 1200, "PAY_AMT4": 1100, "PAY_AMT5": 1069, "PAY_AMT6": 1000}]}'
    ```
*   **Формат ответа (JSON, Status 200):**
    ```json
    {
      "results": [
        {
          "default_probability": 0.6841,
          "prediction": 1,
          "verdict": "Reject (High Risk)"
        }
      ]
    }
    ```

---

## 🐳 Ссылка на Docker Hub
Готовый к эксплуатации и полностью собранный образ проекта опубликован в публичном репозитории:
[https://docker.com](https://docker.com)  
*(Замените `your_username` на ваш реальный логин Docker Hub после загрузки образа)*
https://hub.docker.com/repository/docker/olgaarykova/credit-card-ml-service/general
