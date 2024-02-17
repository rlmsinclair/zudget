from flask import Flask, render_template, session, redirect, request, url_for, flash, jsonify
import csv
import flask_login
from flask_login import UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm

# graph generator
# from graph_gen import getPastImage, getPopularGraphs

imagePath = r"static/"

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
    balance = db.Column(db.Integer, nullable=False)
    transaction_history = db.Column(db.String(4096), nullable=False)


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
        new_user = User(email=email, password=hashed_password, balance=0, transaction_history='0,')
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
        return render_template('index.html')
    return render_template('home.html', balance=user.balance)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add_money():
    if request.method == 'POST':
        user = flask_login.current_user
        money_to_add = request.form['add']
        user.transaction_history = user.transaction_history + money_to_add + ','
        user.balance = user.balance + float(money_to_add)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw_money():
    if request.method == 'POST':
        user = flask_login.current_user
        money_to_withdraw = request.form['withdraw']
        user.transaction_history = user.transaction_history + "-" + money_to_withdraw + ','
        user.balance = user.balance - float(money_to_withdraw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('withdraw.html')


@app.route('/roulette')
def roulette():
    user = flask_login.current_user
    return render_template('roulette.html', balance=user.balance)


@app.route('/api/get_balance', methods=['GET'])
def get_balance():
    user = flask_login.current_user
    return jsonify({'balance': user.balance})


@app.route('/api/update_balance', methods=['POST'])
def update_balance():
    user = flask_login.current_user
    user.balance = request.json['new_balance']
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 200})

'''
@app.route("/info")
def info():

    # generate images
    pastImageName1 = "image1.png"
    user = flask_login.current_user
    print(user.transaction_history)
    pastData = []
    getPastImage(400, 200, pastData, "Past Earnings", imagePath + pastImageName1)
    

    # get data about popular stocks
    tickers = ['NVDA', 'AAPL', 'TSLA']
    data = getPopularGraphs(user.balance, tickers)

    
    
    return render_template(
        "info.html",
        image1=imagePath + pastImageName1,  
        image2=imagePath + "image2.jpg",
        image3=imagePath + "image3.jpg",
        image4=imagePath + "image4.jpg",
        text1=''.join([item + "\n" for item in data[0]]),
        text2=''.join([item + "\n" for item in data[1]]),
        text3=''.join([item + "\n" for item in data[2]]),
        )


@app.route('/save')
def save():
    pass
'''

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
