from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Product, Order, OrderItem, GeneratedDesign, Like, Comment, SavedDesign

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/products')
def api_products():
    all_products = Product.query.all()
    return jsonify([p.to_dict() for p in all_products])

@api_bp.route('/api/products/<int:product_id>')
def api_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@api_bp.route('/cart')
def cart():
    return render_template('cartPage.html')

@api_bp.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@api_bp.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    return render_template('order_success.html', order=order)

@api_bp.route('/api/checkout', methods=['POST'])
@login_required
def api_checkout():
    data = request.get_json()
    cart_items = data.get('items', [])
    
    if not cart_items:
        return jsonify({'success': False, 'message': 'El carrito está vacío'}), 400
        
    try:
        new_order = Order(user_id=current_user.id, total_price=0, status='pending')
        db.session.add(new_order)
        db.session.commit()
        
        total = 0.0
        for item in cart_items:
            if item.get('type') == 'custom':
                design_id = item.get('designId')
                if not design_id:
                    try:
                        design_id = int(str(item.get('id')).replace('custom_', ''))
                    except ValueError:
                        design_id = None
                
                price_clean = float(item['price'])
                item_total = price_clean * item['quantity']
                total += item_total
                
                order_item = OrderItem(order_id=new_order.id, design_id=design_id, quantity=item['quantity'], price=price_clean)
                db.session.add(order_item)
            else:
                product = Product.query.get(item['id'])
                if product:
                    price_clean = float(product.price.replace('$', '').replace(',', ''))
                    item_total = price_clean * item['quantity']
                    total += item_total
                    order_item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=item['quantity'], price=price_clean)
                    db.session.add(order_item)
        
        total += 70.00
        new_order.total_price = total
        db.session.commit()
        return jsonify({'success': True, 'order_id': new_order.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>')
@login_required
def api_get_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    return jsonify({
        'id': order.id,
        'date': order.date.strftime('%d/%m/%Y'),
        'total_price': f"{order.total_price:.2f}",
        'items': [{
            'name': item.product.name if item.product else "Diseño IA Custom",
            'quantity': item.quantity,
            'price': f"{item.price:.2f}"
        } for item in order.items]
    })

@api_bp.route('/api/generate_design', methods=['POST'])
@login_required
@limiter.limit("10 per day")
def api_generate_design():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'success': False, 'message': 'El prompt es requerido'}), 400
    mock_url = 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
    return jsonify({'success': True, 'image_url': mock_url, 'message': '¡Diseño generado con éxito!'})

@api_bp.route('/api/save_wardrobe', methods=['POST'])
@login_required
def api_save_wardrobe():
    data = request.get_json()
    prompt = data.get('prompt')
    image_url = data.get('image_url')
    if not prompt or not image_url:
        return jsonify({'success': False, 'message': 'Faltan datos para guardar el diseño'}), 400
    try:
        new_design = GeneratedDesign(user_id=current_user.id, prompt=prompt, image_url=image_url, status='wardrobe')
        db.session.add(new_design)
        db.session.commit()
        return jsonify({'success': True, 'design_id': new_design.id, 'message': 'Guardado en tu armario'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/publish_design', methods=['POST'])
@login_required
def api_publish_design():
    data = request.get_json()
    design_id = data.get('design_id')
    if not design_id:
        return jsonify({'success': False, 'message': 'ID de diseño no proporcionado'}), 400
    try:
        design = GeneratedDesign.query.get(design_id)
        if not design or design.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'No encontrado o no autorizado'}), 404
        design.status = 'published'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Diseño publicado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/toggle_like', methods=['POST'])
@login_required
def api_toggle_like():
    data = request.get_json()
    design_id = data.get('design_id')
    design = GeneratedDesign.query.get_or_404(design_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, design_id=design.id).first()
    try:
        if existing_like:
            db.session.delete(existing_like)
            liked = False
        else:
            new_like = Like(user_id=current_user.id, design_id=design.id)
            db.session.add(new_like)
            liked = True
        db.session.commit()
        return jsonify({'success': True, 'liked': liked, 'likes_count': len(design.likes)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/toggle_save', methods=['POST'])
@login_required
def api_toggle_save():
    data = request.get_json()
    design_id = data.get('design_id')
    design = GeneratedDesign.query.get_or_404(design_id)
    existing_save = SavedDesign.query.filter_by(user_id=current_user.id, design_id=design.id).first()
    try:
        if existing_save:
            db.session.delete(existing_save)
            saved = False
        else:
            new_save = SavedDesign(user_id=current_user.id, design_id=design.id)
            db.session.add(new_save)
            saved = True
        db.session.commit()
        return jsonify({'success': True, 'saved': saved})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/add_comment', methods=['POST'])
@login_required
def api_add_comment():
    data = request.get_json()
    design_id = data.get('design_id')
    text = data.get('text', '').strip()
    if not design_id or not text:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
    try:
        design = GeneratedDesign.query.get_or_404(design_id)
        new_comment = Comment(user_id=current_user.id, design_id=design.id, text=text)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'success': True, 'comment': {'user': current_user.first_name, 'text': new_comment.text, 'date': new_comment.date_created.strftime('%d/%m/%Y %H:%M')}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
