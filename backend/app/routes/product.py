from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Member, Product, Like
from datetime import datetime, timezone

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

    user_likes = Like.query.filter_by(
        user_id=current_user_id,
        target_type='product'
    ).all()

    liked_products_ids = {like.target_id for like in user_likes}

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
        'is_bargain': p.is_bargain,
        'likes_count': p.likes_count or 0,
        'is_liked': p.id in liked_products_ids
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
    
@product.route('/api/product/<int:product_id>/like', methods=['POST'])
@jwt_required()
def like_product(product_id):
    current_user_id = get_jwt_identity()

    product = Product.query.get(product_id)
    if not product:
        return jsonify({ 'error': 'Product not fount' }), 404
    
    existing_like = Like.query.filter_by(
        user_id=current_user_id,
        target_type='product',
        target_id=product_id
    ).first()

    if existing_like:
        db.session.delete(existing_like)
        product.likes_count = max(0, product.likes_count - 1)
        db.session.commit()
        return jsonify({
            'liked': False,
            'likes_count': product.likes_count,
            'message': 'Like removed'
        }), 200
    
    new_like = Like(
        user_id=current_user_id,
        target_type='product',
        target_id=product_id,
        created_at=datetime.now(timezone.utc)
    )

    db.session.add(new_like)
    product.likes_count = product.likes_count + 1 if product.likes_count else 1
    db.session.commit()

    return jsonify({
        'liked': True,
        'likes_count': product.likes_count,
        'message': 'Product liked'
    }), 201

@product.route('/api/product/<int:product_id>/like/status', methods=['GET'])
@jwt_required()
def check_like_status(product_id):
    current_user_id = get_jwt_identity()

    product = Product.query.get(product_id)
    if not product:
        return jsonify({ 'error': 'Product not fount' }), 404
    
    is_liked = Like.query.filter_by(
        user_id=current_user_id,
        target_type='product',
        target_id=product_id
    ).first() is not None

    return jsonify({
        'liked': is_liked,
        'likes_count': product.likes_count or 0
    }), 200

@product.route('/api/user/liked-products', methods=['GET'])
@jwt_required()
def get_liked_products():
    current_user_id = get_jwt_identity()

    liked_products = db.session.query(Product).join(
        Like,
        (Like.target_id == Product.id) & (Like.target_type == 'product')
    ).filter(
        Like.user_id == current_user_id
    ).all()

    products_data =[{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'images': p.images,
        'cost': p.cost,
        'category': p.category,
        'town': p.town,
        'date_pub': p.date_pub,
        'is_active': p.is_active,
        'is_bargain': p.is_bargain,
        'likes_count': p.likes_count or 0
    } for p in liked_products]

    return jsonify({
        'liked_products': products_data,
        'count': len(products_data)
    }), 200