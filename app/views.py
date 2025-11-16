from flask import render_template, flash, redirect, url_for, Blueprint, current_app
from app.forms import ContactForm



main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def resume():
    return render_template('resume.html', title='Моє Резюме')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data


        current_app.logger.info(f"New contact form submission: Name={name}, Email={email}, Phone={phone}, Message={message}")

        flash(f'Дякуємо, {name}! Ваше повідомлення на тему "{form.subject.data}" отримано.', 'success')
        
        return redirect(url_for('main.contact'))

    return render_template('contact.html', title='Контакти', form=form)