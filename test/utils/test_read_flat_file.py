import pytest
import os

from src import utils


methods = utils.read_flat_file.ReadFile


class TestCheckPath(object):

    @pytest.fixture
    def create_file(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "hello.txt"
        p.write_text("content")
        yield p

    def test_create_file(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "hello.txt"
        p.write_text("content")
        assert p.read_text() == "content"
        assert len(list(tmp_path.iterdir())) == 1

    def test_on_path(self, create_file):
        p = create_file
        path_val = methods.check_path(p)
        assert path_val is True

    def test_on_wrong_path(self):
        path = "/some/wrong/path"
        path_value = methods.check_path(path)
        assert path_value is False

    def test_exception(self):
        pass


class TestGetDelimiter(object):

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

