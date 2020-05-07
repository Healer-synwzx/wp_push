import os
import logging

APP_ID = os.getenv("wp_app_id")
APP_SECRET = os.getenv("wp_app_secret")

PUSH_TEMPLATE_ID = os.getenv("push_template_id")
QR_SCENE = '123'
QR_EXP = 1800

REDIS_HOST = os.getenv("redis_host", "127.0.0.1")
REDIS_PORT = os.getenv("redis_port", 6379)
REDIS_PASSWORD = os.getenv("redis_password", "123456")
REDIS_DB = 5

MYSQL_HOST = os.getenv("mysql_host", "127.0.0.1")
MYSQL_PORT = os.getenv("mysql_port", 3306)
MYSQL_USER = os.getenv("mysql_user", "root")
MYSQL_PASSWD = os.getenv("mysql_passwd", "123456")
MYSQL_DB = os.getenv("mysql_db", "zhihuhaowu")

SQLALCHEMY_DATABASE_URI = \
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4'


logger = logging.getLogger('pusher')