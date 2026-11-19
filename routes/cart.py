from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import Product, Order, OrderItem, db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item_data in cart.items():
        product = Product.query.get(item_data['product_id'])
        if product:
            subtotal = product.price * item_data['quantity']
            total += subtotal
            cart_items.append({
                'product': product,
                'cart_key': product_id,
                'quantity': item_data['quantity'],
                'size': item_data.get('size'),
                'color': item_data.get('color'),
                'subtotal': subtotal
            })
    
    shipping = 50 if total > 0 and total < 500 else 0
    grand_total = total + shipping
    
    return render_template('cart.html', cart_items=cart_items, total=total, shipping=shipping, grand_total=grand_total)

@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size')
    color = request.form.get('color')
    
    cart = session.get('cart', {})
    cart_key = f"{product_id}_{size}_{color}"
    
    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {
            'product_id': product_id,
            'quantity': quantity,
            'size': size,
            'color': color
        }
        
    session['cart'] = cart
    session.modified = True
    flash('Produit ajouté au panier avec succès!', 'success')
    return redirect(request.referrer or url_for('cart.view_cart'))

@cart_bp.route('/cart/update/<cart_key>', methods=['POST'])
def update_cart(cart_key):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    
    if cart_key in cart:
        if quantity > 0:
            cart[cart_key]['quantity'] = quantity
        else:
            cart.pop(cart_key)
            
        session['cart'] = cart
        session.modified = True
        
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/remove/<cart_key>', methods=['POST'])
def remove_from_cart(cart_key):
    cart = session.get('cart', {})
    if cart_key in cart:
        cart.pop(cart_key)
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Votre panier est vide.', 'warning')
        return redirect(url_for('shop.shop'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        
        total = 0
        order_items = []
        for cart_key, item_data in cart.items():
            product = Product.query.get(item_data['product_id'])
            if product:
                subtotal = product.price * item_data['quantity']
                total += subtotal
                order_item = OrderItem(
                    product_id=product.id,
                    quantity=item_data['quantity'],
                    size=item_data.get('size'),
                    color=item_data.get('color'),
                    unit_price=product.price
                )
                order_items.append(order_item)
                
        shipping = 50 if total > 0 and total < 500 else 0
        grand_total = total + shipping
        
        order = Order(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            customer_address=address,
            customer_city=city,
            total_price=grand_total,
            payment_method='Cash on Delivery'
        )
        for item in order_items:
            order.items.append(item)
            
        db.session.add(order)
        db.session.commit()
        
        session.pop('cart', None)
        flash('Votre commande a été confirmée avec succès! Paiement à la livraison.', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('checkout.html')
