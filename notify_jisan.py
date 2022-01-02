from datetime import datetime, timedelta
from argparse import ArgumentParser
from sqlalchemy.orm import sessionmaker
from data.db import engine
from data.db.schema import Jisan
from line.notify import LineNotifier

DAILY_MESSAGE_FORMAT = """\
お昼: {lunch}
おやつ: {snack}
"""

WEEKLY_MESSAGE_FORMAT = """\
日付: {date}
お昼: {lunch}
おやつ: {snack}
"""


def get_args():
    parser = ArgumentParser()
    parser.add_argument("notify_type",
                        type=str,
                        choices=["daily", "weekly"],
                        help="通知のタイプ (daily or weekly)")
    return parser.parse_args()


def create_daily_message() -> str:
    target_date = (datetime.now() + timedelta(days=1)).date()

    Session = sessionmaker(engine)
    session = Session()

    jisan_list = session.query(Jisan).where(Jisan.date == target_date).all()
    if not jisan_list:
        exit(0)

    jisan = jisan_list[0]

    jisan_message = DAILY_MESSAGE_FORMAT.format(
        lunch=jisan.lunch,
        snack=jisan.snack if jisan.snack is not None else "なし"
    )
    message = (
            "\n"
            f"{jisan.child_name}の{jisan.date}の持参\n"
            "-----\n"
    )
    message += jisan_message
    return message


def create_weekly_message():
    start_date = (datetime.now() + timedelta(days=1)).date()
    end_date = start_date + timedelta(days=7)

    Session = sessionmaker(engine)
    session = Session()

    jisan_list = session.query(Jisan) \
                        .where(Jisan.date.between(start_date, end_date)) \
                        .order_by(Jisan.date) \
                        .all()

    if not jisan_list:
        exit(0)

    message = (
        "\n"
        f"{jisan_list[0].child_name}の1週間の持参予定\n"
    )

    for jisan in jisan_list:
        jisan_message = WEEKLY_MESSAGE_FORMAT.format(
            date=jisan.date,
            lunch=jisan.lunch,
            snack=jisan.snack if jisan.snack is not None else "なし"
        )
        message += ("-----\n" + jisan_message)
    return message


if __name__ == "__main__":
    args = get_args()

    if args.notify_type == "daily":
        message = create_daily_message()
    elif args.notify_type == "weekly":
        message = create_weekly_message()

    notifier = LineNotifier(test=True)
    #notifier = LineNotifier()
    notifier.send(message)
