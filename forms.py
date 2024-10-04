from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import IntegerField, FileField, SubmitField, EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class TemplateForm(FlaskForm):
    file = FileField("Upload an Image", validators=[DataRequired(),
                                                    FileAllowed(["jpg", "png", "jpeg"], "Images Only!")])
    num_colors = IntegerField("Number of Colors", validators=[DataRequired(),
                                                              NumberRange(min=1, message="Number must be at least 1")])
    submit = SubmitField("Process Image")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
