from app_config import db
from flask import request, jsonify, Blueprint
from database.models import VideoList
from database.schemas import VideoListSchema
import logger
log = logger.create_logger(__name__)
video_schema = VideoListSchema()
videos_schema = VideoListSchema(many=True)
videos_blueprint = Blueprint('videos_blueprint', __name__, template_folder='templates')


@videos_blueprint.route('/video_list', methods=['GET', 'POST', 'DELETE'])
def videos_all():
    if request.method == 'GET':
        videos = db.session.query(VideoList).all()
        return jsonify(videos_schema.dump(videos))

    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@videos_blueprint.route('/video_list/<video_list_id>', methods=['GET', 'POST', 'DELETE'])
def videos_id(video_list_id):
    if request.method == 'GET':
        return video_list_id
    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')