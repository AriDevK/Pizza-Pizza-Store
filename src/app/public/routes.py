from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from . import public_bp
from app import db, bcrypt
from app.models import Menu
from app.auth.models import User
from app.auth.routes import logout
from .forms import LocationForm, ConfigurationForm


@public_bp.route('/')
def index():
    user = None
    menu = Menu.query.filter_by(type='pizza').all()

    if current_user.is_authenticated:
        user = current_user

    return render_template('public/index.html', current_user = user, menu = menu)


@public_bp.route('/menu')
def menu():
    user = None
    menu = Menu.query.filter_by(type='pizza').all()
    prices = {product.name : Menu.query.filter_by(name=product.name).first().price for product in menu}

    if current_user.is_authenticated:
        user = current_user

    return render_template('public/menu.html', current_user = user, menu = menu, prices=prices)


@public_bp.route('/complements')
def complements():
    user = None
    menu = Menu.query.filter_by(type='drink').all()
    menu += Menu.query.filter_by(type='complement').all()
    prices = {k.name : Menu.query.filter_by(name=k.name).first().price for k in menu}

    if current_user.is_authenticated:
        user = current_user

    return render_template('public/complements.html', current_user = user, menu = menu, prices=prices)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')


@public_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    location_form = LocationForm()
    configuration_form = ConfigurationForm()

    if location_form.submit.data and location_form.validate():
        user.street = location_form.street.data
        user.house_number = location_form.house_number.data
        user.zip_code = location_form.zip_code.data
        user.phone_number = location_form.phone_number.data
        db.session.add(user)
        db.session.commit()
        flash('Perfil actualizado correctamente', 'dark')

    elif configuration_form.submit.data and configuration_form.validate():
        name = configuration_form.name.data
        email = configuration_form.email.data
        password = configuration_form.password.data

        if user.name == name and user.email == email and password == '':
            flash('Ningún dato ha sido modificado, por favor verifique sus cambios.', 'warning')
            return redirect(url_for('public.profile'))

        elif User.query.filter_by(email = email).first() and user.email != email:
            flash(f'El correo electrónico {email} ya esta en uso, por favor seleccione otro.', 'warning')
            return(redirect(url_for('public.profile')))

        else:
            user.name = user.name if name == '' else name
            user.email = user.email if email == '' else email
            user.password = user.password if password == '' else bcrypt.generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            logout()
            flash('Datos actualizados correctamente (Campos en blanco se mantendran con los mismos datos.)', 'dark')
            return redirect(url_for('public.index'))

    return render_template('public/profile.html', current_user=user, location_form=location_form, configuration_form=configuration_form)