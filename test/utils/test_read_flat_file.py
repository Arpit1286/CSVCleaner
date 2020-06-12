import pytest
import os
import pandas as pd

from src import utils

methods = utils.read_flat_file.ReadFile()


@pytest.fixture
def get_df():
    zil = {'Index': [1, 2, 3, 4, 5],
           'Living Space (sq ft)': [2222, 1628, 3824, 1137, 3560],
           'Beds': [3, 3, 5, 3, 6],
           'Baths': [3.5, 2, 4, 2, 4],
           'Zip': [32312, 32308, 32312, 32309, 32309],
           'Year': [1981, 2009, 1954, 1993, 1973],
           'List Price ($)': [250000, 185000, 399000, 150000, 315000]
           }
    df = pd.DataFrame(data=zil)
    yield df


class TestCheckPath(object):

    @pytest.fixture
    def create_path(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "hello.txt"
        p.write_text("content")
        yield p
        os.remove(p)

    def test_create_file(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "hello.txt"
        p.write_text("content")
        assert p.read_text() == "content"
        assert len(list(tmp_path.iterdir())) == 1

    def test_on_path(self, create_path):
        p = create_path
        path_val = methods.check_path(p)
        assert path_val is True

    def test_on_wrong_path(self):
        path = "/some/wrong/path"
        path_value = methods.check_path(path)
        assert path_value is False


class TestGetDelimiter(object):

    @pytest.fixture
    def csv_file(self, tmp_path):
        file_name = "zillow.csv"
        d = tmp_path / "sub"
        d.mkdir()
        path = d / file_name
        content = """"Index", "Living Space (sq ft)", "Beds", "Baths", "Zip", "Year", "List Price ($)\n"
        1, 2222, 3, 3.5, 32312, 1981, 250000\n
        2, 1628, 3, 2,   32308, 2009, 185000\n
        3, 3824, 5, 4,   32312, 1954, 399000\n
        4, 1137, 3, 2,   32309, 1993, 150000\n
        5, 3560, 6, 4,   32309, 1973, 315000"""
        path.write_text(content)
        yield path

    @pytest.fixture
    def tsv_file(self, tmp_path):
        file_name = "zillow.csv"
        d = tmp_path / "sub"
        d.mkdir()
        path = d / file_name
        content = """"Index"\t"Living Space (sq ft)"\t"Beds"\t"Baths"\t"Zip"\t"Year"\t"List Price ($)\n"
         1\t2222\t3\t3.5\t32312\t1981 250000\n
         2\t1628\t3\t2\t32308\t2009\t185000\n
         3\t3824\t5\t4\t32312\t1954\t399000\n
         4\t1137\t3\t2\t32309\t1993\t150000\n
         5\t3560\t6\t4\t32309\t1973\t315000"""
        path.write_text(content)
        yield path

    @pytest.fixture
    def colon_file(self, tmp_path):
        file_name = "zillow.csv"
        d = tmp_path / "sub"
        d.mkdir()
        path = d / file_name
        content = """"Index": "Living Space (sq ft)": "Beds": "Baths": "Zip": "Year": "List Price ($)\n"
        1: 2222: 3: 3.5: 32312: 1981: 250000\n
        2: 1628: 3: 2:   32308: 2009: 185000\n
        3: 3824: 5: 4:   32312: 1954: 399000\n
        4: 1137: 3: 2:   32309: 1993: 150000\n
        5: 3560: 6: 4:   32309: 1973: 315000"""
        path.write_text(content)
        yield path

    @pytest.fixture
    def malformed_file(self, tmp_path):
        file_name = "zillow.csv"
        d = tmp_path / "sub"
        d.mkdir()
        path = d / file_name
        content = """"Index";"Living Space (sq ft)" "Beds";"Baths" "Zip" "Year" "List Price ($)\n"
        1: 2222: 3: 3.5: 32312: 250000\n
        2: 1628: 3: 2:   32308; 2009: 185000\n
        3: 3824: 5: 4:   32312: 1954: 399000\n
        4: 1137: 3; 2:   32309; 1993: 150000\n
        5: 3560: 6: 4:   32309: 1973: 315000"""
        path.write_text(content)
        yield path

    def test_on_comma_delimiter(self, csv_file):
        expected = ","
        path = csv_file
        actual = methods.get_delimiter(path)
        message = "comma delimiter should return ',' but returns {0}".format(actual)
        assert actual is expected, message

    def test_on_tab_delimiter(self, tsv_file):
        expected = "\t"
        path = tsv_file
        actual = methods.get_delimiter(path)
        message = "tab delimiter should return ',' but returns {0}".format(actual)
        assert actual is expected, message

    def test_on_colon_delimiter(self, colon_file):
        expected = ":"
        path = colon_file
        actual = methods.get_delimiter(path)
        message = "colon delimiter should return ',' but returns {0}".format(actual)
        assert actual is expected, message

    @pytest.mark.skip("dialect returns a value, implement later")
    def test_exception(self, malformed_file):
        expected = None
        path = malformed_file
        actual = methods.get_delimiter(path)
        message = "value should return None but returns {0}".format(actual)
        assert actual is expected, message


class TestReadFile(object):

    @pytest.fixture
    def csv_file(self, tmp_path):
        file_name = "zillow.csv"
        d = tmp_path / "sub"
        d.mkdir()
        path = d / file_name
        content = """Index,Living Space (sq ft),Beds,Baths,Zip,Year,List Price ($)
        1,2222,3,3.5,32312,1981,250000
        2,1628,3,2,32308,2009,185000
        3,3824,5,4,32312,1954,399000
        4,1137,3,2,32309,1993,150000
        5,3560,6,4,32309,1973,315000"""
        path.write_text(content)
        yield path

    def test_on_regular_csv(self, csv_file, get_df):
        expected_df = get_df
        path = csv_file
        actual_df = methods.read_file(path)
        pd.testing.assert_frame_equal(expected_df, actual_df)

    def test_regular_schema_columns(self, csv_file, get_df):
        expected = get_df
        actual = methods.read_file(csv_file)
        expected_columns = list(expected.columns.values)
        actual_columns = list(actual.columns.values)
        message = "value should return \n{0} \nbut returns \n{1}".format(actual_columns, expected_columns)
        assert expected_columns == actual_columns, message

    def test_regular_schema_dtypes(self, csv_file, get_df):
        expected = get_df
        actual = methods.read_file(csv_file)
        expected_dtypes = list(expected.dtypes) # list to compare
        actual_dtypes = list(actual.dtypes)
        message = "value should return \n{0} \nbut returns \n{1}".format(actual_dtypes, expected_dtypes)
        assert expected_dtypes == actual_dtypes, message

    def test_on_wrong_path(self):
        expected = None
        path = "/some/wrong/path"
        actual = methods.read_file(path)
        assert expected == actual


class TestGetDFHeader(object):

    # regular scenario
    def test_get_df_header(self, get_df):
        expected_tuple = ('Beds', 2)
        expected_header = [('Index', 0), ('Living Space (sq ft)', 1), ('Beds', 2),
                           ('Baths', 3), ('Zip', 4), ('Year', 5), ('List Price ($)', 6)]
        actual_header = methods.get_df_header(get_df)
        actual_tuple = actual_header[2]
        assert expected_header == actual_header
        assert expected_tuple == actual_tuple


class TestGetDFSchema(object):

    # regular scenario
    def test_get_df_schema(self, get_df):
        expected_dict = {'Index': 'int64', 'Living Space (sq ft)': 'int64', 'Beds': 'int64',
                         'Baths': 'float64', 'Zip': 'int64', 'Year': 'int64', 'List Price ($)': 'int64'}
        expected_value = 'float64'
        actual_dict = methods.get_df_schema(get_df)
        actual_value = actual_dict['Baths']
        assert expected_dict == actual_dict
        assert expected_value == actual_value

