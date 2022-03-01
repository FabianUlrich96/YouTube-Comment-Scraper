from sqlalchemy.orm import sessionmaker

import logger
from database.models import CommentList
from database.models import ReplyList
import re
import html
import urllib.request
from urllib.error import URLError, HTTPError
import urllib.parse
import math
import time
from sqlalchemy import create_engine
from database.models import Jobs

log = logger.create_logger(__name__)


engine = create_engine('mysql+pymysql://dataapi:fnmwm4d833834erjn@dataapidb/dataapi?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()


def unescape(text):
    parser = html
    return parser.unescape(text)


def prepare_translate(translation_object):
    if len(translation_object) < 5000:
        return True, translation_object
    else:
        n = int(math.ceil((len(translation_object) / 5000)))
        chunk_len = len(translation_object) // n
        res = []

        for idx in range(0, len(translation_object), chunk_len):
            res.append(translation_object[idx: idx + chunk_len])
        return False, res


def translate(to_translate, job_id, to_language="auto", from_language="auto"):
    agent = {'User-Agent':
                 "Mozilla/4.0 (\
                 compatible;\
                 MSIE 6.0;\
                 Windows NT 5.1;\
                 SV1;\
                 .NET CLR 1.1.4322;\
                 .NET CLR 2.0.50727;\
                 .NET CLR 3.0.04506.30\
                 )"}

    base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"

    to_translate = urllib.parse.quote(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    try:
        request = urllib.request.Request(link, headers=agent)
        raw_data = urllib.request.urlopen(request).read()
        data = raw_data.decode("utf-8")
        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        re_result = re.findall(expr, data)

        if len(re_result) == 0:
            result = ""
        else:
            result = unescape(re_result[0])

        return result
    except HTTPError as err:
        log.error(err)
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.failed_at = to_translate
        session.commit()
    except URLError as err:
        log.error(err)
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.failed_at = to_translate
        session.commit()


def translate_text(comment_array, table, job_id, count_now, count_total):
    for translation_object in comment_array:
        time.sleep(1)
        length_check, prepared_string = prepare_translate(translation_object)

        if length_check:
            if table == "comment_list":
                translation = translate(translation_object, job_id, to_language="en")
                translation_db = session.query(CommentList).filter_by(comment=translation_object).first()
                translation_db.translation = translation
                session.commit()
            if table == "reply_list":
                translation = translate(translation_object, job_id, to_language="en")
                translation_db = session.query(ReplyList).filter_by(comment=translation_object).first()
                translation_db.translation = translation
                session.commit()
        else:
            translation = ['']
            for translation_string in prepared_string:
                translation_chunk = translate(translation_string, job_id, to_language="en")
                translation.append(translation_chunk)

            translation = ' '.join(translation)
            if table == "comment_list":
                translation_db = session.query(CommentList).filter_by(comment=translation_object).first()
                translation_db.translation = translation
                session.commit()
            if table == "reply_list":
                translation_db = session.query(ReplyList).filter_by(comment=translation_object).first()
                translation_db.translation = translation
                session.commit()

        count_now = count_now + 1
        job_db = session.query(Jobs).filter_by(job_id=job_id).first()
        job_db.status = count_now
        session.commit()

    return count_now
