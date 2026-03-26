import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# Define model paths
MODEL_PATH = "models.pkl"

class DisorderPredictor:
    def __init__(self):
        self.models = {
            "RandomForest": RandomForestClassifier(n_estimators=100),
            "SVM": SVC(probability=True),
            "LogisticRegression": LogisticRegression()
        }
        self.is_trained = False

    def train(self, X, y):
        """
        Trains all models on the provided data.
        """
        for name, model in self.models.items():
            model.fit(X, y)
        self.is_trained = True
        self.save_models()

    def predict(self, features):
        """
        Predicts disorder probabilities using the trained models.
        features: dict or array corresponding to [Delta, Theta, Alpha, Beta, Gamma]
        """
        if not self.is_trained:
            self.load_models()
        
        # Convert dictionary features to array if needed
        if isinstance(features, dict):
            # Ensure order matches training: Delta, Theta, Alpha, Beta, Gamma
            feature_vector = np.array([[features['Delta'], features['Theta'], 
                                        features['Alpha'], features['Beta'], features['Gamma']]])
        else:
            feature_vector = np.array([features])

        results = {}
        for name, model in self.models.items():
            prediction = model.predict(feature_vector)[0]
            probability = model.predict_proba(feature_vector)[0]
            results[name] = {
                "prediction": prediction,
                "confidence": float(np.max(probability))
            }
        
        # Aggregated result (Voting or specific preference)
        # Using Random Forest as primary
        primary_pred = results["RandomForest"]["prediction"]
        risk_level = "High" if primary_pred != "Normal" else "Low"
        
        return {
            "disorder": primary_pred,
            "risk_level": risk_level,
            "details": results
        }

    def save_models(self):
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(self.models, f)

    def load_models(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                self.models = pickle.load(f)
            self.is_trained = True
        else:
            print("No models found. Training dummy models for demo...")
            self.train_dummy_models()

    def train_dummy_models(self):
        """
        Trains on synthetic data to ensure the system works out-of-the-box.
        Classes: Normal, Epilepsy, Sleep Disorder, ADHD, Stress
        """
        # Generate synthetic data
        # Features: Delta, Theta, Alpha, Beta, Gamma
        # Heuristics:
        # Normal: Balanced (Alpha dominant)
        # Epilepsy: High spikes (Gamma/Beta variations, often high amplitude but here simplified to spectral)
        # Sleep: High Delta/Theta
        # ADHD: High Theta, Low Beta
        # Stress: High Beta/Gamma
        
        X = []
        y = []
        
        for _ in range(50):
            # Normal
            X.append([0.2, 0.1, 0.4, 0.2, 0.1]) 
            y.append("Normal")
            # Epilepsy
            X.append([0.1, 0.1, 0.1, 0.3, 0.4])
            y.append("Epilepsy")
            # Sleep Apnea / Disorder
            X.append([0.5, 0.3, 0.1, 0.05, 0.05])
            y.append("Sleep Disorder")
            # ADHD
            X.append([0.1, 0.5, 0.2, 0.1, 0.1])
            y.append("ADHD")
            # Stress
            X.append([0.1, 0.1, 0.1, 0.5, 0.2])
            y.append("Stress")
            
        self.train(X, y)
        print("Dummy models trained and saved.")

# Global instance
predictor = DisorderPredictor()
