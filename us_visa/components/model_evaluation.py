import sys, pandas as pd
from typing import Optional
from sklearn.metrics import f1_score
from dataclasses import dataclass
from us_visa.constants import TARGET_COLUMN, CURRENT_YEAR
from us_visa.entity.artifact_entity import ModelEvaluationArtifact, ModelTrainerArtifact, DataIngestionArtifact
from us_visa.entity.config_entity import ModelEvaluationConfig
from us_visa.entity.s3_estimator import USvisaEstimator
from us_visa.entity.estimator import USVisaModel, TargetValueMapping
from us_visa.exceptions import CustomException
from us_visa.logger import logging


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: float
    difference :float

class ModelEvaluation:
    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        

