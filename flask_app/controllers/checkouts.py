from flask_app.models.checkout import Checkout
from flask import request, redirect
from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask.json import JSONEncoder
import datetime
import json


@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    from flask_app.models.order import Order
    from flask_app.models.checkout import Checkout

    order_id = request.form.get("order_id")
    if not order_id:
        return "Invalid order ID", 400

    # Get the order from the database based on the order ID
    order = Order.get_by_id(order_id)
    if not order:
        return "Invalid order ID", 400

    # Remove the order from the cart
    cart = session.get("cart", {})
    if order_id in cart:
        del cart[order_id]
        session["cart"] = cart

        # Remove the checkout record associated with the order being removed from the cart
        Checkout.delete(order_id)

    return redirect("/checkout")

# ==================


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    from flask_app.models.order import Order
    order_id = request.form.get("order_id")
    # get the quantity from the form
    quantity = int(request.form.get("quantity"))
    print("order_id:", order_id)
    order = Order.get_by_id(order_id)
    print("order:", order)
    if not order:
        return "Invalid order ID", 400

    # Get the current cart from the session (or create an empty cart
    # if it doesn't exist)
    cart = session.get("cart", {})
    print("cart:", cart)
    # If the order is already in the cart, add the new quantity
    # to the existing quantity
    if order_id in cart:
        cart[order_id]["quantity"] += quantity
    else:
        cart[order_id] = {
            "flavor": order.flavor,
            "price": order.price,
            "quantity": int(quantity),
        }

    session["cart"] = cart

    flash("It has been added to your cart!")

    return redirect("/products")


@app.route("/checkout")
def checkout():
    from flask_app.models.order import Order
    user_id = session.get('user_id')
    cart = session.get("cart", {})
    orders = []
    total_price = 0
    for order_id, item in cart.items():
        order = Order.get_by_id(order_id)
        if order:
            order.quantity = item['quantity']
            order.flavor = item['flavor']
            order.price = item['price']
            # order.image = item['image']
            total_price += order.price * order.quantity
            orders.append(order)

    return render_template("checkout.html", orders=orders, total_price=total_price)
