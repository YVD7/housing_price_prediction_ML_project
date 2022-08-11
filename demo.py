import os

from pexpect import ExceptionPexpect
from housing.component import data_validation
from housing.pipeline.pipeline import pipeline
from housing.exception import HousingException 
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformaiton


def main():
    try:
        pipeline = pipeline()
        # pipeline.run_pipeline()

        # data_validation_config = Configuration().get_data_validation_config()
        # print(data_validation_config)
        pipeline.start()
        logging.info("main function execution completed.")
    except Exception as e:
        logging.error(f"{e}")
        print(e)
    