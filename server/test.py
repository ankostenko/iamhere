# _*_ coding = utf-8 _*_

from model import Building, Stage, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///%s' % 'iamhere.db?charset=utf8', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Добавим здание
name = "ГО"
description= "ул. Угличская, 36"
building = Building(name, description)
session.add(building)
session.commit()

# Добавим этаж
stage = Stage(building_id = 1, name = "1", image_id="1")
session.add(stage)
session.commit()
for stage in session.query(Stage).filter_by(building_id=1).all():
    print(stage.as_dict())

