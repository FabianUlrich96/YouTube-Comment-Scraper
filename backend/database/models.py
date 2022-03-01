from app_config import db
from sqlalchemy.orm import backref


class Users(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.Text)
    date_created = db.Column(db.Date)


class Apis(db.Model):
    api_id = db.Column('api_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    token = db.Column(db.String(50))

    def __init__(self, api_id, name, token):
        self.api_id = api_id
        self.name = name
        self.token = token


class Jobs(db.Model):
    job_id = db.Column('job_id', db.Integer, primary_key=True, autoincrement=True)
    job_type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    date = db.Column(db.Date)
    query = db.Column(db.String(200))
    published_before = db.Column(db.Date)
    published_after = db.Column(db.Date)
    status = db.Column(db.Integer)
    total = db.Column(db.Integer)
    done = db.Column(db.Boolean)
    failed_at = db.Column(db.Text)

    def __init__(self, job_id, job_type, name, date, query, status, total, done, published_before, published_after, failed_at):
        self.job_id = job_id
        self.job_type = job_type
        self.name = name
        self.date = date
        self.query = query
        self.published_before = published_before
        self.published_after = published_after
        self.status = status
        self.total = total
        self.done = done
        self.failed_at = failed_at


class VideoList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(50))
    kind = db.Column(db.String(50))
    job = db.Column(db.Integer, db.ForeignKey(Jobs.job_id))
    job_backref = db.relationship("Jobs", backref=backref("jobs", uselist=False))
    page = db.Column(db.String(50))
    date = db.Column(db.Date)

    def __init__(self, id, video_id, kind, job, page, date):
        self.id = id
        self.video_id = video_id
        self.kind = kind
        self.job = job
        self.page = page
        self.date = date


class CommentList(db.Model):
    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(50))
    job = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    page = db.Column(db.Text)
    date = db.Column(db.Date)
    author = db.Column(db.Text)
    likes = db.Column(db.Integer)
    published = db.Column(db.Date)
    updated = db.Column(db.Date)
    reply_count = db.Column(db.Integer)
    comment_id = db.Column(db.String(50))
    comment = db.Column(db.Text)
    translation = db.Column(db.Text)

    def __init__(self, table_id, video_id, job, page, date, author, likes, published, updated, reply_count, comment_id, comment, translation):
        self.table_id = table_id
        self.video_id = video_id
        self.job = job
        self.page = page
        self.date = date
        self.author = author
        self.likes = likes
        self.published = published
        self.updated = updated
        self.reply_count = reply_count
        self.comment_id = comment_id
        self.comment = comment
        self.translation = translation


class ReplyList(db.Model):
    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(50))
    job = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    page = db.Column(db.Text)
    date = db.Column(db.Date)
    parent_id = db.Column(db.String(50))
    author = db.Column(db.Text)
    likes = db.Column(db.Integer)
    published = db.Column(db.Date)
    updated = db.Column(db.Date)
    comment = db.Column(db.Text)
    translation = db.Column(db.Text)

    def __init__(self, table_id, video_id, job, page, date, parent_id, author, likes, published, updated, comment, translation):
        self.table_id = table_id
        self.video_id = video_id
        self.job = job
        self.page = page
        self.date = date
        self.parent_id = parent_id
        self.author = author
        self.likes = likes
        self.published = published
        self.updated = updated
        self.comment = comment
        self.comment = translation



