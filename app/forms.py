from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, TextAreaField, SubmitField, 
    PasswordField, BooleanField
)
from wtforms.validators import DataRequired, Length, Email, Regexp

# ===== ЗАВДАННЯ 1: КЛАС ДЛЯ КОНТАКТНОЇ ФОРМИ =====
class ContactForm(FlaskForm):
    # Поле Name
    name = StringField('Ім\'я', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(min=4, max=10, message="Ім'я має бути від 4 до 10 символів")
    ])

    # Поле Email
    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Email(message="Введіть коректну email-адресу.")
    ])
    
    # Поле Phone Формат: +380?????????
    phone = StringField('Телефон', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Regexp(r'^\+380\d{9}$',
               message="Формат телефону має бути +380XXXXXXXXX (12 цифр)")
    ])
    
    # Поле Subject (Випадаючий список)
    subject = SelectField('Тема', choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('feedback', 'Відгук')
    ], validators=[DataRequired()])
    
    # Поле Message
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(max=500, message="Повідомлення не може перевищувати 500 символів")
    ])
    
    submit = SubmitField('Надіслати')


# ===== ЗАВДАННЯ 2: КЛАС ДЛЯ ФОРМИ ЛОГІНУ =====
class LoginForm(FlaskForm):
    # Поле Username
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(message="Це поле обов'язкове.")
    ])
    
    # Поле Password
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ])
    
    # Поле Remember Me
    remember = BooleanField("Запам'ятати мене")
    
    submit = SubmitField('Увійти')