from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

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
    return render_template('contact.html')

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
        
        flash("お問い合わせありがとうございました！")
        return redirect(url_for('contact_complete'))
    
    return render_template('contact_complete.html')

with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello-endpoint', name='world'))
    print(url_for('show_name', name='Ichiro', page='1'))
