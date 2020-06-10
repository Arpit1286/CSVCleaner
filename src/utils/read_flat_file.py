# Author: Arpit Tandon
# Read utilities for files

import os
import logging
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

