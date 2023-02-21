from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
import random
import string


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlshort.db'
app.config['SQLAHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, nullable=False)
    
class UrlForm(FlaskForm):
    website = StringField('Enter Your Website', validators=[DataRequired()], render_kw={"class": "form-control mb-6", "style": "width: 400px; margin: 10px;" })
    submit = SubmitField('Shorten URL', render_kw={"class": "btn btn-primary mb-3"})
    
with app.app_context():
    db.create_all()
    

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) 

 
@app.route("/", methods=['GET', 'POST'])
def home():
    form = UrlForm()
    
    return render_template('index.html', form=form)

@app.route("/result")
def result():
    return render_template('result.html')


if __name__=="__main__":
    app.run(debug=True)

