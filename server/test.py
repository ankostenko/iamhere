# _*_ coding = utf-8 _*_
import os
import uuid
from shutil import copyfile
from model import Building, Stage, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.model import File

engine = create_engine('sqlite:///%s' % 'iamhere.db?charset=utf8', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def create_file(src):
    dst = str(uuid.uuid4()) + '.' + src.split('.')[-1]
    copyfile(src, os.path.join('files', dst))
    file = File(dst)
    session.add(file)
    session.commit()
    return file.id


def create_building(name, descr):
    building = Building(name, descr)
    session.add(building)
    session.commit()


def create_stage(b_id, name, i_id):
    stage = Stage(building_id=b_id, name=name, image_id=i_id)
    session.add(stage)
    session.commit()


def delete_data():
    for i in os.listdir("files"):
        os.remove(f"files/{i}")
    for i in range(1, session.query(Stage).count() + 1):
        session.query(Stage).filter_by(id=i).delete()
    for i in range(1, session.query(Building).count() + 1):
        session.query(Building).filter_by(name="Тензор").delete()
    for i in range(1, session.query(File).count() + 1):
        session.query(File).filter_by(id=i).delete()


def run_test():
    delete_data()
    create_building("Тензор", "Углическая 36")
    for i in range(1, 8):
        create_stage(1, str(i), create_file(f"static/images/floor_{i}.png"))


if __name__ == '__main__':
    run_test()
