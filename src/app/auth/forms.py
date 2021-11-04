from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    name = StringField('Nombre de usuario', validators=[DataRequired(), Length(max=64)])
    email = StringField('Correo electronico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8)])
    captcha = RecaptchaField()
    submit = SubmitField('Enviar')


class LogInForm(FlaskForm):
    email = StringField('Correo electronico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuerdame')
    submit = SubmitField('Enviar')