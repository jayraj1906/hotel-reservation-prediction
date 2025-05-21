import os
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
import pandas as pd

logger=get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the given path")
        with open(file_path,"r") as yaml_file:
            config=yaml.safe_load(yaml_file)
            logger.info("Successfull read yaml file")
            return config
    except Exception as e:
        logger.error("Error reading yaml file")
        CustomException("Failed to read yaml file",e)

def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading data in path {path}")
        raise CustomException(f"Error loading the data from path {path}",e)

