"""
Standalone script to train the Machine Learning models.
Usage: Place 'data.csv' in the 'dataset/' folder and run this script.
The CSV should have columns for features (Delta, Theta, Alpha, Beta, Gamma) and a 'label' column.
"""

import pandas as pd
import numpy as np
import os
import sys

# Add backend to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ml_models import predictor

DATASET_PATH = "../dataset/data.csv"

def train_models():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        print("Please place a CSV file with extracted features and a 'label' column there.")
        print("Expected columns: Delta, Theta, Alpha, Beta, Gamma, label")
        return

    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    # Check columns
    required_cols = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma', 'label']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Dataset missing required columns. Needs: {required_cols}")
        return

    X = df[['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']].values
    y = df['label'].values

    print(f"Training on {len(X)} samples...")
    predictor.train(X, y)
    print("Training complete. Models saved to 'models.pkl'.")

if __name__ == "__main__":
    train_models()
