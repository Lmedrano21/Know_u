import os
import json
from flask import Flask
from extensions import db, login_manager, csrf, limiter
from models import User, Product, ProductImage
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'clave_secreta_know_u_desarrollo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///know_u.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    limiter.init_app(app)

    # Middleware de Seguridad Global
    @app.after_request
    def add_security_headers(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://unpkg.com https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; "
            "font-src 'self' https://fonts.gstatic.com https://unpkg.com data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://unpkg.com; "
            "worker-src blob:; "
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    # Registro de Blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.api import api_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

app = create_app()

def init_db():
    with app.app_context():
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

        if not Product.query.first():
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
                        for img_path in item['images']:
                            final_path = img_path if img_path.startswith('static/') else f"static/{img_path}"
                            db.session.add(ProductImage(product_id=p.id, image_url=final_path))
                    db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
