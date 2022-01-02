from sqlalchemy import create_engine

engine = create_engine("mysql://root:root@127.0.0.1:3306/testdb?charset=utf8")
