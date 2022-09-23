"""
	DB設定等を詰め込んだモジュールです。

"""
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

"""
# mysqlのDBの設定
DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    "user_name",
    "password",
    "host_ip",
    "db_name",
)
"""
#sqlite設定
DATABASE = 'sqlite:///data.sqlite'

ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
session = scoped_session(
  # ORM実行時の設定。
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()

#関数戻り値定義
RESULT_SUCCESS = 0         #成功
RESULT_ERROR = 1           #失敗

JOIN_SOW_RESULT_UPDATE = 2          #ScreenName更新
JOIN_SOW_RESULT_ALREADY = 3         #入隊済

