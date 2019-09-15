from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import hashlib
from passlib.hash import sha256_crypt
#import para sqlserver
from urllib.parse import quote_plus
import pyodbc
from sqlalchemy import create_engine

app = Flask(__name__)

parametros = (
# Driver que será utilizado na conexão#
    'DRIVER={ODBC Driver 17 for SQL Server}', 
# IP ou nome do servidor.#
    'SERVER=DARKMATTER-PC\DARKMATER;', 
# Porta#
    'PORT=1433;', 
# Banco que será utilizado.#
    'DATABASE=pythonSQL;', 
# Nome de usuário.#
    'UID=python;', 
# Senha/Token.#
    'PWD=123456'
)



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


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match!')      
    ])
    confirm = PasswordField('Confirm Password')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        if request.method == ['POST'] and form.validate():
            return render_template('register.html')
        return render_template('register.html', form=form)
    

if __name__ == '__main__':
    app.run(debug=True)