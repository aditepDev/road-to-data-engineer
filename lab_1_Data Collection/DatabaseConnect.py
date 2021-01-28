from Config import Config
import pymysql.cursors


def connect():
    connection = pymysql.connect(host=Config.MYSQL_HOST,
                                 port=Config.MYSQL_PORT,
                                 user=Config.MYSQL_USER,
                                 password=Config.MYSQL_PASSWORD,
                                 db=Config.MYSQL_DB,
                                 charset=Config.MYSQL_CHARSET,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
