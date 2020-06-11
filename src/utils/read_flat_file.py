# Author: Arpit Tandon
# Read utilities for files

import os
import logging
from typing import List, Any, Tuple

import pandas as pd
import csv

from src.utils.read_util import ReadUtils

LOGGER = logging.getLogger()


class ReadFile(ReadUtils):

    @staticmethod
    def check_path(path: str) -> bool:
        """
        check if the path exists, if not gracefully exit
        :param path: input file path
        :return:
        """
        if os.path.isfile(path):
            LOGGER.info("Reading file from %s" % path)
            return True
        else:
            LOGGER.error("File / path not present")
            return False

    # using csv Sniffer to get delimiter
    def get_delimiter(self, path: str):
        """
        infer the delimiter using the csv sniffer
        :param path:
        :return:
        """
        boolean = self.check_path(path)
        if boolean:
            try:
                with open(path, newline='') as csv_file:
                    dialect = csv.Sniffer().sniff(csv_file.read(1024))
                return dialect.delimiter
            except csv.Error as e:
                LOGGER.error(e)
        return None

    def read_file(self, path, strip=False):
        """
        read csv file as pandas dataframe
        :type strip: bool
        :param strip: Default False, if true strip the str values of leading/trailing characters
        :param path: path to the file
        :return: dataframe from the file
        """
        boolean = self.check_path(path)
        df = None
        if boolean:
            if strip:
                delimiter = self.get_delimiter(path)
                df = pd.read_csv(path, delimiter=delimiter)
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            else:
                delimiter = self.get_delimiter(path)
                df = pd.read_csv(path, delimiter=delimiter)
        LOGGER.error("DataFrame could not be created, file path non-existent")
        return df

    #Wrapper functions for dataframe methods.
    def get_df_header(self, df: pd.DataFrame):
        """
        get the header (column names) and column numbers
        :type df: pd.DataFrame
        :param df: input dataframe
        :return: list of tuples with column name and location
        """
        header: List[Tuple[Any, Any]] = []
        for i in df.columns.values:
            col_name_index = (i, df.columns.get_loc(i))
            header.append(col_name_index)
        return header

    def get_df_schema(self, df: pd.DataFrame):
        """
        get the schema (column name and type)
        :type df: pd.DataFrame
        :param df: input DataFrame
        :return: dict key: column name,  value: col_type
        """
        col_dict = dict(df.dtypes)
        return col_dict

    def get_column_type_from_df(self, column_name, df: pd.DataFrame):
        """
        get the data type for a given column
        :param column_name: name of column
        :param df: DataFrame
        :type df: pd.DataFrame
        :return: datatype string
        """
        type_obj = None
        if column_name in df.columns:
            type_obj = str(df.dtypes[column_name])
        else:
            LOGGER.error("Column not in dataframe, check the column list")
        return type_obj

    def get_column_number(self, column_name, df: pd.DataFrame):
        """
        get the data type column number from DataFrame
        :param column_name: col name
        :type df: pd.DataFrame
        :param df: input DataFrame
        :return: col location
        """
        col_num = None
        if column_name in df.columns:
            col_num = df.columns.get_loc(column_name)
        else:
            LOGGER.error("Column not in dataframe, check the column list")
        return col_num

    def get_column_values_list(self, column_name, df: pd.DataFrame):
        """
        get the column values as a list
        :type df: pd.DataFrame
        :param df: input DataFrame
        :param column_name: column name
        :return:
        """
        val_list = []
        if column_name in df.columns:
            val_list = df[column_name].tolist()
        else:
            LOGGER.error("Column not in DataFrame, check the column list")
        return val_list

    def get_column_values_series(self, column_name, df: pd.DataFrame):
        """
        get the column values as numpy Array
        :type df: pd.DataFrame
        :param df: input DataFrame
        :param column_name: column name
        :return:
        """
        val_array = None
        if column_name in df.columns:
            val_array = df[column_name].to_numpy()
        else:
            LOGGER.error("Column not in dataframe, check the column list")
        return val_array
