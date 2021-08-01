from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings
from datetime import datetime

Base = declarative_base()


def dbConnect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def createTable(engine):
    Base.metadata.create_all(engine)


class Alokasi(Base):
    __tablename__ = "tbAlokasi"

    id = Column(Integer, primary_key=True)
    program = Column('program', Text())
    nopend = Column('nopend', Text())
    kprk = Column('kprk', Text())
    alokasi = Column('alokasi', Text())
    tanggalReport = Column('tanggalReport', DateTime, default=datetime.utcnow)


class Realisasi(Base):
    __tablename__ = "tbRealisasi"

    id = Column(Integer, primary_key=True)
    program = Column('program', Text())
    nopend = Column('nopend', Text())
    kprk = Column('kprk', Text())
    tanggal = Column('tanggal', DateTime)
    realisasi = Column('realisasi', Integer)
    nominal = Column('nominal', Integer)
    tanggalReport = Column('tanggalReport', DateTime, default=datetime.utcnow)
