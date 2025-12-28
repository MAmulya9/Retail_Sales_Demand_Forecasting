import os
import pickle
from tensorflow.keras.models import load_model

def load_lgbm_models():
    with open("models/lgbm_storewise_models.pkl", "rb") as f:
        return pickle.load(f)

def load_exp_models():
    with open("models/exp_smoothing_storewise_models.pkl", "rb") as f:
        return pickle.load(f)



