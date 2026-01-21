from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    follower: Mapped[list["User"]] =  relationship(back_populates="user_from_id")
    following: Mapped[list["User"]] =  relationship(back_populates="user_to_id")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(String(300), nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="posts")
    medias: Mapped[list["Media"]] = relationship(back_populates="posts")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(150), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    id_post: Mapped[int] = mapped_column(ForeignKey("post.id"))

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    id_post: Mapped[int] = mapped_column(ForeignKey("post.id"))

class Follower(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    user_from_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    create_at: Mapped [datetime] = mapped_column (default = datetime.utcnow)