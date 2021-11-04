import datetime
from flask import render_template, flash, redirect, url_for, Markup, session
from flask_login.utils import login_required, login_user, logout_user, current_user

from . import auth_bp
from .forms import LogInForm, SignUpForm
from .models import User

from app import db, bcrypt, login_manager


@auth_bp.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()

    if current_user.is_authenticated:
        flash('not anonymous', 'warning')
        return redirect(url_for('public.index'))

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')

        if User.query.filter_by(email = email).first():
            flash(Markup(f'El correo <b>{email}</b ya esta en uso.'), 'danger')
        
        else:
            created_at = datetime.datetime.now()
            user = User(name=name, email=email, password=hashed_password, created_at=created_at)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Usuario creado correctamente.', 'dark')
            return redirect(url_for('public.index'))

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LogInForm()

    if current_user.is_authenticated:
        flash('not anonymous', 'warning')
        return redirect(url_for('public.index'))

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        
        if user:
            password = form.password.data

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('public.index'))

            else:
                flash('Contraseña incorrecta', 'danger')

        else:
            flash(Markup(f'Ya existe una cuenta con el correo <b>{email}</b> asociado.'), 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('cart', None)
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)