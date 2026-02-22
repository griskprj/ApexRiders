from flask import current_app
import os
import uuid
from werkzeug.utils import secure_filename
import mimetypes

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    if '.' not in filename:
        return True
    ext = filename.rsplit('.', 1)[1].lower()
    result = ext in ALLOWED_EXTENSIONS
    return result

def get_extension_from_mime(content_type):
    """Определяет расширение файла по MIME типу"""
    mime_to_ext = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/bmp': '.bmp'
    }
    return mime_to_ext.get(content_type, '')

def save_images(files):
    """Сохранение изображений (уже сжатых на клиенте)"""
    saved_filenames = []
    failed_files = []

    base_upload_folder = current_app.config['UPLOAD_FOLDER']
    
    upload_folder = os.path.join(base_upload_folder, 'listings')
    
    os.makedirs(upload_folder, exist_ok=True)
    
    for i, file in enumerate(files):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
    
    for file in files:
        if file and file.filename:
            
            if not allowed_file(file.filename):
                if file.content_type and file.content_type in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']:
                    return
                else:
                    failed_files.append(file.filename)
                    continue

            original_filename = secure_filename(file.filename)
            
            if original_filename == 'blob' or '.' not in original_filename:
                ext = get_extension_from_mime(file.content_type)
                if not ext:
                    failed_files.append(file.filename)
                    continue
                filename = f"{uuid.uuid4().hex}{ext}"
            else:
                name_without_ext = os.path.splitext(original_filename)[0]
                ext = os.path.splitext(original_filename)[1]
                filename = f"{uuid.uuid4().hex}_{name_without_ext}{ext}"

            try:
                file_path = os.path.join(upload_folder, filename)
                file.seek(0)
                file.save(file_path)
                
                if os.path.exists(file_path):
                    saved_size = os.path.getsize(file_path)
                    saved_filenames.append(filename)
                else:
                    failed_files.append(original_filename)
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                failed_files.append(original_filename)
        else:
            failed_files.append("unknown_file")

    if failed_files:
        try:
            current_app.logger.warning(f'Не удалось сохранить файлы: {failed_files}')
        except:
            print(f'Не удалось сохранить файлы: {failed_files}')

    return saved_filenames