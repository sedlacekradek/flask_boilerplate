from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


# # setting up many-to-many relationship for User-Projects Project-Developers
# user_project = db.Table("user_project",
#                         db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
#                         db.Column("project_id", db.Integer(), db.ForeignKey("project.id"))
#                         )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    department = db.Column(db.String(), default="no department")
    description = db.Column(db.String(), default="no description filled in")
    avatar = db.Column(db.String(), default="/static/img/avatar-default.png")
    date_created = db.Column(db.DateTime(), default=func.now())
    comments = db.relationship("Comment", backref="user")
    likes = db.relationship("Like", backref="user")
    # more about the lazy parameter
    # https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef
    messages_sent = db.relationship('UserMessage', foreign_keys='UserMessage.sender_id', backref='author',
                                    lazy='dynamic')
    messages_received = db.relationship('UserMessage', foreign_keys='UserMessage.recipient_id', backref='recipient',
                                        lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime())
    notification_sent = db.relationship('UserNotification', foreign_keys='UserNotification.sender_id', backref='author',
                                        lazy='dynamic')
    notification_received = db.relationship('UserNotification', foreign_keys='UserNotification.recipient_id',
                                            backref='recipient', lazy='dynamic')
    last_notification_read_time = db.Column(db.DateTime())
    private_profile = db.Column(db.Boolean, default=False)

    def new_messages(self):
        # returns number of unread messages, called from HTML
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return UserMessage.query.filter_by(recipient=self).filter(UserMessage.timestamp > last_read_time).count()

    def new_notifications(self):
        # returns number of unread notifications, called from HTML
        last_read_time = self.last_notification_read_time or datetime(1900, 1, 1)
        return UserNotification.query.filter_by(recipient=self).filter(UserNotification.timestamp > last_read_time,
                                                                       UserNotification.author != self).count()


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String())
    date_created = db.Column(db.DateTime(), default=func.now())
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"), default=None)
    ticket_id = db.Column(db.Integer(), db.ForeignKey("ticket.id"), default=None)
    file = db.Column(db.String())
    deleted = db.Column(db.Boolean(), default=False)
    likes = db.relationship("Like", backref="comment", cascade="all,delete")


class Like(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    author = db.Column(db.Integer(), db.ForeignKey("user.id"))
    comment_id = db.Column(db.Integer(), db.ForeignKey("comment.id"))
    date_created = db.Column(db.DateTime(), default=func.now())


class UserMessage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime(), index=True, default=func.now())


class UserNotification(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    subject = db.Column(db.String())
    body = db.Column(db.String())
    type = db.Column(db.String())
    timestamp = db.Column(db.DateTime(), index=True, default=func.now())
