from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import(
  String, Text, DateTime, Enum, Integer, Boolean,
  func, ForeignKey, Table, Column
  )
import datetime
import typing
if typing.TYPE_CHECKING:
    from app.users.models import User

post_tags = Table(
    'post_tags',
    db.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Зв'язок "багато-до-багатьох" з Post
    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags, 
        back_populates="tags"
    )
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.UTC)
    )
    category: Mapped[str] = mapped_column(
        Enum('news', 'publication', 'tech', 'other', name='post_categories'),
        default='other',
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags, 
        back_populates="posts"
    )
    
    def __repr__(self):
        return f'<Post(title="{self.title}")>'