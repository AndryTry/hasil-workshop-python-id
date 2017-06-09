from flask import Blueprint, render_template, redirect, request, abort
from pos.models import db
from pos.models.products import Products

bp = Blueprint("products", __name__)


@bp.route("/products")
def product_list():
    """List product"""
    product = Products.query.all()

    return render_template('product/list.html', products=product)


@bp.route("/products/add", methods=["POST", "GET"])
def product_add():
    """Add product"""
    if request.method == "GET":
        return render_template('product/form_add.html')

    name = request.form["name"]
    price = request.form["price"]
    stock = request.form['stock']

    product = Products()
    product.name = name
    product.price = price
    product.stock = stock
    db.session.add(product)
    db.session.commit()

    return redirect("/products")


@bp.route("/products/update", methods=["POST", "GET"])
def product_update():
    """Update product"""
    product_id = request.args['id']

    if request.method == "GET":
        product = Products.query.filter_by(id=product_id).first()

        if product:
            return render_template('product/form_edit.html', product=product)
        else:
            abort(404)

    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    product = Products.query.filter_by(id=product_id).first()

    if product:
        product.name = name
        product.price = price
        product.stock = stock
        db.session.add(product)
        db.session.commit()

    return redirect("/products")


@bp.route("/products/delete")
def product_delete():
    """Delete product"""
    product_id = request.args['id']

    product = Products.query.filter_by(id=product_id).first()

    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect("/products")
