import pandas as pd
import sys
import os
from sklearn.model_selection import train_test_split
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exceptions import CustomException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USVisaData


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        

    def export_data_into_feature_store(self)->pd.DataFrame:
        try:
            logging.info("Exporting data from MongoDB")
            usvisa_data = USVisaData()
            dataframe = usvisa_data.export_collection_as_df(collection_name=self.data_ingestion_config.collection_name)
            logging.info("Shape of dataframe:", dataframe.shape)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving data into feature store file path:{feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise CustomException(e, sys)
        

    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_df, test_df = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path.")
            train_df.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) ->DataIngestionArtifact:

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")

            self.split_data_as_train_test(dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)

