import pymysql
import pymysql.cursors

from config.config import DB

def get_connection():
    return pymysql.connect(
        host=DB["host"],
        port=DB.get("port", 3306),
        user=DB["user"],
        password=DB["password"],
        database=DB["database"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
