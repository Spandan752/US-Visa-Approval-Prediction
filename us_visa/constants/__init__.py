import os
from datetime import date

DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "visa_datasets"
MONGODB_URL_KEY = "mongodb+srv://spandanpagar2002_db_user:spandanpagar2002_db_user@cluster0.uchraog.mongodb.net/?appName=Cluster0"
PIPELINE_NAME : str = "usvisa"
ARTIFACT_DIR : str = "artifact"
FILE_NAME = "usvisa.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
MODEL_FILE_NAME = "model.pkl"

# Data ingestion related constants
DATA_INGESTION_COLLECTION_NAME: str = "visa_datasets"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2