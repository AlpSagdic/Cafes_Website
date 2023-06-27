from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired, URL, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOU_CAN_WRITE_WHATEVER_YOU_WANT'
Bootstrap(app)

#Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Configure Table
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cafe_url = db.Column(db.String(500), unique=True, nullable=False)
    img_url = db.Column(db.String(500), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_wc = db.Column(db.String(10), nullable=False, default=True)
    has_wifi = db.Column(db.String(10), nullable=False, default=True)
    has_sockets = db.Column(db.String(10), nullable=False, default=True)


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=False, nullable=False)
    user_email = db.Column(db.String(100), unique=False, nullable=False)
    message_subject = db.Column(db.String(100), unique=False, nullable=False)
    message = db.Column(db.String(5000), unique=False, nullable=False)

#We used it to create the database.
#with app.app_context():
#   db.create_all()


#Forms
class CafeForm(FlaskForm):
    name = StringField("Cafe's Name", validators=[DataRequired()])
    cafe_url = StringField("Cafe's URL", validators=[DataRequired(), URL()])
    img_url = StringField("Images' URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe's Location", validators=[DataRequired()])
    has_wc = SelectField("Does the cafe have a wc?", choices=["❌", "✅"], validators=[DataRequired()])
    has_wifi = SelectField("Does the cafe have a wifi?", choices=["❌", "✅", "✅✅", "✅✅✅"], validators=[DataRequired()])
    has_sockets = SelectField("Does the cafe have a sockets?", choices=["❌", "✅", "✅✅", "✅✅✅"], validators=[DataRequired()])
    submit = SubmitField("Submit")


class ContactForm(FlaskForm):
    user_name = StringField("What's Your Name?", validators=[DataRequired()])
    user_email = EmailField("What's Your Email Address?", validators=[Email()])
    message_subject = StringField("What's Your Subject?", validators=[DataRequired()])
    message = StringField("What's Your Message?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", all_cafes=all_cafes)


@app.route("/create-cafe", methods=["GET", "POST"])
def create_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            cafe_url=form.cafe_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_wc=form.has_wc.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("create_cafe.html", form=form)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user_info = UserInfo(
            user_name=form.user_name.data,
            user_email=form.user_email.data,
            message_subject=form.message_subject.data,
            message=form.message.data
        )
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("contact.html", form=form)


@app.route("/cafes", methods=["GET", "POST"])
def cafes():
    all_cafes = db.session.query(Cafe).all()
    len_cafe = len(all_cafes)
    return render_template("cafes.html", all_cafes=all_cafes, lenght=len_cafe)


if __name__ == "__main__":
    app.run(debug=True)
