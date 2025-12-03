from app import db, bcrypt, login_manager
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from datetime import datetime, timezone
from flask_login import UserMixin
import typing
if typing.TYPE_CHECKING:
    from app.posts.models import Post


@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='profile_default.png')
    about_me: Mapped[str | None] = mapped_column(String(140))
    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'