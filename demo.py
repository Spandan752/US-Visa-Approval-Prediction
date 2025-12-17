# from us_visa.logger import logging
# from us_visa.exceptions import CustomException
# import sys

# # logging.info("Demo logger initialized")
# try:
#     a = 1/0

# except Exception as e:
#     raise CustomException(e, sys)

from us_visa.pipelines.training_pipeline import TrainingPipeline

obj = TrainingPipeline()
obj.run_pipeline()