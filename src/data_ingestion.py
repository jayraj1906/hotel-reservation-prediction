import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.commmon_functions import read_yaml

logger=get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config=config["data_ingestion"]
        self.bucket_name=self.config["bucket_name"]
        self.bucket_file_name=self.config["bucket_file_name"]
        self.train_ratio=self.config["train_ratio"]
        os.makedirs(RAW_DIR,exist_ok=True)

        logger.info(f"Data ingestion started with bucket name : {self.bucket_name}, file name: {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        try:
            client=storage.Client()
            bucket=client.bucket(self.bucket_name)
            blob=bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error("Error donwloading csv file from google cloud bucket")
            raise CustomException("Failed to download csv file from google cloud bucket",e)

    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            data=pd.read_csv(RAW_FILE_PATH)
            train_data,test_data=train_test_split(data,test_size=self.train_ratio,random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error("Error while splitting the data")
            raise CustomException("Erorr while splitting the data",e)

    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion process completed successfully")
        except Exception as e:
            logger.error(f"Custom Exception : {str(e)}")
            raise CustomException("Erorr while splitting the data",e)

        finally:
            logger.info("Data ingestion completed")

if __name__=="__main__":
    data_ingestion_obj=DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion_obj.run()
