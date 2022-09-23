"""
    DBのテーブル定義

    このモジュールを実行するとテーブル作成する。
    SowStatusとSowClassのテーブル作ってみたけど今の所使い途ない

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sow_setting import Base, ENGINE

class SowMembers(Base):

    __tablename__ = 'sow_members'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    screen_name = Column(String, unique=True)
    join_date = Column(Integer)
    status_id = Column(Integer, ForeignKey('sow_status.id'))
    class_id = Column(Integer, ForeignKey('sow_class.id'))
    summon_num = Column(Integer)
    response_num = Column(Integer)

class SowStatus(Base):
    __tablename__ = 'sow_status'

    id = Column(Integer, primary_key=True)
    sow_status = Column(String)
    members = relationship('SowMembers')

class SowClass(Base):
    __tablename__ = 'sow_class'

    id = Column(Integer, primary_key=True)
    sow_class = Column(String)
    members = relationship('SowMembers')


def main():
    """
    メイン関数
    このファイルを実行すると、DB作成する
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main()