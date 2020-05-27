# Author: Arpit Tandon
# Read utilities for files

import os
import logging
import pandas as pd
import csv

from src.utils.read_util import ReadUtils

LOGGER = logging.getLogger()


class ReadFile(ReadUtils):

    def check_path(self, path):
        if os.path.isfile(path):
            LOGGER.info("Reading file from %s" % path)
            return True
        else:
            LOGGER.error("File / path not present")
            return False

    # TODO: write the get delimiter function
    def get_delimiter(self, path):
        boolean = self.check_path(path)
        dialect = None
        if boolean:
            with open(path, newline='') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
            return dialect
        return "not a valid path"

    # TODO: modify to get the delimiter from the file and use it in this
    def read_file(self, path):
        boolean = self.check_path(path)
        df = None
        if boolean:
            df = pd.read_csv(path)
        return df
