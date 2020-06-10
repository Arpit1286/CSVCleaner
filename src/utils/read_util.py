# Author: Arpit Tandon
# Read Utilities base class


class ReadUtils:

    def check_path(self):
        """
        check if the path entered is correct
        :return:
        """
        pass

    def get_delimiter(self):
        """
        return the delimiter for the file
        :return:
        """

    def read_file(self):
        """
        read the file into a dataframe
        :return:
        """
        pass

    def get_df_header(self):
        """
        get the header from the dataframe
        :return:
        """
        pass

    def get_df_schema(self):
        """"
        get the column schema from the dataframe
        :return:
        """
        pass

    def get_column_type(self):
        """
        get the inferred column type from dataframe
        :return:
        """
        pass

    def get_column_number(self):
        """
        get the column position for iloc operations
        :return:
        """
        pass

    def get_column_values_list(self):
        """
        get the columns values as list
        :return:
        """
        pass

    def get_column_values_series(self):
        """
        get the column values as np series
        :return:
        """
        pass
