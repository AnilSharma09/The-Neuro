import numpy as np
from scipy.signal import welch

def extract_brain_waves(data, fs):
    """
    Extracts power spectral density for Delta, Theta, Alpha, Beta, Gamma bands.
    """
    # Define frequency bands
    bands = {
        'Delta': (0.5, 4),
        'Theta': (4, 8),
        'Alpha': (8, 13),
        'Beta': (13, 30),
        'Gamma': (30, 100)
    }

    # Calculate Power Spectral Density (PSD) using Welch's method
    freqs, psd = welch(data, fs, nperseg=fs*2)

    features = {}
    total_power = np.sum(psd)

    for band, (low, high) in bands.items():
        # Find indices of frequencies within the band
        idx_band = np.logical_and(freqs >= low, freqs <= high)
        band_power = np.sum(psd[idx_band])
        
        # Calculate relative power
        relative_power = band_power / total_power if total_power > 0 else 0
        features[band] = relative_power

    return features

def get_signal_stats(data):
    """
    Returns basic statistical features: Mean, Std, Max, Min.
    """
    return {
        "mean": np.mean(data),
        "std": np.std(data),
        "max": np.max(data),
        "min": np.min(data)
    }
