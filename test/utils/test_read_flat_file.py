import pytest
import os

from src import utils


methods = utils.read_flat_file.ReadFile


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
    def csv_file(self, tmpdir):
        csv_file = tmpdir.mkdir("sub").join("zillow.csv")
        content = """"Index", "Living Space (sq ft)", "Beds", "Baths", "Zip", "Year", "List Price ($)"
        1, 2222, 3, 3.5, 32312, 1981, 250000
        2, 1628, 3, 2,   32308, 2009, 185000
        3, 3824, 5, 4,   32312, 1954, 399000
        4, 1137, 3, 2,   32309, 1993, 150000
        5, 3560, 6, 4,   32309, 1973, 315000"""
        csv_file.write(content)
        yield csv_file

    def test_on_comma_delimiter(self):
        pass

    def test_on_tab_delimiter(self):
        pass

    def test_on_colon_delimiter(self):
        pass

    def test_on_mixed_delimiter(self):
        pass

    def test_exception(self):
        pass


class TestReadFile(object):

    def test_on_regular_csv(self):
        pass

    def test_on_malformed_csv(self):
        pass

    def test_on_wrong_path(self):
        pass

    def test_on_delimiter(self):
        pass

