from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import numpy as np

# Import our modules
from eeg_processing import read_eeg_file, bandpass_filter, remove_artifacts, normalize_signal
from feature_extraction import extract_brain_waves, get_signal_stats
from ml_models import predictor
from chatbot import chatbot

app = FastAPI(title="EEG-Based Neurological Disorder Detection")

# CORS setup to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ChatRequest(BaseModel):
    message: str

class AnalysisResponse(BaseModel):
    features: dict
    prediction: dict
    signal_stats: dict
    message: str

@app.on_event("startup")
async def startup_event():
    # Initialize/Load models on startup
    predictor.load_models()

@app.get("/")
def read_root():
    return {"message": "EEG Disorder Detection API is running"}

@app.post("/upload", response_model=AnalysisResponse)
async def upload_eeg(file: UploadFile = File(...)):
    """
    Handle EEG file upload, process it, and return analysis results + predictions.
    """
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save uploaded file momentarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Processing
        try:
            raw_data, fs = read_eeg_file(temp_file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        filtered_data = bandpass_filter(raw_data, fs)
        clean_data = remove_artifacts(filtered_data)
        # normalized_data = normalize_signal(clean_data) # Optional for viz, but features extract from raw/filtered usually

        # 2. Feature Extraction
        features = extract_brain_waves(clean_data, fs)
        stats = get_signal_stats(clean_data)

        # 3. Prediction
        prediction_result = predictor.predict(features)

        return {
            "features": features,
            "prediction": prediction_result,
            "signal_stats": {k: float(v) for k, v in stats.items()}, # Ensure floats for JSON
            "message": "Analysis successful"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/chat")
def chat_with_bot(request: ChatRequest):
    response = chatbot.get_response(request.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
