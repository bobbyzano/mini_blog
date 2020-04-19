from flask_wtf import Form, RecaptchaField
from wtforms import StringField, RadioField, SelectField, BooleanField, TextAreaField,PasswordField, DateField, validators, SubmitField, ValidationError


class RegisterForm(Form):
    email = StringField(u'Email', validators=
    [validators.input_required(), validators.Length(min=3, max=50)])

    username = StringField(u'Username', validators=
    [validators.input_required(), validators.length(min=3, max=50)])
    password = PasswordField(u'Password', [ validators.DataRequired()
    ])
    recaptcha = RecaptchaField()
#login form
class LoginForm(Form):
    
    email = StringField(u'Email', validators=[validators.input_required(), validators.Length(1, 64)])
    password = PasswordField(u'Password', validators=[validators.input_required()])
    remember_me = BooleanField(u'Keep me logged in')

class ContactForm(Form):
    name = StringField(u'Name', validators=[validators.input_required()])
    email = StringField(u'Email', validators=[validators.input_required(), validators.Email()])
    website = StringField(u'Website')
    subject = StringField(u'Subject', validators=[validators.input_required()])
    message = TextAreaField(u'Enter Message', validators=[validators.input_required()])
