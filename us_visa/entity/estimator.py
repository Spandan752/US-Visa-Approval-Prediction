import pandas as pd
from pandas import DataFrame
from us_visa.exceptions import CustomException
from us_visa.logger import logging
from sklearn.pipeline import Pipeline
import sys

class TargetValueMapping:
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_result = self._asdict()
        return dict(zip(mapping_result.values(), mapping_result.keys()))
    

class USVisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
    
    def predict(self, dataframe: DataFrame) -> DataFrame:
        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def  __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"



