from collections import namedtuple
from flask import Blueprint, render_template, request, redirect
from pos.models.transactions import Transactions
from pos.models.transactions_products import TransactionProducts
from pos.models import db

bp = Blueprint("transaction", __name__)


@bp.route("/transaction")
def transaction_list():
    transactions = Transactions.query.all()
    return render_template("/transaction/list.html", transactions=transactions)


@bp.route("/transaction/add", methods=["POST", "GET"])
def transaction_add():
    if request.method == "GET":
        return render_template("/transaction/form_add.html")

    products = request.form.getlist("products")
    products_qty = request.form.getlist("products_qty")

    transaction = Transactions()
    db.session.add(transaction)
    db.session.flush()

    Product = namedtuple('Product', ['id', 'qty'])
    for product in map(Product._make, zip(products, products_qty)):
        transaction_product = TransactionProducts()
        transaction_product.transaction_id = transaction.id
        transaction_product.product_id = int(product.id)
        transaction_product.product_qty = int(product.qty)

        db.session.add(transaction_product)
        db.session.flush()

    db.session.commit()

    return redirect("/transaction")
