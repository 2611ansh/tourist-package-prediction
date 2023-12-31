import sys
from typing import Tuple

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from tourism.configuration.mongo_operations import MongoDBOperation
from tourism.constant import TRAIN_TEST_SPLIT_SIZE, RANDOM_STATE
from tourism.entity.config_entity import DatabaseConfig
from tourism.exception import TourismException
from tourism.logger import logging
from tourism.utils.main_utils import MainUtils


class DataIngestion:
    def __init__(self):
        self.utils = MainUtils()

        self.mongo_op = MongoDBOperation()

        self.mongo_config = DatabaseConfig()

    @staticmethod
    def split_data_as_train_test(df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio

        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(
                df, test_size=TRAIN_TEST_SPLIT_SIZE, random_state=RANDOM_STATE
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:
            raise TourismException(e, sys) from e

    def get_data_from_mongodb(self) -> DataFrame:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio

        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered get_data_from_mongodb method of Data_Ingestion class")

        try:
            logging.info("Getting the dataframe from mongodb")

            df = self.mongo_op.get_collection_as_dataframe(
                self.mongo_config.DATABASE_NAME, self.mongo_config.COLLECTION_NAME
            )

            logging.info("Got the dataframe from mongodb")

            logging.info(
                "Exited the get_data_from_mongodb method of Data_Ingestion class"
            )

            return df

        except Exception as e:
            raise TourismException(e, sys) from e

    def initiate_data_ingestion(self) -> Tuple[DataFrame, DataFrame]:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline

        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            df = self.get_data_from_mongodb()

            schema_config = self.utils.read_schema_config_file()

            drop_columns = schema_config["Drop_columns"]

            df = df.drop(drop_columns, axis=1)

            logging.info("Got the data from mongodb")

            train_set, test_set = self.split_data_as_train_test(df)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:
            raise TourismException(e, sys) from e
