from . import post_bp # Імпортуємо наш blueprint
from flask import render_template, redirect, url_for, flash, session, request
from app import db
from .models import Post, Tag
from .forms import PostForm, EmptyForm
from app.users.models import User

@post_bp.route('/')
def list_all():
    """US02: Відображення списку всіх видимих постів"""

    # 1. Робимо запит до БД
    stmt = db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()

    return render_template('posts.html', posts=posts)

# US01: Створення поста
@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    stmt = db.select(User).order_by(User.username)
    form.author_id.choices = [(user.id, user.username) for user in db.session.scalars(stmt).all()]
    
    if form.validate_on_submit():
        user_id = form.author_id.data

        new_post = Post(
          title=form.title.data,
          content=form.content.data,
          category=form.category.data,
          user_id=user_id,
          is_active=form.enabled.data
        )
        if form.publish_date.data:
            new_post.posted = form.publish_date.data

        tag_ids = form.tags.data
        stmt = db.select(Tag).where(Tag.id.in_(tag_ids))
        new_post.tags = db.session.scalars(stmt).all()

        db.session.add(new_post)
        db.session.commit()

        flash('Post added successfully', 'success')

        return redirect(url_for('posts.list_all'))

    return render_template('add_post.html', form=form, title="Create a New Post")

@post_bp.route('/<int:id>')
def detail_post(id):
    """US03: Відображення одного поста."""

    post = db.get_or_404(Post, id)

    return render_template('detail_post.html', post=post)

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    """US04: Редагування існуючого поста (REFACTORED)."""
    post = db.get_or_404(Post, id)

    form = PostForm()

    stmt_users = db.select(User).order_by(User.username)
    form.author_id.choices = [(user.id, user.username) for user in db.session.scalars(stmt_users).all()]
    stmt_tags = db.select(Tag).order_by(Tag.name)
    form.tags.choices = [(tag.id, tag.name) for tag in db.session.scalars(stmt_tags).all()]


    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.user_id = form.author_id.data

        if form.publish_date.data:
            post.posted = form.publish_date.data

        tag_ids = form.tags.data
        stmt = db.select(Tag).where(Tag.id.in_(tag_ids))
        post.tags = db.session.scalars(stmt).all()
        
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]


    return render_template('add_post.html', form=form, title="Update Post")

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    """US05: Видалення існуючого поста."""
    post = db.get_or_404(Post, id)
    form = EmptyForm()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted', 'danger')
        return redirect(url_for('posts.list_all'))

    return render_template('delete_confirm.html', post=post, form=form)