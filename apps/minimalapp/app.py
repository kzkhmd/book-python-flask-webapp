import logging
import os
from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    make_response,
    session
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)

app.debug = True
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

app.logger.setLevel("DEBUG")

toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    return "Hello, Minimal App!"

@app.route('/hello/<name>',
           methods=['GET'],
           endpoint='hello-endpoint')
def hello(name):
    return f"Hello, {name}!"

@app.route('/name/<name>')
def show_name(name):
    return render_template('index.html', name=name)

@app.route('/contact')
def contact():
    response = make_response(render_template('contact.html'))
    response.set_cookie('flaskbook key', 'flaskbook value')
    session['username'] = 'flaskbook'
    return response

@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("ユーザー名は必須です。")
            is_valid = False
        if not email:
            flash("メールアドレスは必須です。")
            is_valid = False
        
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式が正しくありません。")
            is_valid = False
        
        if not description:
            flash("お問い合わせ内容は必須です。")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for('contact'))
        
        send_mail(
            email,
            "お問い合わせありがとうございます",
            "contact_mail",
            username=username,
            description=description
        )
        
        flash("お問い合わせありがとうございました！")
        return redirect(url_for('contact_complete'))
    
    return render_template('contact_complete.html')

def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(f"{template}.txt", **kwargs)
    msg.html = render_template(f"{template}.html", **kwargs)
    mail.send(msg)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello-endpoint', name='world'))
    print(url_for('show_name', name='Ichiro', page='1'))
