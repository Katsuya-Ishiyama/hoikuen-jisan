from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date, DateTime

from data.db import engine

Base = declarative_base()


class Jisan(Base):
    __tablename__ = "jisan"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    child_name = Column(String(50))
    class_name = Column(String(50))
    lunch = Column(String(255))
    snack = Column(String(255))
    entry_date = Column(Date)
    change_ts = Column(DateTime)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
