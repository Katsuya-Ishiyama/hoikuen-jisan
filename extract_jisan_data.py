from argparse import ArgumentParser
from datetime import datetime
from typing import Tuple, List
from word.data import JisanData
from sqlalchemy.orm import sessionmaker
from data.db import engine
from data.db.schema import Jisan


def get_args():
    parser = ArgumentParser()
    parser.add_argument("path", type=str, help="抽出するdocxファイルのパス")
    return parser.parse_args()


def convert_tuple_to_csv(tuple_: Tuple[str]) -> str:
    if tuple_ is None:
        return None
    return ", ".join(tuple_)


def extract_jisan_from_word(path: str) -> List[dict]:
    jisan_data = JisanData(path=path)
    _jisan_list = jisan_data.extract_jisan_from_tables()
    child_data = jisan_data.child
    entry_date = jisan_data.entry_date
    change_ts = datetime.now()

    jisan_list = []
    for j in _jisan_list:
        jisan_list.append({
            "date": j.date,
            "child_name": child_data.child_name,
            "class_name": child_data.class_name,
            "lunch": convert_tuple_to_csv(j.lunch),
            "snack": convert_tuple_to_csv(j.snack),
            "entry_date": entry_date,
            "change_ts": change_ts
        })
    return jisan_list


def insert_jisan(jisan_list: List[dict]):
    Session = sessionmaker(engine)
    session = Session()

    for jisan in jisan_list:
        session.add(Jisan(**jisan))

    session.commit()
    session.close()


if __name__ == "__main__":
    args = get_args()
    jisan_list = extract_jisan_from_word(args.path)
    insert_jisan(jisan_list)