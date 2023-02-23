from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, URL
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
    website = URLField('Enter Your Website', validators=[DataRequired(), URL()], render_kw={"class": "form-control mb-6", "style": "width: 400px; margin: 10px;" })
    submit = SubmitField('Shorten URL', render_kw={"class": "btn btn-primary mb-4"})
    
with app.app_context():
    db.create_all()
    

def generate_code(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) 

 
@app.route("/", methods=['GET', 'POST'])
def home():
    form = UrlForm()
    
    if form.validate_on_submit():
        long_url = form.website.data
        if not long_url.startswith('http'):
            long_url = 'http://' + long_url
        url = db.session.query(Url).filter_by(long_url=long_url).first()
        if url:
            
            return redirect(url_for('result', short_url=url.short_url) )
        else:
            short_url = generate_code()
            url = Url(long_url=long_url, short_url=short_url)
            db.session.add(url)
            db.session.commit()
            return redirect(url_for('result', short_url=url.short_url))
    
    return render_template('index.html', form=form)


@app.route("/result")
def result():
    short_url = request.args.get("short_url")
    return render_template('result.html', short_url=short_url)




if __name__=="__main__":
    app.run(debug=True)

