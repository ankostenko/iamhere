# _*_ coding = utf-8 _*_
from datetime import datetime, timedelta

from flask import Flask, request, render_template, make_response, send_from_directory, send_file
from flask_restplus import Resource, Api, fields
from model import Building, Stage, File, Base, Tag, run_model
from flask.logging import default_handler
from model import Building, Stage, File, Base, Stats, SiteRequest
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.datastructures import FileStorage
import uuid
from flask_restplus import reqparse
import os
import sys
import server
from test import run_test
from datetime import datetime
from server.routes.way_finder import WayFinder


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config['JSON_AS_ASCII'] = False
api = Api(app, doc='/api/v1', prefix="/api/v1")
api = api.namespace('', description='Сервис картографии для помещений')
upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)
engine = create_engine('sqlite:///%s' % 'iamhere.db?charset=utf8', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@api.route('/building/<int:id>')
class BuildingAPI(Resource):
    def get(self, id):
        return make_response(session.query(Building).filter_by(id=id).first().as_dict())

    def delete(self, id):
        session.query(Building).filter_by(id=id).delete()
        session.commit()
        return 'OK'


@api.route('/buildings')
class BuildingsApi(Resource):
    building = api.model('Building', {
        'name': fields.String,
        'description': fields.String,
    })

    def get(self):
        result = []
        for building in session.query(Building).all():
            result.append(building.as_dict())
        return make_response(str(result))

    @api.expect(building)
    def post(self):
        building = Building(**request.json)
        session.add(building)
        session.commit()
        return building.id

@api.route('/stages/<int:id>')
class StagesAPI(Resource):
    stage = api.model('Stage', {
        'name': fields.String,
        'building_id': fields.Integer,
        'image_id': fields.Integer,
    })

    def get(self, id):
        result = []
        for stage in session.query(Stage).filter_by(building_id=id).all():
            result.append(stage.as_dict())
        return make_response(str(result))

    @api.expect(stage)
    def post(self, id):
        stage = Stage(**request.json)
        session.add(stage)
        session.commit()
        return stage.id

@api.route('/stage/<int:id>')
class StagesAPI(Resource):

    def get(self, id):
        return make_response(session.query(Stage).filter_by(id=id).first().as_dict())

    def delete(self, id):
        session.query(Stage).filter_by(id=id).delete()
        session.commit()
        return 'OK'


@api.route('/upload/')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        args = parser.parse_args()
        uploaded_file = request.files['file']
        filename = str(uuid.uuid4()) + '.' + uploaded_file.filename.split('.')[-1]
        print(uploaded_file.filename)
        uploaded_file.save(os.path.join('files', filename))
        file = File(filename)
        session.add(file)
        session.commit()
        return file.id, 201
        
@api.route('/image/<int:id>')
class ImagesAPI(Resource):

    def get(self, id):
        return session.query(File).filter_by(id=id).first().name


@app.route('/test')
def test():
    return "Тест!"

@app.route('/')
@app.route('/index')
def index():
    buildings = session.query(Building);
    building = buildings.first();
    building_id = building.id;
    building = building.as_dict();
    building_stages = []
    buildingsData = []
    for building_item in buildings:
        buildingsData.append(building_item.as_dict())
    for stage in session.query(Stage).filter_by(building_id=building_id).all():
        building_stages.append(stage.as_dict())
    return render_template('index.html', building=building, stages=building_stages, buildings=buildingsData)


@api.route('/tag/<int:id>')
class TagAPI(Resource):
    def get(self, id):
        return make_response(session.query(Tag).filter_by(id=id).first().as_dict())

    def delete(self, id):
        session.query(Tag).filter_by(id=id).delete()
        session.commit()
        return 'OK'

@api.route('/tags/')
class TagsAPI(Resource):
    tag = api.model('Tag', {
        'name': fields.String,
        'x': fields.Integer,
        'y': fields.Integer,
        'file_type': fields.Integer,
        'stage_id': fields.Integer,
        'created': fields.DateTime,
        'length_in_days': fields.Integer,
    })


    @api.expect(tag)
    def post(self):
        created = datetime.strptime(request.json['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        request.json['created'] = created
        tag = Tag(**request.json)
        session.add(tag)
        session.commit()
        return tag.id

@api.route('/tags/<int:id>')
class TagsAPI(Resource):
    tag = api.model('Tag', {
        "name": fields.String,
        "x": fields.Integer,
        "y": fields.Integer,
        "file_type": fields.Integer,
        "stage_id": fields.Integer,
        "created": fields.DateTime,
        "length_in_days": fields.Integer,
    })

    def get(self, id):
        result = []
        for tag in session.query(Tag).filter_by(stage_id=id).all():
            # if (datetime.now() < tag.created + timedelta(days=tag.length_in_days)):
            #     result.append(tag.as_dict())
            # else:
            #     session.delete(tag)
            result.append(tag.as_dict())
                # tags_for_del = session.query(Tag).filter(
                #     (datetime.now().timestamp() - Tag.created.timestamp()).day < Tag.length_in_days)
        # tags_for_del = session.query(Tag).filter((datetime.now().timestamp() - Tag.created.timestamp()).day < Tag.length_in_days)
        # tags_for_del.delete()
        session.commit()

        # d = addresses_table.delete().where(addresses_table.c.retired == 1)
        # d.execute()
        return make_response(str(result))


@api.route('/way/<int:id>')
class WayFinderApi(Resource):
    way = api.model('way', {
        'start_row': fields.Integer,
        'start_col': fields.Integer,
        'end_row': fields.Integer,
        'end_col': fields.Integer,
    })
    @api.expect(way)
    def post(self, id):
        filename = session.query(File).filter_by(id=id).first().name

        finder = WayFinder(os.path.join('server', 'files', filename))
        #finder = WayFinder('C:\\Users\\ДНС\\PycharmProjects\\iamhere-dev\\example\\floor_2.png')

        return finder.find_way(**request.json)


@app.route('/admin/<int:buildingId>')
def admin(buildingId):
    buildingStages = []
    building = session.query(Building).filter_by(id=buildingId).first().as_dict()
    for stage in session.query(Stage).filter_by(building_id=buildingId).all():
        buildingStages.append(stage.as_dict())
    return render_template('buildingManager.html', buildingStages=buildingStages, building=building)

@app.route('/admin/<int:building_id>/<int:stage_id>')
def admin_edit_floor(building_id, stage_id):
    stage = session.query(Stage).filter_by(building_id=building_id, id=stage_id).first().as_dict()
    return render_template('floorAddition.html', stage=stage, buildingId=building_id)

@app.route('/admin/<int:building_id>/add')
def admin_add_floor(building_id):
    is_edit = True
    return render_template('floorAddition.html', buildingId=building_id, isEdit=is_edit, stage=None)

@app.route('/building/<int:id>/')
def building_get(id):
    buildings = session.query(Building);
    building = session.query(Building).filter_by(id=id).first().as_dict()
    building_stages = []
    buildingsData = []
    for building_item in buildings:
        buildingsData.append(building_item.as_dict())

    for stage in session.query(Stage).filter_by(building_id=id).all():
        building_stages.append(stage.as_dict())
    return render_template('index.html', building=building, stages=building_stages, buildings=buildingsData)

@app.route('/building-adder')
def building_add():
    return render_template('buildingAddition.html')


@app.route('/statistics')
def statistics():
    # ip = request.remote_addr
    # count_of_unique = session.query(func.count(Stats.id)).scalar()
    # count_of_current = session.query(Stats).filter_by(ip=ip).first().counter
    # return render_template('statistics.html', count_of_unique=count_of_unique, count_of_current=count_of_current)
    siterequestData = []
    for another_request in session.query(SiteRequest).all():
        siterequestData.append((another_request.as_dict()))
    return render_template('statistics.html',another_request=siterequestData)


@app.route('/buildings')
def buildings():
    buildingsData = []
    for building in session.query(Building).all():
        buildingsData.append(building.as_dict())
    return render_template('buildingListing.html', buildings=buildingsData)

@app.route('/static/js/<filename>')
def js(filename):
    return send_from_directory('static/js', filename)

@app.route('/static/css/<filename>')
def css(filename):
    return send_from_directory('static/css', filename)
    
@app.route('/static/images/<filename>')
def images(filename):
    return send_from_directory('static/images', filename)
    
@app.route('/files/<filename>')
def files(filename):
    print('HMMMM!')
    return send_from_directory('files', filename)


#@app.before_request
def before_request():
    print("request called")
    print(request.remote_addr, '- -', datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          '- -', request.user_agent.browser, '- -', request.user_agent.platform, '- -', request.url)

    stats = api.model('Stats', {
        'ip': fields.String,
        'date': fields.String,
        'browser': fields.String,
        'os': fields.String,
    })

    siterequest = api.model('SiteRequest',{
        'ip': fields.String,
        'date': fields.String,
        'browser': fields.String,
        'os': fields.String,
        'url':fields.String,
    })

    # def get(self):
    #     result = []
    #     for stats in session.query(Stats).all():
    #         result.append(stats.as_dict())
    #     return make_response(str(result))

    # request.json['ip'] = request.remote_addr
    # request.json['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # request.json['browser'] = request.user_agent.browser
    # request.json['os'] = request.user_agent.platform
    # "%Y-%m-%d %H:%M:%S"pyth
    ip = request.remote_addr
    # stats = Stats(ip,
    #               datetime.strptime(str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')), '%Y-%m-%dT%H:%M:%S.%fZ'),
    #               request.user_agent.browser, request.user_agent.platform, 0)
    # row = session.query(Stats).filter_by(ip=ip).first()
    siterequest = SiteRequest(ip,datetime.strptime(str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')), '%Y-%m-%dT%H:%M:%S.%fZ'),
                  request.user_agent.browser, request.user_agent.platform,request.url)

    session.add(siterequest)
    session.commit()
    # if (row is None):
    #     session.add(stats)
    # else:
    #     row.counter += 1
    # session.commit()

def runme():
    if (len(sys.argv) > 1 and sys.argv[1] == "fill"):
        run_model()
        run_test()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')

if __name__ == '__main__':
    runme()