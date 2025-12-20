from pandas import DataFrame
import pandas as pd
import sys
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from us_visa.exceptions import CustomException
from us_visa.logger import logging
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.utlis.main_utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)
        
    def validate_num_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Required columns present:{status}")
            return status
        except Exception as e:
            raise CustomException(e, sys)
        
    def is_column_exist(self, dataframe: DataFrame) -> bool:
        try:
            dataframe_columns = dataframe.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical columns:{missing_categorical_columns}")

            return False if len(missing_categorical_columns)>0 and len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise CustomException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
        
    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_msg = ""
            logging.info("Data Validation Started.")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path), DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            req_columns_status = self.validate_num_of_columns(dataframe=train_df)
            logging.info(f"All required columns are present in training df: {req_columns_status}")
            if not req_columns_status:
                validation_error_msg += f"Columns are missing in train df."

            req_columns_status = self.validate_num_of_columns(dataframe=test_df)
            logging.info(f"All required columns are present in training df: {req_columns_status}")
            if not req_columns_status:
                validation_error_msg += f"Columns are missing in test df."
            
            status = self.is_column_exist(dataframe=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training df."
            
            status = self.is_column_exist(dataframe=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in testing df."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info("Drift detected.")
                    validation_error_msg = "drift detected"
                else:
                    validation_error_msg = "drift not detected"
            else:
                logging.info(f"Validation error:{validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(validation_status=validation_status, message=validation_error_msg, drift_report_file_path= self.data_validation_config.drift_report_file_path)

            logging.info(f"Data Validation Artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)
            


        

                    
        
        