import pytest
import yaml

from utils import utils


class TestConvertReiwaToYear:

    @pytest.fixture(scope="function")
    def data_fixture(self):
        return ((1, 2019), (2, 2020), (3, 2021))

    def test_convert(self, data_fixture):
        for reiwa, actual in data_fixture:
            assert utils.convert_reiwa_to_year(reiwa) == actual


class TestLoadSettings:

    @pytest.fixture(scope="function")
    def yml_data(self, tmp_path):
        _path = tmp_path / "settings_test.yml"
        _expected = {"line": {"token": "test"}}
        with _path.open(mode="w") as f:
            yaml.safe_dump(_expected, f)
        return _path, _expected

    def test_load_settings(self, yml_data):
        path, expected = yml_data
        actual = utils.load_settings(str(path))
        assert actual == expected