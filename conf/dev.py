import pymysql
from app.dirty_secrets import db_host, db_user, db_pass, db_name

conn = "mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8mb4".format(db_user, db_pass, db_host, db_name)

SQLALCHEMY_DATABASE_URI = conn
SQLALCHEMY_TRACK_MODIFICATIONS = False