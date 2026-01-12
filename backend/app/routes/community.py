import markdown
from bleach import clean
import bleach
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Member, Post, Comment, Like, db
from datetime import datetime, timezone

community = Blueprint('community', __name__)

@community.route('/api/posts', methods=['GET'])
@jwt_required()
def get_posts():
    current_user_id = get_jwt_identity()

    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filter_type = request.args.get('filter', 'all')

        query = Post.query

        if filter_type == 'popular':
            query = query.order_by(Post.like_count.desc())
        elif filter_type == 'recent':
            query = query.order_by(Post.created_at.desc())
        elif filter_type == 'my':
            query = query.filter_by(author_id=current_user_id).order_by(Post.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        posts = pagination.items

        posts_data = []
        for post in posts:
            author = Member.query.get(post.author_id)

            html_content = markdown.markdown(
                post.content[:500] + '...' if len(post.content) > 500 else post.content,
                extensions=['tables', 'fenced_code', 'nl2br']
            )

            posts_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'htmlContent': html_content,
                'excerpt': post.content[:150] + '...' if len(post.content) > 150 else post.content,
                'author': {
                    'id': author.id,
                    'username': author.username,
                    'name': author.username
                },
                'createdAt': post.created_at.isoformat(),
                'updatedAt': post.updated_at.isoformat(),
                'commentsCount': post.comment_count,
                'likesCount': post.like_count,
                'views': post.view_count,
                'category': 'General',
                'categoryIcon': 'fas fa-comment',
                'imageUrl': None
            })

        return jsonify({
            'posts': posts_data,
            'total': pagination.total,
            'page': page,
            'perPage': per_page,
            'totalPages': pagination.pages
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error fetching posts: {str(e)}')
        return jsonify({ 'error': 'Failed to fetch posts' }), 500
    
@community.route('/api/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    try:
        current_user_id = get_jwt_identity()

        post = Post.query.get_or_404(post_id)

        post.view_count += 1
        db.session.commit()

        author = Member.query.get(post.author_id)

        raw_content = post.content
        html_content = markdown.markdown(
            raw_content, 
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'b', 'i', 'u', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 
            'hr', 'a', 'img', 'table', 'thead', 'tbody', 
            'tr', 'th', 'td', 'span', 'div'
        ]
        
        allowed_attrs = {
            'a': ['href', 'title', 'target', 'rel'],
            'img': ['src', 'alt', 'title', 'width', 'height', 'class', 'style'],
            'code': ['class'],
            'pre': ['class']
        }
        
        safe_html = clean(
            html_content, 
            tags=allowed_tags, 
            attributes=allowed_attrs,
            protocols=['http', 'https', 'mailto', 'data'],
            strip=False
        )

        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.html_content,
            'htmlContent': safe_html,
            'author': {
                'id': author.id,
                'username': author.username,
                'isVerified': True if int(author.id) == int(current_user_id) else False
            },
            'createdAt': post.created_at.isoformat(),
            'updatedAt': post.updated_at.isoformat(),
            'commentsCount': post.comment_count,
            'likesCount': post.like_count,
            'views': post.view_count
        }), 200

    except Exception as e:
        current_app.logger.error(f'Error fetching post: {str(e)}')
        return jsonify({ 'error': 'Post not found' }), 404
    
@community.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data.get('title') or not data.get('content'):
            return jsonify({ 'error': 'Title and content are required' }), 400
        
        raw_content = data['content']
        html_content = markdown.markdown(
            raw_content, 
            extensions=['tables', 'fenced_code', 'nl2br']
        )

        allowed_tags = [
            'p', 'br', 'strong', 'em', 'b', 'i', 'u', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 
            'hr', 'a', 'img', 'table', 'thead', 'tbody', 
            'tr', 'th', 'td', 'span', 'div'
        ]
        
        allowed_attrs = {
            '*': ['class', 'id', 'style'],
            'a': ['href', 'title', 'target', 'rel'],
            'img': ['src', 'alt', 'title', 'width', 'height', 'class', 'style'],
            'code': ['class'],
            'pre': ['class']
        }
        
        safe_html = clean(
            html_content, 
            tags=allowed_tags, 
            attributes=allowed_attrs,
            protocols=['http', 'https', 'mailto', 'data'],
            strip=False
        )

        new_post = Post(
            title=data['title'],
            content=raw_content,
            html_content=safe_html,
            author_id=current_user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.session.add(new_post)
        db.session.commit()

        author = Member.query.get(current_user_id)

        return jsonify({
            'id': new_post.id,
            'title': new_post.title,
            'content': new_post.content,
            'excerpt': new_post.content[:150] + '...',
            'author': {
                'id': author.id,
                'username': author.username,
                'name': author.username
            },
            'createdAt': new_post.created_at.isoformat(),
            'commentsCount': 0,
            'likesCount': 0,
            'views': 0,
            'imageUrl': data.get('imageUrl')
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating post: {str(e)}')
        return jsonify({ 'error': 'Failed to create post'}), 500
    
@community.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    try:
        current_user_id = get_jwt_identity()

        existing_like = Like.query.filter_by(
            user_id=current_user_id,
            target_type='post',
            target_id=post_id,
        ).first()

        post = Post.query.get_or_404(post_id)

        if existing_like:
            db.session.delete(existing_like)
            post.like_count = max(0, post.like_count - 1)
            db.session.commit()
            return jsonify({ 'liked': False, 'likesCount': post.like_count }), 200
        else:
            new_like = Like(
                user_id=current_user_id,
                target_type='post',
                target_id=post_id
            )
            db.session.add(new_like)
            post.like_count += 1
            db.session.commit()
            return jsonify({ 'liked': True, 'likesCount': post.like_count }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error toggling like: {str(e)}')
        return jsonify({ 'error': 'Failed to toggle like'}), 500
    
@community.route('/api/posts/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        comments = Comment.query.filter_by(post_id=post_id)\
            .order_by(Comment.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        print(post_id)
        
        comments_data = []
        for comment in comments.items:
            author = Member.query.get(comment.author_id)
            comments_data.append({
                'id': comment.id,
                'content': comment.content,
                'author': {
                    'id': author.id,
                    'username': author.username,
                    'isVerified': author.is_verified
                },
                'createdAt': comment.created_at,
                'likeCount': comment.like_count
            })

        return jsonify({
            'comment': comments_data,
            'total': comments.total,
            'page': page,
            'perPage': per_page
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error fetching comments: {str(e)}')
        return jsonify({ 'error': 'Failed to fetch comments'}), 500
    
@community.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data.get('content'):
            return jsonify({ 'error': 'Comment content is required' }), 400
        
        post = Post.query.get_or_404(post_id)

        new_comment = Comment(
            content=data['content'],
            post_id=post_id,
            author_id=current_user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        post.comment_count += 1

        db.session.add(new_comment)
        db.session.commit()

        author = Member.query.get(current_user_id)

        return jsonify({
            'id': new_comment.id,
            'content': new_comment.content,
            'author': {
                'id': author.id,
                'username': author.username
            },
            'createdAt': new_comment.created_at.isoformat(),
            'likeCount': 0
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating comment: {str(e)}')
        return jsonify({ 'error': 'Failed to create comment' }), 500
    
@community.route('/api/community/stats', methods=['GET'])
@jwt_required()
def get_community_stats():
    try:
        current_user_id = get_jwt_identity()

        user_posts = Post.query.filter_by(author_id=current_user_id).count()
        user_comments = Comment.query.filter_by(author_id=current_user_id).count()

        active_users = Member.query\
            .join(Post, Member.id == Post.author_id)\
            .group_by(Member.id)\
            .order_by(db.func.count(Post.id).desc())\
            .limit(5)\
            .all()
        
        active_users_data = []
        for user in active_users:
            post_count = Post.query.filter_by(author_id=user.id).count()
            active_users_data.append({
                'id': user.id,
                'username': user.username,
                'name': user.username,
                'posts': post_count
            })

        return jsonify({
            'userStats': {
                'posts': user_posts,
                'comments': user_comments
            },
            'activeUsers': active_users_data
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error fetching community stats: {str(e)}')
        return jsonify({ 'error': 'Error fetching community stats'}), 500
    
@community.route('/api/posts/<int:post_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        current_user_id = get_jwt_identity()

        post = Post.query.get(post_id)
        if not post:
            current_app.logger.error('Post not found')
            return jsonify({ 'error': 'Post not found' }), 404
        
        comments = Comment.query.filter_by(post_id=post_id).all()
        likes = Like.query.filter_by(target_type='post', target_id=post_id).all()

        if comments:
            for comment in comments:
                db.session.delete(comment)
        if likes:
            for like in likes:
                db.session.delete(like)

        db.session.delete(post)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Пост удален'
        })
    except Exception as e:
        current_app.logger.error(f'Error delete post: {str(e)}')
        return jsonify({ 'error': 'Error delete post'}), 500
    
@community.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        post = Post.query.get_or_404(post_id)
        if int(post.author_id) != int(current_user_id):
            return jsonify({ 'error': 'You can only edit your own posts' }), 403
        
        if 'title' in data and data['title']:
            post.title = data['title']
        
        if 'content' in data and data['content']:
            raw_content = data['content']

            html_content = markdown.markdown(
                raw_content, 
                extensions=['tables', 'fenced_code', 'nl2br']  # <-- ДОБАВЬТЕ ЭТО
            )

            allowed_tags = [
                'p', 'br', 'strong', 'em', 'b', 'i', 'u', 
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 
                'hr', 'a', 'img', 'table', 'thead', 'tbody', 
                'tr', 'th', 'td', 'span', 'div'
            ]
            
            allowed_attrs = {
                '*': ['class', 'id', 'style'],
                'a': ['href', 'title', 'target', 'rel'],
                'img': ['src', 'alt', 'title', 'width', 'height', 'class', 'style'],
                'code': ['class'],
                'pre': ['class']
            }

            safe_html = clean(
                html_content,
                tags=allowed_tags,
                attributes=allowed_attrs,
                protocols=['http', 'https', 'mailto', 'data'],
                strip=False
            )

            post.content = raw_content
            post.html_content = safe_html
        
        post.updated_at = datetime.now(timezone.utc)

        db.session.commit()

        author = Member.query.get(post.author_id)

        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'htmlContent': post.html_content,
            'author': {
                'id': author.id,
                'username': author.username,
                'name': author.username
            },
            'createdAt': post.created_at,
            'updatedAt': post.updated_at,
            'commentsCount': post.comment_count,
            'likesCount': post.like_count,
            'views': post.view_count
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating post: {str(e)}')
        return jsonify({ 'error': 'Failed to update post' }), 500