from flask import Flask, flash, redirect, render_template, request, url_for, logging, session
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import hashlib, os
import pyodbc
from urllib.parse import quote_plus
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def connect():
    cnxn = pyodbc.connect('driver={SQL Server};''server=DARKMATTER-PC;''database=myflaskapp1;''trusted_consnection=yes')
    cnxn.setencoding('utf-8') 
    return cnxn
cursor = connect()                    

#cnxn = pyodbc.connect('driver={SQL Server};''server=DARKMATTER-PC;''database=myflask;''trusted_consnection=yes')
#cursor = cnxn.cursor()

Articles = Articles()

@app.route('/') 
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')  


@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)  


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


@app.route('/errormessage')
def errormessage():
    return render_template('errormessage.html', current_time=datetime.utcnow())


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50, message=None)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50, message=None)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25, message=None)]) 
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Password do not match!')])
    confirm = PasswordField('confirm Password', [validators.DataRequired()])
    register_date = datetime.now()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        register_date = form.register_date

        cursor.execute("INSERT INTO users(name, email, username, password, register_date) VALUES(?, ?, ?, ?, ?)", (name, email, username, password, register_date)) 
        cursor.commit()
        cursor.close()
        flash("Thanks for registering")
        return index()
      
    return render_template('register.html', form=form)
        
    
if __name__ == '__main__':
    app.run(debug=True)
    