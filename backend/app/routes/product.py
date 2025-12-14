from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Member, Product

product = Blueprint('product', __name__)

@product.route('/api/product/user', methods=['GET'])
@jwt_required()
def user_product():
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404
    
    all_products = Product.query.filter_by(owner_id=current_user_id).all()
    product_data = ([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'images': p.images,
        'cost': p.cost,
        'category': p.category,
        'town': p.town,
        'phone_number': p.phone_number,
        'date_pub': p.date_pub,
        'watchs': p.watchs,
        'is_active': p.is_active,
        'is_bargain': p.is_bargain
    } for p in all_products])

    return jsonify({ 'product_data': product_data })

@product.route('/api/products/get', methods=['GET'])
@jwt_required()
def get_products():
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404
    
    all_products = Product.query.all()
    all_products_data = [{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'images': p.images,
        'cost': p.cost,
        'category': p.category,
        'town': p.town,
        'phone_number': p.phone_number,
        'date_pub': p.date_pub,
        'watchs': p.watchs,
        'is_active': p.is_active,
        'is_bargain': p.is_bargain
    } for p in all_products]
    
    user_products = Product.query.filter_by(owner_id=current_user_id).all()
    user_product_data = ([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'images': p.images,
        'cost': p.cost,
        'category': p.category,
        'town': p.town,
        'phone_number': p.phone_number,
        'date_pub': p.date_pub,
        'watchs': p.watchs,
        'is_active': p.is_active,
        'is_bargain': p.is_bargain
    } for p in user_products])

    all_products_count = Product.query.all()

    print(len(all_products_count))

    return jsonify({
        'all_products': all_products_data,
        'user_products': user_product_data,
        'product_count': len(all_products_count),
        'user_product_count': len(user_products)
    })

@product.route('/api/product/new', methods=['POST'])
@jwt_required()
def new_product():
    current_user_id = get_jwt_identity()
    
    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404
    
    data = request.get_json()

    if not all([data.get('title'), data.get('category'), data.get('price'), data.get('description'), data.get('city'), data.get('phone')]):
        return jsonify({ 'error': 'Required fields empty'}), 400
    
    try:
        product = Product(
            owner_id=current_user_id,
            title=data.get('title'),
            description=data.get('description'),
            cost=data.get('price'),
            category=data.get('category'),
            town=data.get('city'),
            phone_number=data.get('phone')
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'message': 'New lsiting created successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({ 'error': f'Internal server error: {e}' }), 500