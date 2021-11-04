from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, Length


class LocationForm(FlaskForm):
    street = StringField('Calle', validators=[DataRequired(), Length(max=80)])
    house_number = StringField('Número de casa', validators=[DataRequired(), Length(max=10)])
    zip_code = StringField('Código Postal', validators=[DataRequired(), Length(min=5, max=5)])
    phone_number = StringField('Número de teléfono', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Guardar')


class ConfigurationForm(FlaskForm):
    name = StringField('Nombre de usuario')
    email = StringField('Correo electrónico', validators=[Email()])
    password = PasswordField('Contraseña')
    submit = SubmitField('Guardar')