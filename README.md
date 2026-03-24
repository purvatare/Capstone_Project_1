# 🏭 Manufacturing Output Prediction System
👉 Runs at: http://localhost:8501

An AI-powered web application that predicts manufacturing output based on machine parameters, performance metrics, and operational conditions.

---

## 📌 Features

- 🔮 Predict manufacturing output using Machine Learning
- 📊 Interactive UI built with Streamlit
- ⚙️ FastAPI backend for model inference
- 📈 Live chart: Output vs Efficiency
- 🎛️ Dynamic inputs (sliders, toggles, dropdowns)
- 🎨 Modern UI with Glassmorphism & Dark Theme

---

## 🧠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **ML Model:** Linear Regression (Scikit-learn)
- **Visualization:** Plotly
- **Language:** Python

---

## 📂 Project Structure

manufacturing-output-prediction/
├── app/
│   └── main.py
├── frontend/
│   └── app.py
├── models/
│   ├── linear_regression_model.pkl
│   └── scaler.pkl
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Setup Instructions
```bash
1️⃣ Clone the repository
git clone https://github.com/your-username/manufacturing-output-prediction.git
cd manufacturing-output-prediction
2️⃣ Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
3️⃣ Install dependencies
pip install -r requirements.txt
(or manually)

pip install fastapi uvicorn scikit-learn joblib streamlit plotly
4️⃣ Run Backend (FastAPI)
uvicorn app.main:app --reload

5️⃣ Run Frontend (Streamlit)
Open a new terminal:

source venv/bin/activate
streamlit run frontend/app.py
👉 Runs at: http://localhost:8501

📊 How It Works
User inputs machine & operational parameters
Data is sent to FastAPI backend
ML model predicts output
Result is displayed with a live visualization

🐳 Docker Support
The project includes:

Multi-stage Docker setup (separate backend & frontend)
Proper environment variable handling (BACKEND_URL)
Optimized Dockerfiles with minimal image size
.dockerignore for clean builds

🛠️ Useful Docker Commands
Command,Description
docker compose up -d,Start the app in background
docker compose down,Stop and remove containers
docker compose restart,Restart both services
docker compose restart frontend,Restart only frontend
docker compose logs -f,View real-time logs
docker compose build --no-cache,Rebuild images after code changes

App URLs:

Frontend (Streamlit) → http://localhost:8501
Backend API Docs → http://localhost:8000/docs

📸 Screenshots
<img width="1440" height="858" alt="image" src="https://github.com/user-attachments/assets/eff9338c-4a80-462b-8694-fdc7568b1167" />
<img width="1440" height="859" alt="image" src="https://github.com/user-attachments/assets/2ba9b582-7eda-4568-a75b-fe6e7f3dd6ea" />


