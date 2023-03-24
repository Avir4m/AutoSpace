from . import db
from flask_login import UserMixin
import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(200), nullable=False, default="")
    picture = db.Column(db.String(), default="default_profile_pic.jpg")
    date_joined = db.Column(db.DateTime, default=datetime.datetime.now())
    permissions = db.Column(db.Integer(), default=0)
    verified = db.Column(db.Boolean(), default=False)

    #Badges
    developer = db.Column(db.Integer(), default=0)

    # Relationships

    posts = db.relationship("Post", backref="user", passive_deletes=True) # User's posts
    comments = db.relationship("Comment", backref="user", passive_deletes=True) # User's comments
    likes = db.relationship("Like", backref="user", passive_deletes=True) #User's likes
    saves = db.relationship("Saved", backref="user", passive_deletes=True) # User's saves
    spaces = db.relationship("Space", backref="user", passive_deletes=True) # User's spaces
    spaces_joined = db.relationship("SpaceMember", backref="user", passive_deletes=True) # User's spaces joined
    reports = db.relationship("Report", backref="user", passive_deletes=True) # User's reports
    messages = db.relationship("ChatMessage", backref="user", passive_deletes=True) # User's messages

    notifications = db.relationship("Notification", backref="user", passive_deletes=True, primaryjoin="and_(" "Notification.to==User.id)") # User's notifications
    actions = db.relationship("Notification", backref="user_action", passive_deletes=True, primaryjoin="and_(" "Notification.action_user==User.id)") # User's actions

    friends = db.relationship("Friend", backref="user_friend", passive_deletes=True, primaryjoin="""and_(Friend.status=='friends', or_(Friend.user_id1==User.id, Friend.user_id2==User.id))""") # User's friends
    friend_requests = db.relationship("Friend", backref="user_request", passive_deletes=True, primaryjoin="""and_(Friend.status=='pending', or_(Friend.user_id1==User.id, Friend.user_id2==User.id))""") # User's friend requests

    followers = db.relationship("Follow", backref="user", passive_deletes=True, primaryjoin="and_(" "Follow.followed_id==User.id)") # User's followers
    following = db.relationship("Follow", backref="follower", passive_deletes=True, primaryjoin="and_(" "Follow.follower_id==User.id)") # User's following


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String, default=None)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    url = db.Column(db.String(150), nullable=False, unique=True)
    edited = db.Column(db.Boolean(), default=False)
    private = db.Column(db.Boolean(), default=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comment", backref="post", passive_deletes=True)
    likes = db.relationship("Like", backref="post", passive_deletes=True)
    saves = db.relationship("Saved", backref="post", passive_deletes=True)
    space_id = db.Column(db.Integer, db.ForeignKey("space.id", ondelete="CASCADE"), nullable=True)
    reports = db.relationship("Report", backref="post", passive_deletes=True)


class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    edited = db.Column(db.Boolean(), default=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    reports = db.relationship("Report", backref="comment", passive_deletes=True)
    notifications = db.relationship("Notification", backref="comment", passive_deletes=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    notifications = db.relationship("Notification", backref="like", passive_deletes=True)


class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    picture = db.Column(db.String(), default=None)
    edited = db.Column(db.Boolean(), default=False)
    creator = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    url = db.Column(db.String(150), nullable=False, unique=True)
    posts = db.relationship("Post", backref="space", passive_deletes=True)
    members = db.relationship("SpaceMember", backref="space", passive_deletes=True)
    reports = db.relationship("Report", backref="space", passive_deletes=True)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=True)
    space_id = db.Column(db.Integer, db.ForeignKey("space.id", ondelete="CASCADE"), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id", ondelete="CASCADE"), nullable=True)


class SpaceMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey("space.id", ondelete="CASCADE"), nullable=False)


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user_id2 = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Text())  # Statuses: pending, friends
    notifications = db.relationship("Notification", backref="friend", passive_deletes=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    seen = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    action_user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    action = db.Column(db.String())
    message = db.Column(db.Text())
    like_id = db.Column(db.Integer(), db.ForeignKey("like.id", ondelete="CASCADE"), nullable=True)
    comment_id = db.Column(db.Integer(), db.ForeignKey("comment.id", ondelete="CASCADE"), nullable=True)
    friend_id = db.Column(db.Integer(), db.ForeignKey("friend.id", ondelete="CASCADE"), nullable=True)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    members = db.relationship("ChatMember", backref="chat", passive_deletes=True)
    messages = db.relationship("ChatMessage", backref="chat", passive_deletes=True)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id =  db.Column(db.Integer, db.ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    message = db.Column(db.Text())
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

class ChatMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id =  db.Column(db.Integer, db.ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)