# migration_script.py
from app import create_app
from app.models import Post, db
import html2text

app = create_app()

with app.app_context():
    posts = Post.query.all()
    h = html2text.HTML2Text()
    h.ignore_links = False
    
    for post in posts:
        try:
            # Конвертируем HTML в Markdown
            markdown_content = h.handle(post.content)
            # Сохраняем Markdown в content
            post.content = markdown_content
            
            # Генерируем HTML из Markdown для html_content
            import markdown
            from bleach import clean
            
            html_content = markdown.markdown(
                markdown_content, 
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
            
            post.html_content = clean(
                html_content, 
                tags=allowed_tags, 
                attributes=allowed_attrs,
                protocols=['http', 'https', 'mailto', 'data'],
                strip=False
            )
            
            print(f"Конвертирован пост {post.id}")
            
        except Exception as e:
            print(f"Ошибка конвертации поста {post.id}: {e}")
            continue
    
    db.session.commit()
    print("Миграция завершена")