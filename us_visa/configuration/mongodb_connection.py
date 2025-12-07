import sys
import os
import pymongo
import certifi
from us_visa.exceptions import CustomException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()

class MongoDBClient:
    """
    Class Name: 
    """

    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
                logging.info("MongoDB connection successful")
        except Exception as e:
            raise CustomException(e,sys)