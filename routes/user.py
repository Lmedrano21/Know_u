from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import User, Order, GeneratedDesign, OrderItem, Product, ProductImage
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    user_designs = GeneratedDesign.query.filter_by(user_id=current_user.id).order_by(GeneratedDesign.date_created.desc()).all()
    
    design_ids = [d.id for d in user_designs]
    sold_items = []
    total_earnings = 0.0
    total_sales_count = 0
    
    if design_ids:
        sold_items = OrderItem.query.join(Order).filter(
            OrderItem.design_id.in_(design_ids),
            Order.status.in_(['paid', 'shipped'])
        ).all()
        
        total_sales_count = sum(item.quantity for item in sold_items)
        total_earnings = total_sales_count * 10.0
        
    return render_template('profile.html', 
                           orders=user_orders, 
                           designs=user_designs, 
                           sold_items=sold_items, 
                           total_earnings=total_earnings,
                           total_sales_count=total_sales_count)

@user_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    success_msg = None
    error_msg = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            fname = request.form.get('first_name', '').strip()
            lname = request.form.get('last_name', '').strip()
            new_email = request.form.get('email', '').strip().lower()

            if not fname or not new_email:
                error_msg = 'El nombre y el correo son obligatorios.'
            else:
                existing = User.query.filter_by(email=new_email).first()
                if existing and existing.id != current_user.id:
                    error_msg = 'Ese correo ya está en uso por otra cuenta.'
                else:
                    current_user.first_name = fname
                    current_user.last_name = lname
                    current_user.email = new_email
                    db.session.commit()
                    success_msg = '¡Datos personales actualizados con éxito!'

        elif action == 'change_password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            if not check_password_hash(current_user.password, current_password):
                error_msg = 'Tu contraseña actual no es correcta.'
            elif len(new_password) < 8:
                error_msg = 'La nueva contraseña debe tener al menos 8 caracteres.'
            elif new_password != confirm_password:
                error_msg = 'Las contraseñas nuevas no coinciden.'
            else:
                current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                db.session.commit()
                success_msg = '¡Contraseña cambiada con éxito!'

    return render_template('settings.html', success_msg=success_msg, error_msg=error_msg)

@user_bp.route('/creator/<int:user_id>')
def public_profile(user_id):
    creator = User.query.get_or_404(user_id)
    public_designs = GeneratedDesign.query.filter_by(user_id=creator.id, status='published').order_by(GeneratedDesign.date_created.desc()).all()
    
    total_likes_received = sum(len(d.likes) for d in public_designs)
    
    design_ids = [d.id for d in public_designs]
    total_sales_count = 0
    if design_ids:
        sales = OrderItem.query.join(Order).filter(
            OrderItem.design_id.in_(design_ids),
            Order.status.in_(['paid', 'shipped'])
        ).all()
        total_sales_count = sum(item.quantity for item in sales)
    
    return render_template('public_profile.html', 
                           creator=creator, 
                           designs=public_designs, 
                           total_likes_received=total_likes_received,
                           total_sales_count=total_sales_count)
