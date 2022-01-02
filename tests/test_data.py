from datetime import date
import pytest
from word import data
from dataclasses import dataclass
from typing import Tuple
from pathlib import Path


class TestExtractTargetMonth:

    @pytest.fixture(scope="function")
    def text(self):
        line = "令和 3 年度　 1 月　食事持参予定表"
        actual = (2021, 1)
        return line, actual

    def test_extract(self, text):
        line, actual = text
        expected = data.extract_target_month(line)
        assert expected, actual


class TestExtractEntryData:

    @pytest.fixture(scope="function")
    def text(self):
        line = "記入日　令和 3 年　12月 18日"
        actual = date(2021, 12, 18)
        return line, actual

    def test_extract(self, text):
        line, actual = text
        expected = data.extract_entry_date(line)
        assert expected == actual


class TestExtractChild:

    @pytest.fixture(scope="function")
    def text(self):
        line = "　　　　　れもん　　　　　　　クラス　園児氏名　山田　太郎"
        actual = data.Child("れもん", "山田　太郎")
        return line, actual

    def test_extract(self, text):
        line, actual = text
        expected = data.extract_child(line)
        assert expected == actual


@dataclass
class JisanFixture:
    path: Path
    child: data.Child
    entry_date: date
    target_month: Tuple[int, int]
    jisan: Tuple[data.Jisan, ...]


class TestJisanData:

    jisan_data = [
        JisanFixture(
            path=Path("../data/docx/食事持参予定表2021_test_01.docx"),
            child=data.Child("れもん", "山田　太郎"),
            entry_date=date(2021, 12, 28),
            target_month=(2022, 1),
            jisan=(
                data.Jisan(date(2022, 1, 4), ("豆乳シチュー",), None),
                data.Jisan(date(2022, 1, 5), ("焼き鮭",), ("アスパラガスビスケット",)),
                data.Jisan(date(2022, 1, 6), ("ハンバーグ",), None),
            )
        ),
        JisanFixture(
            path=Path("../data/docx/食事持参予定表2021_test_02.docx"),
            child=data.Child("いちご", "山田　花子"),
            entry_date=date(2021, 11, 27),
            target_month=(2021, 12),
            jisan=(
                data.Jisan(date(2021, 12, 12), ("オニオンスープ",), ("蒸しパン",)),
                data.Jisan(date(2021, 12, 13), ("豆乳スープ",), ("せんべい",)),
                data.Jisan(date(2021, 12, 14), None, ("蒸しパン",)),
                data.Jisan(date(2021, 12, 17), ("ミートソーススパゲティ",), None),
                data.Jisan(date(2021, 12, 18), None, ("豆乳ホットケーキ",)),
                data.Jisan(date(2021, 12, 19), ("ドライカレー",), ("いちごジャムサンド",)),
            )
        )
    ]

    @pytest.mark.parametrize("actual", jisan_data)
    def test_path(self, actual):
        jisan = data.JisanData(path=str(actual.path))
        assert jisan.path == actual.path

    @pytest.mark.parametrize("actual", jisan_data)
    def test_target_month(self, actual):
        jisan = data.JisanData(path=str(actual.path))
        assert jisan.target_month == actual.target_month

    @pytest.mark.parametrize("actual", jisan_data)
    def test_entry_date(self, actual):
        jisan = data.JisanData(path=str(actual.path))
        assert jisan.entry_date == actual.entry_date

    @pytest.mark.parametrize("actual", jisan_data)
    def test_child(self, actual):
        jisan = data.JisanData(path=str(actual.path))
        assert jisan.child == actual.child

    @pytest.mark.parametrize("actual", jisan_data)
    def test_extract_jisan_from_tables(self, actual):
        jisan = data.JisanData(path=str(actual.path))
        expected = jisan.extract_jisan_from_tables()
        assert expected == actual.jisan