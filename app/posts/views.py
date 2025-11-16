from . import post_bp # Імпортуємо наш blueprint
from flask import render_template, redirect, url_for, flash, session, request
from app import db
from .models import Post
from .forms import PostForm, EmptyForm

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
    
    if form.validate_on_submit():
        author = session.get('username', 'Anonymous') 

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=author
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        flash('Post added successfully', 'success')

        return redirect(url_for('posts.list_all'))

    return render_template('add_post.html', form=form)

@post_bp.route('/<int:id>')
def detail_post(id):
    """US03: Відображення одного поста."""

    post = db.get_or_404(Post, id)

    return render_template('detail_post.html', post=post)

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    """US04: Редагування існуючого поста (REFACTORED)."""
    post = db.get_or_404(Post, id)

    if request.method == 'POST':
        form = PostForm()
        if form.validate_on_submit():
            form.populate_obj(post)

            if form.publish_date.data:
              post.posted = form.publish_date.data

            post.is_active = form.enabled.data

            db.session.commit()
            flash('Post has been updated!', 'success')
            return redirect(url_for('posts.detail_post', id=post.id))

    form = PostForm(obj=post)

    form.publish_date.data = post.posted
    form.enabled.data = post.is_active

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