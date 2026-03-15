from flask import Blueprint, render_template, request
from models import GeneratedDesign, Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/knowu-chat')
def knowu_chat():
    return render_template('knowu_chat.html')

@main_bp.route('/products')
def products():
    return render_template('products.html')

@main_bp.route('/community')
def community():
    published_designs = GeneratedDesign.query.filter_by(status='published').order_by(GeneratedDesign.date_created.desc()).all()
    return render_template('community.html', designs=published_designs)

@main_bp.route('/create')
def create_studio():
    return render_template('create.html')

@main_bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('ProductDetails.html', product_id=product_id, product=product)
