import os
import uuid
import mimetypes
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
from flask import Blueprint, current_app, request, jsonify, send_from_directory, abort, json
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Member, Product, Like
from datetime import datetime, timezone

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

def allowed_file(filename):
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def save_images(files):
    saved_filenames = []

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            
            file_ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
            
            if file_ext:
                filename = f"{uuid.uuid4().hex}.{file_ext}"
            else:
                filename = f"{uuid.uuid4().hex}" 
            
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            saved_filenames.append(filename)

    return saved_filenames

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
    
    if 'images' in request.files:
        files = request.files.getlist('images')

        if len(files) > 5:
            return jsonify({ 'error': 'Можно загрузить не более 5 изображений' }), 400

        try:
            image_filenames = save_images(files)
        except Exception as e:
            return jsonify({ 'error': f'Ошибка загрузки изображений: {str(e)}' }), 500
        
        title = request.form.get('title')
        category = request.form.get('category')
        price = request.form.get('price')
        description = request.form.get('description')
        city = request.form.get('city')
        phone = request.form.get('phone')
    else:
        data = request.get_json
        image_filenames = []
        title = data.get('title')
        category = data.get('category')
        price = data.get('price')
        description = data.get('description')
        city = data.get('city')
        phone = data.get('phone')

    if not all([title, category, price, description, city, phone]):
        return jsonify({ 'error': 'Required fileds empty' }), 400
    
    try:
        price_int = int(price)

        product = Product(
            owner_id=current_user_id,
            title=title,
            description=description,
            cost=price_int,
            category=category,
            town=city,
            phone_number=phone,
            images=image_filenames
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'message': 'New listing created successfully',
            'product_id': product.id,
            'images': image_filenames
        }), 201
    except ValueError:
        return jsonify({ 'error': 'Invalid price format' }), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({ 'error': f'Inrernal server error: {e}' }), 500

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

@product.route('/uploads/<path:filename>')
def uploaded_file(filename):
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            abort(404)
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            if filename.lower().endswith(('.jpg', '.jpeg')):
                mime_type = 'image/jpeg'
            elif filename.lower().endswith('.png'):
                mime_type = 'image/png'
            elif filename.lower().endswith('.gif'):
                mime_type = 'image/gif'
            elif filename.lower().endswith('.webp'):
                mime_type = 'image/webp'
            else:
                mime_type = 'application/octet-stream'
        
        print(f"Serving file: {filename}, MIME: {mime_type}, Size: {os.path.getsize(file_path)}")
        
        response = send_from_directory(upload_folder, filename)
        response.headers.set('Content-Type', mime_type)
        response.headers.set('Cache-Control', 'public, max-age=31536000')
        
        return response
        
    except NotFound:
        print(f"File not found in send_from_directory: {filename}")
        abort(404)
    except Exception as e:
        print(f"Error serving file {filename}: {e}")
        abort(500)

@product.route('/api/product/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404
    
    user_likes = Like.query.filter_by(
        user_id=current_user_id,
        target_type='product'
    ).all()

    liked_products_ids = {like.target_id for like in user_likes}
    
    product = Product.query.get(product_id)
    product_data = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'images': product.images,
        'cost': product.cost,
        'category': product.category,
        'town': product.town,
        'phone_number': product.phone_number,
        'date_pub': product.date_pub,
        'watchs': product.watchs,
        'likes_count': product.likes_count or 0,
        'is_active': product.is_active,
        'is_bargain': product.is_bargain,
        'is_liked': product.id in liked_products_ids,
        'is_owner': True if int(product.owner_id) == int(current_user_id) else False
    }
    return jsonify({
        'product': product_data
    })

@product.route('/api/product/<int:product_id>/view', methods=['POST'])
@jwt_required()
def increment_views(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({ 'error': 'Product not found' }), 404
    
    product.watchs = (product.watchs or 0) + 1
    db.session.commit()

    return jsonify({ 'message': 'View counted', 'views': product.watchs }), 200

@product.route('/api/products/similar/<int:product_id>', methods=['GET'])
@jwt_required()
def get_simmilar_products(product_id):
    current_product = Product.query.get(product_id)
    if not current_product:
        return jsonify({ 'error': 'Product not found' }), 404
    
    similar_products = Product.query.filter(
        Product.category == current_product.category,
        Product.id != product_id,
        Product.is_active == True
    ).order_by(Product.date_pub.desc()).limit(4).all()

    similar_data = [{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'images': p.images,
        'cost': p.cost,
        'category': p.category,
        'town': p.town,
        'date_pub': p.date_pub,
        'watchs': p.watchs,
        'is_active': p.is_active,
        'is_bargain': p.is_bargain
    } for p in similar_products]

    return jsonify({ 'products': similar_data }), 200

@product.route('/api/product/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({ 'error': 'Product not found' }), 404
    
    product_likes = Like.query.filter_by(
        target_id = product_id,
        target_type = 'product'
    ).all()

    if product_likes:
        for like in product_likes:
            db.session.delete(like)

    db.session.delete(product)
    db.session.commit()

    return jsonify({ 'message': 'Product was delete successfully' }), 200

@product.route('/api/product/<int:product_id>/edit', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_product(product_id):
    current_user_id = get_jwt_identity()
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({ 'error': 'Product not found' }), 404
    
    if int(product.owner_id) != int(current_user_id):
        return jsonify({ 'error': 'Not authorized to edit this product' }), 403
    
    try:
        current_images = product.images.copy() if product.images else []
        
        if request.content_type and 'multipart/form-data' in request.content_type:
            if 'images_to_delete' in request.form:
                try:
                    images_to_delete = json.loads(request.form['images_to_delete'])
                    for img in images_to_delete:
                        if img in current_images:
                            current_images.remove(img)
                            try:
                                img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img)
                                if os.path.exists(img_path):
                                    os.remove(img_path)
                            except Exception as e:
                                print(f'Error deleting image file {img}: {e}')
                except json.JSONDecodeError:
                    pass
            
            if 'images' in request.files:
                files = request.files.getlist('images')
                
                if len(files) > 5:
                    return jsonify({ 'error': 'Можно загрузить не более 5 изображений' }), 400
                
                try:
                    image_filenames = save_images(files)
                    current_images.extend(image_filenames)
                except Exception as e:
                    return jsonify({ 'error': f'Ошибка загрузки изображений: {str(e)}' }), 500
            
            if 'title' in request.form:
                product.title = request.form.get('title')
            if 'category' in request.form:
                product.category = request.form.get('category')
            if 'description' in request.form:
                product.description = request.form.get('description')
            if 'city' in request.form:
                product.town = request.form.get('city')
            if 'phone' in request.form:
                product.phone_number = request.form.get('phone')
            
            if 'price' in request.form:
                try:
                    product.cost = int(request.form.get('price'))
                except ValueError:
                    return jsonify({ 'error': 'Invalid price format' }), 400

            if 'is_active' in request.form:
                product.is_active = request.form.get('is_active', 'false').lower() == 'true'
            if 'is_bargain' in request.form:
                product.is_bargain = request.form.get('is_bargain', 'false').lower() == 'true'
            
        else:
            data = request.get_json()
            if data:
                if 'title' in data:
                    product.title = data['title']
                if 'category' in data:
                    product.category = data['category']
                if 'description' in data:
                    product.description = data['description']
                if 'city' in data:
                    product.town = data['city']
                if 'phone' in data:
                    product.phone_number = data['phone']
                if 'price' in data:
                    try:
                        product.cost = int(data['price'])
                    except ValueError:
                        return jsonify({ 'error': 'Invalid price format' }), 400
                if 'is_active' in data:
                    product.is_active = bool(data['is_active'])
                if 'is_bargain' in data:
                    product.is_bargain = bool(data['is_bargain'])
        
        if len(current_images) > 5:
            return jsonify({ 'error': 'Нельзя иметь более 5 изображений' }), 400
        
        product.images = current_images
        
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'images': product.images,
                'cost': product.cost,
                'category': product.category,
                'town': product.town,
                'phone_number': product.phone_number,
                'is_active': product.is_active,
                'is_bargain': product.is_bargain
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating product: {e}")
        return jsonify({ 'error': f'Internal server error: {e}' }), 500
    
@product.route('/api/product/<int:product_id>/reserved', methods=['PUT'])
@jwt_required()
def reserve_product(product_id):
    current_user_id = get_jwt_identity()

    product = Product.query.get(product_id)

    if not product:
        return jsonify({ 'error': 'Product not found' }), 404
    
    if int(product.owner_id) != int(current_user_id):
        return jsonify({ 'error': 'Not authorized to reserve this product' }), 403
    
    if product.status == 'reserved':
        product.status = 'active'
        message = 'Product unreserzed'
    else:
        product.status = 'reserved'
        message = 'Product reserved'
    
    db.session.commit()

    return jsonify({ 
        'message': message,
        'status': product.status
    }), 200

@product.route('/api/product/<int:product_id>/sold', methods=['PUT'])
@jwt_required()
def sold_product(product_id):
    current_user_id = get_jwt_identity()

    product = Product.query.get(product_id)

    if not product:
        return jsonify({ 'error': 'Product not found' }), 404
    
    if int(product.owner_id) != int(current_user_id):
        return jsonify({ 'error': 'Not authorized to reserve this product' }), 403
    
    product.is_active = False
    product.status = 'sold'

    db.session.commit()

    return jsonify({ 'message': 'Product sold' }), 200