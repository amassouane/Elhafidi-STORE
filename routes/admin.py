from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import json
from models import Product, Order, db
from config import Config

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def dashboard():
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).filter(Order.status == 'Livrée').scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           total_orders=total_orders, 
                           total_products=total_products, 
                           total_revenue=total_revenue,
                           recent_orders=recent_orders)

@admin_bp.route('/products')
@login_required
def manage_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/manage_products.html', products=products)

@admin_bp.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        stock = int(request.form.get('stock', 0))
        
        sizes_raw = request.form.get('sizes', '')
        colors_raw = request.form.get('colors', '')
        
        sizes = [s.strip() for s in sizes_raw.split(',')] if sizes_raw else []
        colors = [c.strip() for c in colors_raw.split(',')] if colors_raw else []
        
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                os.makedirs(Config.UPLOADED_PHOTOS_DEST, exist_ok=True)
                file.save(os.path.join(Config.UPLOADED_PHOTOS_DEST, filename))
                image_url = 'images/' + filename
                
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            sizes=json.dumps(sizes),
            colors=json.dumps(colors),
            stock=stock,
            image_url=image_url,
            is_featured='is_featured' in request.form
        )
        db.session.add(product)
        db.session.commit()
        flash('Produit ajouté avec succès.', 'success')
        return redirect(url_for('admin.manage_products'))
        
    return render_template('admin/add_product.html')

@admin_bp.route('/product/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé.', 'success')
    return redirect(url_for('admin.manage_products'))

@admin_bp.route('/product/update_stock/<int:id>', methods=['POST'])
@login_required
def update_product_stock(id):
    product = Product.query.get_or_404(id)
    new_stock = request.form.get('stock', type=int)
    if new_stock is not None and new_stock >= 0:
        product.stock = new_stock
        db.session.commit()
        flash('Quantité mise à jour avec succès.', 'success')
    else:
        flash('Quantité invalide.', 'danger')
    return redirect(url_for('admin.manage_products'))

@admin_bp.route('/orders')
@login_required
def manage_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/manage_orders.html', orders=orders)

@admin_bp.route('/order/update_status/<int:id>', methods=['POST'])
@login_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    status = request.form.get('status')
    if status in ['En attente', 'Confirmée', 'Livrée', 'Annulée']:
        order.status = status
        db.session.commit()
        flash('Statut de la commande mis à jour.', 'success')
    return redirect(url_for('admin.manage_orders'))
