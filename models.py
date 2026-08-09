from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
import urllib.parse



db = SQLAlchemy()
login = LoginManager()



class User(UserMixin, db.Model):
    id:           so.Mapped[int] = so.mapped_column(primary_key=True)
    username:     so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email:        so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash:so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    name:         so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    avatar:       so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    bio:          so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    created_at:   so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    posts: so.Mapped[list["Post"]] = so.relationship("Post", back_populates="author", lazy="dynamic")

    

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar_url_generator(self):
        base_url = 'https://ui-avatars.com/api/'
        params = {
            'name': self.name,
            'background': 'CC5500',
            'color': 'fff'
        }
        self.avatar = f"{base_url}?{urllib.parse.urlencode(params)}"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    # use "user.id" (table.column) rather than User.id
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)

    author: so.Mapped[User] = so.relationship("User", back_populates="posts")

    def __repr__(self):
        return f'<Post {self.body}>'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Files(db.Model):
    id:         so.Mapped[int] = so.mapped_column(primary_key=True)
    course_code:so.Mapped[str] = so.mapped_column(sa.String(200))
    status:     so.Mapped[str] = so.mapped_column(sa.String(200))
    credit_unit:so.Mapped[int] = so.mapped_column(sa.Integer())
    courseMat: so.Mapped[list['Materials']] = so.relationship("Materials", backref="file", lazy=True)
class Materials(db.Model):
    id:         so.Mapped[int] = so.mapped_column(primary_key=True)
    filename:   so.Mapped[str] = so.mapped_column(sa.String(200))
    filepath:   so.Mapped[str] = so.mapped_column(sa.String(200) )
    c_id:  so.Mapped[int] = so.mapped_column(sa.ForeignKey("files.id"), index=True)

    
