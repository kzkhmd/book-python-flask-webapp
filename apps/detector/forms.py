from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField

class ImageUploadForm(FlaskForm):
    image = FileField(
        "画像ファイル",
        validators=[
            FileRequired(message="画像ファイルを選択してください。"),
            FileAllowed(["jpg", "jpeg", "png"], message="jpg, jpeg, png形式の画像ファイルを選択してください。")
        ]
    )
    submit = SubmitField("アップロード")
