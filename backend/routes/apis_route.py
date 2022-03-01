from app_config import db
from flask import request, jsonify, Blueprint
from database.models import Apis
from database.schemas import ApisSchema
import logger
import pandas as pd
from sqlalchemy.exc import IntegrityError
log = logger.create_logger(__name__)
api_schema = ApisSchema()
apis_schema = ApisSchema(many=True)
apis_blueprint = Blueprint('apis_blueprint', __name__, template_folder='templates')


@apis_blueprint.route('/apis', methods=['GET', 'POST', 'DELETE'])
def apis_all():
    if request.method == 'GET':
        apis = []
        for value in db.session.query(Apis.name).distinct():
            log.info(value)
            apis.append(value)

        to_list = [x[0] for x in apis]
        log.info(to_list)
        return jsonify(to_list)

    if request.method == 'POST':
        data = request.json

        name = data["name"]
        token = data["token"]
        token_list = token.split(",")
        log.info(token_list)
        data_list = []

        for element in token_list:
            data_list.append([name, element])
        columns = ['name', 'token']
        df = pd.DataFrame(data_list, columns=columns)
        log.info(df)
        try:
            df.to_sql('apis', con=db.engine, if_exists='append', chunksize=1000, index=False)
        except IntegrityError as e:
            log.error(e)
        return 'Ok'
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@apis_blueprint.route('/apis/<api_id>', methods=['GET', 'POST', 'DELETE'])
def apis_id(api_id):
    if request.method == 'GET':
        return api_id
    if request.method == 'POST':
        log.info(api_id)
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')