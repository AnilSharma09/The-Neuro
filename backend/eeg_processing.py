import pandas as pd
import numpy as np
import scipy.signal as signal
import mne
import os

def read_eeg_file(file_path):
    """
    Reads EEG data from .csv, .txt, or .edf files.
    Returns:
        raw_data (numpy array): The EEG signal data.
        fs (int): Sampling frequency (default assumed 256Hz if not found).
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.csv' or ext == '.txt':
        try:
            # Assuming standard CSV format where rows are time, cols are channels or vice versa
            # For simplicity, taking the first column (single channel) or averaging
            df = pd.read_csv(file_path)
            # Check if headers exist, if not reread
            if df.shape[1] < 1:
                raise ValueError("Empty file")
            
            # Simple heuristic: if many columns, likely multi-channel. 
            # We will flatten or average for single-channel disorder indicators or use 'FP1-F7' if available.
            # For this MVP: take the first numeric column as the primary signal.
            data = df.select_dtypes(include=[np.number]).iloc[:, 0].values
            
            fs = 173.61 # Standard for many datasets like Bonn (Kaggle), or 256. 
            # We'll default to 173.61 (Kaggle Epileptic Seizure) or 250/256. Let's use 256 as a safe default if unknown.
            # ideally, we'd infer fs from timestamps.
            return data, 256
        except Exception as e:
            raise ValueError(f"Error reading CSV/TXT: {e}")

    elif ext == '.edf':
        try:
            raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
            data = raw.get_data() # (n_channels, n_times)
            # Pick first channel for analysis
            return data[0, :], int(raw.info['sfreq'])
        except Exception as e:
            raise ValueError(f"Error reading EDF: {e}")
    
    else:
        raise ValueError("Unsupported file format")

def bandpass_filter(data, fs, lowcut=0.5, highcut=50.0, order=5):
    """
    Applies a Butterworth bandpass filter.
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, data)

def remove_artifacts(data):
    """
    Simple artifact removal using thresholding (e.g., clipping high amplitude noise).
    """
    # Clip values beyond 3 standard deviations
    mean = np.mean(data)
    std = np.std(data)
    threshold = 3 * std
    return np.clip(data, mean - threshold, mean + threshold)

def normalize_signal(data):
    """
    Normalize signal to -1 to 1 range or z-score.
    Here using Min-Max scaling for visualization mostly.
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data)) * 2 - 1
