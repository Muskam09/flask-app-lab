from flask import Flask, render_template, url_for, flash, redirect
from . import app
from app.forms import ContactForm

@app.route('/')
def resume():
  return render_template('resume.html', title='Моє Резюме')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data

        app.logger.info(f"New contact form submission: Name={name}, Email={email}, Phone={phone}, Message={message}")

        flash(f'Дякуємо, {name}! Ваше повідомлення на тему "{form.subject.data}" отримано.', 'success')

        return redirect(url_for('contact'))

    return render_template('contact.html', title='Контакти', form=form)