from mongoengine import *

    
class Article(Document):
    # **** fields from api ****
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
    article_id = IntField(unique = True)
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
    
    #***** control fields *****
    comments_crawled = BooleanField(default=False)


class Comment(Document):
    # **** fields from api ****
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
    embed = DictField()
    comment_id = IntField(unique = True)
    link = ListField()
    parent_id = IntField()
    vote_count = IntField()
    vote_count_minus = IntField()
    vote_count_plus = IntField()

    #***** control fields *****
    article = ReferenceField(Article)
    
    
    
    
    