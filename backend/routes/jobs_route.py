import datetime
from app_config import db
from flask import request, jsonify, Blueprint
from database.models import Jobs, VideoList
from database.schemas import JobsSchema
from database.models import Apis
from database.models import CommentList
from database.models import ReplyList
import logger
import pandas as pd
from sqlalchemy.exc import IntegrityError
from celery import Celery

log = logger.create_logger(__name__)
job_schema = JobsSchema()
jobs_schema = JobsSchema(many=True)
jobs_blueprint = Blueprint('jobs_blueprint', __name__, template_folder='templates')

celery_context = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@jobs_blueprint.route('/jobs', methods=['GET', 'POST', 'DELETE'])
def jobs_all():
    if request.method == 'GET':
        jobs = db.session.query(Jobs).all()
        return jsonify(jobs_schema.dump(jobs))

    if request.method == 'POST':
        all_data = request.json
        job_type = all_data["job_type"]

        log.info(all_data)
        selected_job = None
        name = None
        api = None
        query = None
        published_before = None
        published_after = None

        if "selected_job" in all_data:
            selected_job = all_data["selected_job"]
        if "name" in all_data:
            name = all_data["name"]
        date = datetime.datetime.now()
        if "query" in all_data:
            query = all_data["query"]
        if "published_before" in all_data:
            published_before = all_data["published_before"]
        if "published_after" in all_data:
            published_after = all_data["published_after"]
        done = False
        failed = None
        status = 0
        total = None

        if "api" in all_data:
            api = all_data["api"]
            api_row = db.session.query(Apis.token).filter(Apis.name == api).all()
            keys = [x[0] for x in api_row]
            log.info(keys)

        job_id = ""
        try:
            job = Jobs(None, job_type, name, date, query, status, total, done, published_before, published_after, failed)
            db.session.add(job)
            db.session.flush()
            db.session.refresh(job)
            job_id = job.job_id
            db.session.commit()
        except IntegrityError as e:
            log.error(e)

        if job_type == "comment":

            videos = db.session.query(VideoList.video_id).filter(VideoList.job == selected_job).all()

            video_ids = [item[0] for item in videos]

            task = celery_context.send_task('tasks.query_comments', queue="comments", kwargs={'keys': keys, 'job_id': job_id, 'video_ids': video_ids})

        if job_type == "video":
            task = celery_context.send_task('tasks.query_videos', queue="video", kwargs={'keys': keys, 'job_id': job_id, 'query': query,
                                                                          'published_before': published_before,
                                                                          'published_after': published_after})

        if job_type == "video_loader":
            file = all_data['file']

            video_df = pd.DataFrame(file)
            new_header = video_df.iloc[0]
            video_df = video_df[1:]
            video_df.columns = new_header
            video_df = video_df.drop('id', axis=1)
            video_df = video_df.drop('job', axis=1)
            video_df['job'] = job_id
            try:
                video_df.to_sql('video_list', con=db.engine, if_exists='append', chunksize=1000, index=False)
            except IntegrityError as e:
                log.error(e)

        if job_type == "translation":
            task = celery_context.send_task('tasks.translate_comments', queue="translation", kwargs={'selected_job': selected_job, 'job_id': job_id})
            #reply_task = celery_context.send_task('tasks.translate_replies', queue="translation", kwargs={'selected_job': selected_job, 'job_id': job_id})

        return 'Ok'
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@jobs_blueprint.route('/jobs/<job_id>', methods=['GET', 'POST', 'DELETE'])
def jobs_id(job_id):
    if request.method == 'GET':
        return job_id
    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')
