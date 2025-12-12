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
    
    all_products = Product.query.filetr_by(owner_id=current_user_id).all()
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