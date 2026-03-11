import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración de la Aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_know_u_desarrollo' # ¡Cambiar en producción!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///know_u.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- MODELOS (Base de Datos) ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False) # String para mantener formato "$225.00" del frontend actual
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_trending = db.Column(db.Boolean, default=False)
    # Relación con imágenes
    images = db.relationship('ProductImage', backref='product', lazy=True)

    def to_dict(self):
        """Serializa el objeto para la API JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'isTrending': self.is_trending,
            'images': [img.image_url for img in self.images]
        }

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DECORADOR ADMIN ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403) # Prohibido
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS DE VISTAS (HTML) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/knowu-chat')
def knowu_chat():
    return render_template('knowu_chat.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product/<int:product_id>')
def product_details(product_id):
    # Pasamos el ID al template por si se necesita renderizado híbrido
    return render_template('ProductDetails.html', product_id=product_id)

@app.route('/cart')
def cart():
    return render_template('cartPage.html')

@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/profile')
@login_required
def profile():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    return render_template('profile.html', orders=user_orders)

# --- RUTAS DE ADMINISTRACIÓN ---

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_product.html', action='Agregar')

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.category = request.form.get('category')
        product.description = request.form.get('description')
        
        # Actualizar imagen (lógica simple: actualiza la primera imagen si existe o crea una)
        image_url = request.form.get('image_url')
        if image_url:
            if product.images:
                product.images[0].image_url = image_url
            else:
                img = ProductImage(product_id=product.id, image_url=image_url)
                db.session.add(img)
        
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('admin_dashboard'))
    
    image_url = product.images[0].image_url if product.images else ''
    return render_template('admin_product.html', action='Editar', product=product, image_url=image_url)

@app.route('/admin/delete/<int:product_id>')
@login_required
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    # Eliminar imágenes asociadas primero
    ProductImage.query.filter_by(product_id=product.id).delete()
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('admin_dashboard'))

# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('Password') # Name coincide con el input HTML
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña inválidos.', 'error')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('Password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('El correo electrónico ya está registrado.', 'error')
            return redirect(url_for('signup'))
        
        new_user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            first_name=fname,
            last_name=lname
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
        
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- API ENDPOINTS (Para JavaScript) ---
# Esto permite que tu JS actual siga funcionando pero obteniendo datos reales

@app.route('/api/products')
def api_products():
    all_products = Product.query.all()
    return jsonify([p.to_dict() for p in all_products])

@app.route('/api/products/<int:product_id>')
def api_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/api/checkout', methods=['POST'])
@login_required
def api_checkout():
    data = request.get_json()
    cart_items = data.get('items', [])
    
    if not cart_items:
        return jsonify({'success': False, 'message': 'El carrito está vacío'}), 400
        
    try:
        # Crear orden inicial
        new_order = Order(user_id=current_user.id, total_price=0)
        db.session.add(new_order)
        db.session.commit() # Commit para obtener el ID de la orden
        
        total = 0.0
        
        for item in cart_items:
            product = Product.query.get(item['id'])
            if product:
                # Convertir precio "$225.00" a float 225.00
                price_clean = float(product.price.replace('$', '').replace(',', ''))
                item_total = price_clean * item['quantity']
                total += item_total
                
                order_item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=item['quantity'], price=price_clean)
                db.session.add(order_item)
        
        # Sumar envío fijo (debe coincidir con frontend)
        total += 70.00
        new_order.total_price = total
        db.session.commit()
        
        return jsonify({'success': True, 'order_id': new_order.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/orders/<int:order_id>')
@login_required
def api_get_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Seguridad: Solo el dueño de la orden puede verla
    if order.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    return jsonify({
        'id': order.id,
        'date': order.date.strftime('%d/%m/%Y'),
        'total_price': f"{order.total_price:.2f}",
        'items': [{
            'name': item.product.name,
            'quantity': item.quantity,
            'price': f"{item.price:.2f}"
        } for item in order.items]
    })

# --- INICIALIZACIÓN Y SEEDER ---

def init_db():
    """Crea la BD y carga datos iniciales desde el JSON si está vacía"""
    with app.app_context():
        # --- MIGRACIÓN AUTOMÁTICA: Detectar y corregir falta de columna is_admin ---
        inspector = inspect(db.engine)
        if inspector.has_table("user"):
            columns = [col['name'] for col in inspector.get_columns("user")]
            if "is_admin" not in columns:
                print("Migrando base de datos: Añadiendo columna 'is_admin'...")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
                    conn.commit()

        db.create_all()
        
        # Crear admin si no existe
        admin_email = 'admin@knowu.com'
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario administrador creado: admin@knowu.com / admin123")

        if not Product.query.first():
            print("Inicializando base de datos con productos.json...")
            json_path = os.path.join(app.static_folder, 'json', 'products.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        p = Product(
                            id=item['id'],
                            name=item['name'],
                            price=item['price'],
                            category=item['category'],
                            description=item['description'],
                            is_trending=item.get('isTrending', False)
                        )
                        db.session.add(p)
                        db.session.commit()
                        
                        # Manejo de imágenes: Ajustamos la ruta para Flask static
                        for img_path in item['images']:
                            # Aseguramos que la ruta apunte a static si no lo hace
                            final_path = img_path
                            if not final_path.startswith('static/'):
                                final_path = f"static/{img_path}"
                            
                            db.session.add(ProductImage(product_id=p.id, image_url=final_path))
                    db.session.commit()
                    print("Base de datos poblada exitosamente.")
            else:
                print(f"Advertencia: No se encontró {json_path}")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
