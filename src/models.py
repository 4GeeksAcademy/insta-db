import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
Base = declarative_base()
class User(Base):
    __tablename__ = 'User'
    ID = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    posts = relationship("Post", back_populates="user")
    followers = relationship("Follower", foreign_keys='Follower.user_from_id', back_populates="user_from")
    following = relationship("Follower", foreign_keys='Follower.user_to_id', back_populates="user_to")
    comments = relationship("Comment", back_populates="author")
class Post(Base):
    __tablename__ = 'Post'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.ID'))
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")
class Follower(Base):
    __tablename__ = 'Follower'
    user_from_id = Column(Integer, ForeignKey('User.ID'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('User.ID'), primary_key=True)
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="followers")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="following")
class Media(Base):
    __tablename__ = 'Media'
    ID = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', 'audio', name='media_types'), nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('Post.ID'))
    post = relationship("Post", back_populates="media")
class Comment(Base):
    __tablename__ = 'Comment'
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('User.ID'))
    post_id = Column(Integer, ForeignKey('Post.ID'))
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e