from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import hashlib
#import para sqlserver
from urllib.parse import quote_plus
import pyodbc
from flask_mysqldb import MySQL
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'Localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '147852'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
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


@app.route('/photos')
def photos():
    return render_template('photos.html')

@app.route('/errormessage')
def errormessage():
    return render_template('errormessage.html', current_time=datetime.utcnow())


class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match!')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == ['POST'] and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
            
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        mysql.connection.commit()            
        cur.close()
        redirect(url_for('index'))
      
    return render_template('register.html', form=form)
        
    
if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = '147852'
    