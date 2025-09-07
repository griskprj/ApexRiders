def get_photo(obj):
    from io import BytesIO
    from flask import send_file

    return send_file(
        BytesIO(obj.image),
        mimetype='image/jpg',
        as_attachment=False
    )
