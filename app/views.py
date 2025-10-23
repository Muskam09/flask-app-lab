from flask import Flask, render_template, url_for
from . import app

@app.route('/')
def resume():
  return render_template('resume.html', title='Моє Резюме')

@app.route('/contact')
def contact():
  return render_template('contact.html', title='Контакти')
