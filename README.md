# EEG-Based Intelligent Web Application for Neurological Disorder Detection

This is a production-ready web application designed for a Final Year Major Project. It allows users to upload EEG datasets, analyzes brain waves, predicts neurological disorders using Machine Learning, and provides an AI medical chatbot.

## Features

1. **EEG Data Upload**: Supports `.csv`, `.edf`, `.txt` formats.
2. **Signal Processing**: Band-pass filtering, noise removal, normalization.
3. **Brain Wave Analysis**: Extract Delta, Theta, Alpha, Beta, Gamma bands.
4. **Disorder Detection**: Predicts Epilepsy, Sleep Disorders, ADHD, Stress.
5. **AI Chatbot**: Medical chatbot for explaining results and answering questions.

## Tech Stack

<div align="center">

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

</div>

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5 · CSS3 · JavaScript (Vanilla) · Chart.js |
| **Backend** | Python · FastAPI |
| **ML / Data** | Scikit-learn · Pandas · NumPy · SciPy · MNE |

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Node.js (optional, for frontend serving if preferred, but not strictly required as it's vanilla JS)

### 2. Create a Virtual Environment

```bash
uv venv .venv
venv\Scripts\activate
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

### 4. Frontend Setup

Simply open `frontend/index.html` in your browser.

For a better experience, use a simple HTTP server:

```bash
cd frontend
python -m http.server 3000
```

Then visit `http://localhost:3000`.

## Disclaimer

This system uses AI and Machine Learning for educational and research purposes only. It is **NOT** a certified medical diagnostic tool.
