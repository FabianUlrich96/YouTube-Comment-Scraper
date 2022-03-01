import datetime
import googleapiclient.discovery
from sqlalchemy.exc import IntegrityError
import pandas as pd
from googleapiclient.errors import HttpError
import pause
from datetime import datetime
from pytz import timezone
from sqlalchemy.orm import sessionmaker
import logger
from sqlalchemy import create_engine

from database.models import Jobs

log = logger.create_logger(__name__)

db = create_engine('mysql+pymysql://dataapi:fnmwm4d833834erjn@dataapidb/dataapi?charset=utf8mb4')

Session = sessionmaker(bind=db)
session = Session()


def save_video_list(data, job_id, page_token):
    try:
        data.to_sql('video_list', con=db.engine, if_exists='append', chunksize=1000, index=False)
    except IntegrityError as e:
        log.error(e)
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.failed_at = page_token
        session.commit()


def new_connection(key):
    api_service_name = "youtube"
    api_version = "v3"

    api_connection = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

    return api_connection


def execute_search_query(keys, job_id, search_query, published_before, published_after):
    page_token = ""
    before_object = datetime.strptime(published_before, '%Y-%m-%d')
    after_object = datetime.strptime(published_after, '%Y-%m-%d')
    before = before_object.isoformat("T") + "Z"
    after = after_object.isoformat("T") + "Z"
    try:
        key_position = 0
        queried = 0
        while page_token is not None and True:
            log.info(page_token)
            log.info("Key with this position is used")
            log.info(key_position)
            keys_length = len(keys) - 1
            kind = []
            result_id = []
            response = None
            try:
                api_connection = new_connection(keys[key_position])
                request = api_connection.search().list(
                    part="id", q=search_query, maxResults=50, pageToken=page_token, publishedAfter=after,
                    publishedBefore=before, fields="items()"
                )
                response = request.execute()

                job_db = session.query(Jobs).filter_by(job_id=job_id).first()
                per_page = response["pageInfo"]["resultsPerPage"]
                queried = queried + per_page
                job_db.status = queried
                session.commit()

            except HttpError as err:
                log.error("HTTP Error: {}".format(err))
                status_code = err.resp.status
                if status_code == 403 and key_position < keys_length:
                    key_position = key_position + 1
                else:
                    the_date = datetime.now()
                    pacific = the_date.astimezone(timezone('US/Pacific'))
                    current_time = pacific.strftime("%H:%M:%S")
                    time_eod = '23:59:59'
                    time_format = '%H:%M:%S'

                    time_delta = datetime.strptime(time_eod, time_format) - datetime.strptime(current_time,
                                                                                              time_format)
                    offset = 1800
                    pause_time = time_delta.seconds

                    log.info("Idling for {} seconds".format(pause_time + offset))
                    pause.seconds(pause_time + offset)
                    key_position = 0
                continue

            try:
                page_token = response["nextPageToken"]
            except KeyError:
                page_token = None
                log.info("Reached last page!")

            for item in response["items"]:
                kind.append(item["kind"])
                try:
                    result_id.append(item["id"]["videoId"])

                except KeyError:
                    try:
                        result_id.append(item["id"]["channelId"])
                    except KeyError:
                        result_id.append(None)
            data = {'kind': kind, 'video_id': result_id}
            # Save each badge to database
            dataframe = pd.DataFrame(data)
            dataframe['job'] = job_id
            dataframe['page'] = page_token
            now = datetime.now()
            date_now = now.strftime("%Y/%m/%d")
            dataframe['date'] = date_now
            save_video_list(dataframe, job_id, page_token)

    except TypeError as err:
        log.error("Next page failed with error: {}".format(err))
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.failed_at = page_token
        session.commit()


def save_reply_list(data, job_id, page_token):
    try:
        data.to_sql('reply_list', con=db.engine, if_exists='append', chunksize=1000, index=False)
    except IntegrityError as e:
        log.error(e)
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.failed_at = page_token
        session.commit()


def save_comment_list(data):
    try:
        data.to_sql('comment_list', con=db.engine, if_exists='append', chunksize=1000, index=False)
    except IntegrityError as e:
        log.error(e)


def get_comments(keys, job_id, video_id):
    page_token = ""
    try:
        key_position = 0
        while page_token is not None and True:
            log.info(key_position)
            keys_length = len(keys) - 1
            response = None
            author = []
            likes = []
            published = []
            updated = []
            comment = []
            reply_count = []
            comment_id = []
            parent_id = []
            reply_author = []
            reply_likes = []
            reply_published = []
            reply_updated = []
            reply_comment = []
            try:
                log.info(keys[key_position])
                api_connection = new_connection(keys[key_position])
                request = api_connection.commentThreads().list(
                    maxResults=50,
                    part='snippet,replies',
                    videoId=video_id,
                    pageToken=page_token
                )
                response = request.execute()
            except HttpError as err:
                log.error("HTTP Error: {}".format(err))
                status_code = err.resp.status
                if status_code == 403 and key_position < keys_length:
                    key_position = key_position + 1
                else:
                    the_date = datetime.now()
                    pacific = the_date.astimezone(timezone('US/Pacific'))
                    current_time = pacific.strftime("%H:%M:%S")
                    time_eod = '23:59:59'
                    time_format = '%H:%M:%S'

                    time_delta = datetime.strptime(time_eod, time_format) - datetime.strptime(current_time,
                                                                                              time_format)
                    offset = 1800
                    pause_time = time_delta.seconds

                    log.info("Idling for {} seconds".format(pause_time + offset))
                    pause.seconds(pause_time + offset)
                    key_position = 0
                continue

            try:
                page_token = response["nextPageToken"]
            except KeyError:
                page_token = None

            for item in response['items']:
                author.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                published_string = item['snippet']['topLevelComment']['snippet']['publishedAt'][:-1]
                published_date = datetime.fromisoformat(published_string)
                published.append(published_date)

                updated_string = item['snippet']['topLevelComment']['snippet']['updatedAt'][:-1]
                updated_date = datetime.fromisoformat(updated_string)
                updated.append(updated_date)

                comment.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                reply_count.append(item['snippet']['totalReplyCount'])
                comment_id.append(item['snippet']['topLevelComment']['id'])

                replies = item['snippet']['totalReplyCount']

                # if reply is there
                if replies > 0:

                    # iterate through all reply
                    for reply in item['replies']['comments']:
                        # Extract reply
                        parent_id.append(reply['snippet']['parentId'])
                        reply_author.append(reply['snippet']['authorDisplayName'])
                        reply_likes.append(reply['snippet']['likeCount'])

                        reply_published_string = reply['snippet']['publishedAt'][:-1]
                        reply_published_date = datetime.fromisoformat(reply_published_string)
                        reply_published.append(reply_published_date)
                        reply_updated_string = reply['snippet']['updatedAt'][:-1]
                        reply_updated_date = datetime.fromisoformat(reply_updated_string)
                        reply_updated.append(reply_updated_date)

                        reply_comment.append(reply['snippet']['textDisplay'])

            comment_data = {'video_id': video_id, 'author': author, 'likes': likes, 'published': published,
                            'updated': updated, 'comment': comment, 'reply_count': reply_count,
                            'comment_id': comment_id}
            reply_data = {'video_id': video_id, 'parent_id': parent_id, 'author': reply_author,
                          'likes': reply_likes, 'published': reply_published, 'updated': reply_updated,
                          'comment': reply_comment}

            comment_dataframe = pd.DataFrame(comment_data)
            comment_dataframe['job'] = job_id
            comment_dataframe['page'] = page_token
            now = datetime.now()
            date_now = now.strftime("%Y/%m/%d")
            comment_dataframe['date'] = date_now
            save_comment_list(comment_dataframe)

            reply_dataframe = pd.DataFrame(reply_data)
            reply_dataframe['job'] = job_id
            reply_dataframe['page'] = page_token
            now = datetime.now()
            date_now = now.strftime("%Y/%m/%d")
            reply_dataframe['date'] = date_now

            save_reply_list(reply_dataframe, job_id, page_token)
            break

    except TypeError as err:
        log.error("Next page failed with error: {}".format(err))
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.failed_at = page_token
        session.commit()
