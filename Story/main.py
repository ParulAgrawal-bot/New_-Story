import sqlalchemy
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_wtf import form
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms.fields.simple import StringField, EmailField, SubmitField
from flask_wtf import FlaskForm
from flask_login import LoginManager


class Base(DeclarativeBase):
    pass


# Create the app
app = Flask(__name__)

db = SQLAlchemy(model_class=Base)
# Secret Key
app.config['SECRET_KEY'] = 'ehjebsbnsjkwnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# CREATE DATABASE
db.init_app(app)
# Create the login_manager
login_manager = LoginManager()
login_manager.init_app(app)


class Base(DeclarativeBase):
    pass


# CREATE TABLE IN DB
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


class MyForm(FlaskForm):
    name = StringField("name")
    email = EmailField("email")
    password = StringField("password")
    submit = SubmitField("Submit")


with app.app_context():
    db.create_all()


# Login manager user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User(name=name, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return "<h1>Looks like you are already registered</h1>"
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    form_to_log_in = MyForm()
    if form_to_log_in.validate_on_submit():
        user = User(title=request.form.get("title"), email=request.form.get("email"), password=request.form.get("password"))
        login_user(user=user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        return redirect(next or url_for('index'))
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory("../static", path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
