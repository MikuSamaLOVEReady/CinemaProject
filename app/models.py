from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64), index=True)


class Order(db.Model):
    __tablename__ = 'orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, index=True)  # 购票客户
    SID = db.Column(db.Integer, db.ForeignKey('schedules.ScheduleID'), index=True)
    Seat = db.Column(db.Integer)
    DealTime = db.Column(db.String(32))


class FilmSchedule(db.Model):
    __tablename__ = 'schedules'
    ScheduleID = db.Column(db.Integer, primary_key=True, index=True)
    FID = db.Column(db.Integer, db.ForeignKey('films.FilmID'))
    Room = db.Column(db.Integer)
    Date = db.Column(db.Date, index=True)
    Time = db.Column(db.String(16))
    Price = db.Column(db.Integer)
    film = db.relationship("Films", backref="TheSchedule")

#多对多的额外表
film_tag_table = db.Table('film_tag_table',
                          db.Column('film_id', db.Integer, db.ForeignKey('films.FilmID')),
                          db.Column('tag_id', db.Integer, db.ForeignKey('tags.Id')))


class Films(db.Model):
    __tablename__ = 'films'
    FilmID = db.Column(db.Integer, primary_key=True)
    FilmName = db.Column(db.String(64), unique=True, index=True)
    Blurb = db.Column(db.String(1024))
    Certificate = db.Column(db.String(1024))  # 凭证，不知道是啥
    Director = db.Column(db.String(64))
    LeadActors = db.Column(db.String(512))
    FilmLength = db.Column(db.Integer)
    Ranking = db.Column(db.Integer)
    #利用多对多关系，为Tag表增加 一个backfre 。这样只用在tag.films就可以从tag中找出所有该类型的电影
    #如果要得到所有 一个电影的所有tag 就直接 film.Genre.all
    Genre = db.relationship('Tag', secondary=film_tag_table, backref=db.backref('films', lazy='dynamic'),
                            lazy='dynamic')
    image = db.Column(db.String(150), index=True)


class Tag(db.Model):
    __tablename__ = 'tags'
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
