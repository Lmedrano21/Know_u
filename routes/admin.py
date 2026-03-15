from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import Product, ProductImage, Order, OrderItem, User, GeneratedDesign

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@admin_bp.route('/admin/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        
        new_product = Product(name=name, price=price, category=category, description=description)
        db.session.add(new_product)
        db.session.commit()
        
        if image_url:
            img = ProductImage(product_id=new_product.id, image_url=image_url)
            db.session.add(img)
            db.session.commit()
            
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin_product.html', action='Agregar')

@admin_bp.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.category = request.form.get('category')
        product.description = request.form.get('description')
        image_url = request.form.get('image_url')
        if image_url:
            if product.images:
                product.images[0].image_url = image_url
            else:
                img = ProductImage(product_id=product.id, image_url=image_url)
                db.session.add(img)
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    image_url = product.images[0].image_url if product.images else ''
    return render_template('admin_product.html', action='Editar', product=product, image_url=image_url)

@admin_bp.route('/admin/delete/<int:product_id>')
@login_required
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    ProductImage.query.filter_by(product_id=product.id).delete()
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('admin_orders.html', orders=orders)

@admin_bp.route('/admin/order/<int:order_id>')
@login_required
@admin_required
def admin_order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin_order_detail.html', order=order)

@admin_bp.route('/admin/order/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def admin_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'paid', 'shipped']:
        order.status = new_status
        db.session.commit()
        flash('Estado del pedido actualizado.', 'success')
    else:
        flash('Estado inválido.', 'error')
    return redirect(url_for('admin.admin_order_detail', order_id=order.id))

@admin_bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/admin/delete_user/<int:user_id>')
@login_required
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('No puedes eliminar un usuario administrador.', 'error')
        return redirect(url_for('admin.admin_users'))
    GeneratedDesign.query.filter_by(user_id=user.id).delete()
    orders = Order.query.filter_by(user_id=user.id).all()
    for o in orders:
        OrderItem.query.filter_by(order_id=o.id).delete()
        db.session.delete(o)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado permanentemente.', 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/community')
@login_required
@admin_required
def admin_community():
    designs = GeneratedDesign.query.order_by(GeneratedDesign.date_created.desc()).all()
    return render_template('admin_community.html', designs=designs)

@admin_bp.route('/admin/delete_design/<int:design_id>')
@login_required
@admin_required
def admin_delete_design(design_id):
    design = GeneratedDesign.query.get_or_404(design_id)
    db.session.delete(design)
    db.session.commit()
    flash('Diseño IA eliminado.', 'success')
    return redirect(url_for('admin.admin_community'))
