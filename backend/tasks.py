from sqlalchemy.orm import sessionmaker
import logger
from celery import Celery
from celery.utils.log import get_task_logger
from logic.YouTubeDataApi import execute_search_query
from logic.YouTubeDataApi import get_comments
from logic.GoogleTranslate import translate_text
from sqlalchemy import create_engine, func, select
from database.models import CommentList
from database.models import ReplyList
from database.models import Jobs


log = logger.create_logger(__name__)

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

engine = create_engine('mysql+pymysql://dataapi:fnmwm4d833834erjn@dataapidb/dataapi?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()


@celery.task(queue="video")
def query_videos(keys, job_id, query, published_before, published_after):
    execute_search_query(keys, job_id, query, published_before, published_after)
    job_db = session.query(Jobs).filter_by(job_id=job_id).first()
    job_db.done = True
    session.commit()


@celery.task(queue="comments")
def query_comments(keys, job_id, video_ids):

    count_total = len(video_ids)
    count_now = 0
    job_db = session.query(Jobs).filter_by(job_id=job_id).first()
    job_db.status = count_now
    job_db.total = count_total
    session.commit()
    for video in video_ids:
        get_comments(keys, job_id, video)
        count_now = count_now + 1
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.status = count_now
        session.commit()

    job_db = session.query(Jobs).filter_by(job_id=job_id).first()
    job_db.done = True
    session.commit()


@celery.task(queue="translation")
def translate_comments(selected_job, job_id):
    count_comments = (
        session.execute(select(func.count()).select_from(select(CommentList.video_id).filter(
            CommentList.translation == None, CommentList.job == selected_job).subquery())).scalar_one()
    )

    count_replies = (
        session.execute(select(func.count()).select_from(select(ReplyList.video_id).filter(
            ReplyList.translation == None, ReplyList.job == selected_job).subquery())).scalar_one()
    )

    log.info(count_comments)
    log.info(count_replies)
    count_total = count_comments + count_replies
    count_now = 0
    job_db = session.query(Jobs).filter_by(job_id=job_id).first()
    job_db.status = count_now
    job_db.total = count_total
    session.commit()
    execute = True
    limit = 1000
    offset = 0
    while execute:

        comments = session.query(CommentList.comment).filter(
            CommentList.translation == None, CommentList.job == selected_job).limit(limit).offset(offset).all()
        if not comments:
            execute = False
        else:
            offset = offset + 1000
            raw_comments = [item[0] for item in comments]
            count_now = translate_text(raw_comments, "comment_list", job_id, count_now, count_total)

    execute = True
    limit = 1000
    offset = 0
    while execute:
        comments = session.query(ReplyList.comment).filter(
            ReplyList.translation == None, ReplyList.job == selected_job).limit(limit).offset(offset).all()
        if not comments:
            execute = False
        else:
            offset = offset + 1000
            raw_comments = [item[0] for item in comments]
            log.info(raw_comments)
            count_now = translate_text(raw_comments, "reply_list", job_id, count_now, count_total)

    job_db = session.query(Jobs).filter_by(job_id=job_id).first()
    job_db.done = True
    session.commit()

