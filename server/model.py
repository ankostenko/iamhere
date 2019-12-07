# _*_ coding = utf-8 _*_
# !/usr/bin/env python3.6

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from datetime import datetime, timedelta

Base = declarative_base()


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name, id=None):
        self.id = id
        self.name = name


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    file_type = Column(Integer, nullable=False)
    stage_id = Column(Integer, ForeignKey('stage.id'))
    created = Column(DateTime, default=datetime.now())
    length_in_days = Column(Integer, default=1)  # add days by default

    def __init__(self, name, x, y, file_type, stage_id, created, length_in_days, id=None):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.file_type = file_type
        self.stage_id = stage_id
        self.created = created
        self.length_in_days = length_in_days

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else \
            getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

class Stage(Base):
    __tablename__ = 'stage'

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('building.id'))
    name = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey('file.id'))
    tags = relationship('Tag', backref='stage', lazy=True)

    def __init__(self, building_id, name, image_id, id=None):
        self.id = id
        self.name = name
        self.image_id = image_id
        self.building_id = building_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else \
            getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}


class Building(Base):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    def __init__(self, name, description, id=None):
        self.id = id
        self.name = name
        self.description = description

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else \
            getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    date = Column(DateTime)
    browser = Column(String)
    os = Column(String)
    counter = Column(Integer)

    def __init__(self,  ip, date, browser, os, counter, id=None):
        self.id = id
        self.ip = ip
        self.date = date
        self.browser = browser
        self.os = os
        self.counter = counter


    def as_dict(self):
       return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else \
       getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

class SiteRequest(Base):
    __tablename__ = 'siterequest'

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    date = Column(DateTime)
    browser = Column(String)
    os = Column(String)
    url = Column(String)


    def __init__(self, ip, date, browser, os, url, id=None):
        self.id = id
        self.ip = ip
        self.date = date
        self.browser = browser
        self.os = os
        self.url = url

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else\
               getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

def run_model():
    engine = create_engine('sqlite:///iamhere.db')
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    engine = create_engine('sqlite:///iamhere.db')
    Base.metadata.create_all(engine)
