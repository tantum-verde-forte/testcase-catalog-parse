from sqlalchemy import create_engine, Column, Table, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings
from datetime import datetime


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class PriceItem(DeclarativeBase):
    __tablename__ = 'spider_items'

    id = Column(Integer, primary_key=True)
    good_name = Column(String(127))
    price = Column(Float)
    price_old = Column(Float)
    img_url = Column(String(127))
    url = Column(String(127))
    unit_raw = Column(String(127))
    item_id = Column(String(127))
    category = Column(String(127))
    region = Column(String(127))
    retailer_name = Column(String(127))
    last_time = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)