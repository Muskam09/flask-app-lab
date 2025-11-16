from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Enum, Integer, Boolean
import datetime

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
    author: Mapped[str] = mapped_column(String(20), default='Anonymous')

    def __repr__(self):
        return f'<Post(title="{self.title}")>'