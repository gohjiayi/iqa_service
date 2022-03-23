from fastapi import FastAPI
from app.models.model import IQAModel
from typing import Callable
import logging
CNN_PATH = r"deepbiq_deploy/model_best.pth"
SVR_PATH = r"deepbiq_deploy/svr.pkl"
SCALER_PATH = r"deepbiq_deploy/data_y_all.pkl" # all the ground-truth MOS (standardized) of the combined dataset
def _startup_model(app: FastAPI) -> None:
    model_instance = IQAModel(CNN_PATH, SVR_PATH, SCALER_PATH)
    app.state.model = model_instance
    
def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None

def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logging.info("Running app start handler.")
        _startup_model(app)
    return startup

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logging.info("Running app shutdown handler.")
        _shutdown_model(app)
    return shutdown
