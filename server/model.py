# _*_ coding = utf-8 _*_
#!/usr/bin/env python3.6

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

class Stage(Base):
    __tablename__ = 'stage'

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('building.id'))
    name = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey('file.id'))

    def __init__(self, building_id, name, image_id, id=None):
        self.id = id
        self.name = name
        self.image_id = image_id
        self.building_id = building_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else\
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
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else\
               getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

if __name__ == '__main__':
    engine = create_engine('sqlite:///iamhere.db')
    Base.metadata.create_all(engine)
