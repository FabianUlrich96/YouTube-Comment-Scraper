from database.models import Users, Apis, Jobs, VideoList, CommentList, ReplyList
from app_config import ma


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class ApisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Apis


class JobsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Jobs


class VideoListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VideoList


class CommentListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommentList


class ReplySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReplyList
