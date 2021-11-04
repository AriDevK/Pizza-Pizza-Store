from flask import render_template, flash, redirect, url_for, session, abort
from flask_login import current_user, login_required
from secrets import token_hex

from . import cart_bp
from app import db
from app.models import Menu, Sell


@cart_bp.route('/cart')
def cart():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    elif 'cart' not in session:
        session['cart'] = {}

    
    prices = {k : Menu.query.filter_by(name=k).first().price for k in session['cart'].keys()}
    return render_template('cart/cart.html', cart=session['cart'], prices=prices)


@cart_bp.route('/cart/<string:item>')
@cart_bp.route('/cart/<string:item>/<int:quantity>')
def add_cart(item='', quantity=1):
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    
    if item != '':
        if "cart" in session:
            cart = session["cart"]
            if item in cart.keys():
                cart[item] += quantity
            else:
                cart[item] = quantity

            session["cart"] = cart

        else:
            session["cart"] = {item : quantity}

    flash('Producto añadido correctamente.', 'dark')
    return redirect(url_for('cart.cart'))


@cart_bp.route('/cart/remove/<string:item>')
@login_required
def remove_cart(item):
    cart = session.get('cart')

    if cart and item in cart.keys():
        cart.pop(item)
        session['cart'] = cart
        return redirect(url_for('cart.cart'))

    return abort(404)


@cart_bp.route('/cart/buy')
@login_required
def buy_cart():
    prices = {k : Menu.query.filter_by(name=k).first().price for k in session['cart'].keys()}
    return render_template('cart/buy.html', current_user=current_user, cart=session['cart'], prices=prices)


@cart_bp.route('/cart/success', methods = ['GET', 'POST'])
@login_required
def cart_success():
    while True:
        sell_number = f'{current_user.street[:2]}-{token_hex(5)}'
        if not Sell.query.filter_by(sell_number=sell_number).first():
            user_id = current_user.id
            final_price = sum([quantity * Menu.query.filter_by(name=product).first().price for product, quantity in session['cart'].items()])
            
            sell = Sell(user_id, sell_number, final_price)
            db.session.add(sell)
            db.session.commit()
            session.pop('cart')
            break

    return render_template('cart/success.html')