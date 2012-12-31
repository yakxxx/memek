from mongoengine import *


class Comment(Document):
    author = StringField()
    author_avatar = StringField()
    author_avatar = StringField()
    author_avatar_big = StringField()
    author_avatar_lo = StringField()
    author_avatar_med = StringField()
    author_group = IntField()
    author_sex = StringField()
    blocked = BooleanField()
    body = StringField()
    can_vote = BooleanField()
    date = DateTimeField()
    deleted = BooleanField()
    embed = StringField()
    comment_id = IntField(db_field = 'id')
    link = ListField()
    parent_id = IntField()
    vote_count = IntField()
    vote_count_minus = IntField()
    vote_count_plus = IntField()

    
class Article(Document):
    author = StringField()
    author_avatar = StringField()
    author_avatar_big = StringField()
    author_avatar_lo = StringField()
    author_avatar_med = StringField()
    author_group = IntField()
    author_sex = StringField()
    can_vote = BooleanField()
    category = StringField()
    category_name = StringField()
    comment_count = IntField()
    date = DateTimeField()
    description = StringField()
    group = StringField()
    has_own_content = BooleanField()
    article_id = IntField(db_field = 'id')
    is_hot = BooleanField()
    plus18 = BooleanField()
    preview = StringField()
    related_count = IntField()
    report_count = IntField()
    source_url = StringField()
    status = StringField()
    tags = StringField()
    title = StringField()
    type = StringField()
    url = StringField()
    vote_count = IntField()
