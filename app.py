from flask import Flask, render_template, session, redirect, request, url_for, flash
import csv
import flask_login
from flask_login import UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms import StringField , PasswordField , SubmitField
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://doadmin:AVNS_JkvcfAiuwN-gsSf6K0c@app-784b9fa7-3b44-405e-9170-d80f0dd5e72d-do-user-14798294-0.c.db.ondigitalocean.com:25060/defaultdb?sslmode=require'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '1234'


@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Registration Form
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter_by(email=email).first():  # the query has returned a user
            flash("Email already in use, please log in or use a different email.")
            return redirect (url_for('register'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful !')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        is_valid = bcrypt.check_password_hash(user.password, password)
        if user and is_valid:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('login failed , check your username and password', 'danger')
    return render_template('login.html')


@app.route('/')
def home():
    user = flask_login.current_user
    if user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/save')
def save():
    pass

if __name__ == '__main__':
    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)


