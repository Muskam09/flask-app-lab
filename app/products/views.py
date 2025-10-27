from flask import request, redirect, url_for, render_template
from app.products import products_bp

products = [
    {
        "id": 1,
        "name": "Iphone",
        "description": "A line of smartphones developed by Apple that runs on the iOS operating system"
    },
    {
        "id": 2,
        "name": "Ipad",
        "description": "The iPad is a brand of tablet computers from Apple, first introduced in 2010."
    },
    {
        "id": 3,
        "name": "MacBook",
        "description": "a line of Apple's laptop computers that run on the macOS operating system."
    },
    {
        "id": 4,
        "name": "Apple Watch",
        "description": "A smartwatch with fitness tracking, health monitoring, and telecommunication features that integrates with other Apple products and services."
    }
]

@products_bp.route("/")
def list_all():
  return render_template("products/products.html", products=products)

@products_bp.route("/<int:product_id>")
def get_product(product_id):
  product = next((p for p in products if p['id'] == product_id), None)
  if product is None:
      abort(404)
  return render_template("products/product_detail.html", product=product)