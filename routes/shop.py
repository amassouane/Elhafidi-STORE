from flask import Blueprint, render_template, request
from models import Product
import json

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop():
    category = request.args.get('category')
    size = request.args.get('size')
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    if size:
        # Sizes are stored as JSON strings that resemble: ["S", "M", "L"]
        query = query.filter(Product.sizes.like(f'%"{size}"%'))
        
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())
        
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    products = pagination.items
    
    return render_template('shop.html', products=products, pagination=pagination, current_category=category, current_size=size, current_sort=sort)

@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    similar_products = Product.query.filter(Product.category == product.category, Product.id != product.id).limit(4).all()
    return render_template('product_detail.html', product=product, similar_products=similar_products)
