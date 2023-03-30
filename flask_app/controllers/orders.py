from flask_app import app
from flask import render_template, session, redirect, request, url_for


@app.route("/products")
def home():
    from flask_app.models.order import Order
    orders = Order.get_all()
    return render_template("products.html", orders=orders)


@app.route("/details")
def details():
    return render_template("details.html")


@ app.route("/finished/check_out")
def after_checkout():
    return render_template("after_checkout.html")


@app.route("/orders/create_order", methods=["POST"])
def create_order():
    from flask_app.models.order import Order

    data = {
        "flavor": request.form["flavor"],
        "price": request.form["price"],
        "image": request.form["image"],
        "quantity": request.form["quantity"]
    }
    Order.save(data)
    return redirect("/orders")


@app.route("/orders")
def orders():
    from flask_app.models.order import Order

    orders = Order.get_all()
    return render_template("create_order.html", orders=orders)


@ app.route("/delete_order/<int:id>", methods=["POST"])
def delete_order(id):
    from flask_app.models.order import Order
    data = {"id": id}
    Order.delete(data)
    return redirect("/checkout")
