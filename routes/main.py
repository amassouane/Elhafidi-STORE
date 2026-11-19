from flask import Blueprint, render_template
from models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch latest 4 products for "Nouveautés"
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(4).all()
    # Featured products or promotions
    featured_products = Product.query.filter_by(is_featured=True).limit(4).all()
    return render_template('index.html', latest_products=latest_products, featured_products=featured_products)
