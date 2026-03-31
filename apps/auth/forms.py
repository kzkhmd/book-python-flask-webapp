from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    username = StringField(
        "ユーザー名", 
        validators=[
            DataRequired("ユーザー名は必須です。"),
            Length(min=1, max=30, message="ユーザー名は30文字以内で入力してください。"),
        ]
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ]
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
        ]
    )
    submit = SubmitField("新規登録")


class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ]
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
        ]
    )
    submit = SubmitField("ログイン")
