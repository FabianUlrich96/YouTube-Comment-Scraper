from app_config import db
from flask import request, jsonify, Blueprint
from database.models import CommentList
from database.schemas import CommentListSchema
import logger
log = logger.create_logger(__name__)
comment_schema = CommentListSchema()
comments_schema = CommentListSchema(many=True)
comments_blueprint = Blueprint('comments_blueprint', __name__, template_folder='templates')


@comments_blueprint.route('/comment_list', methods=['GET', 'POST', 'DELETE'])
def comments_all():
    if request.method == 'GET':
        videos = db.session.query(CommentList).all()
        return jsonify(comments_schema.dump(videos))

    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@comments_blueprint.route('/comment_list/<comment_list_id>', methods=['GET', 'POST', 'DELETE'])
def comments_id(comment_list_id):
    if request.method == 'GET':
        return comment_list_id
    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')