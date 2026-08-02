# EEG-Based Intelligent Web Application for Neurological Disorder Detection

This is a production-ready web application designed for a Final Year Major Project. It allows users to upload EEG datasets, analyzes brain waves, predicts neurological disorders using Machine Learning, and provides an AI medical chatbot. 
## Features
1. **EEG Data Upload**: Supports .csv, .edf, .txt formats.
2. **Signal Processing**: Band-pass filtering, noise removal, normalization.
3. **Brain Wave Analysis**: Extract Delta, Theta, Alpha, Beta, Gamma bands.
4. **Disorder Detection**: Predicts Epilepsy, Sleep Disorders, ADHD, Stress.
5. **AI Chatbot**: Medical chatbot for explaining results and answering questions.

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Chart.js
- **Backend**: Python, FastAPI
- **ML/Data**: Scikit-learn, Pandas, NumPy, SciPy, MNE

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Node.js (optional, for frontend serving if preferred, but not strictly required as it's vanilla JS)

### 2. Create a virtual environment
```bash
uv venv .venv
venv\Scripts\activate
```
### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will run at `http://127.0.0.1:8000`.

### 3. Frontend Setup
Simply open `frontend/index.html` in your browser.
For a better experience, use a simple HTTP server:
```bash
cd frontend
python -m http.server 3000
```
Then visit `http://localhost:3000`.

## Disclaimer
This system uses AI and Machine Learning for educational and research purposes only. It is **NOT** a certified medical diagnostic tool.
