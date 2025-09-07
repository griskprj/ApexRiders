from flask import current_app, url_for, render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.extensions import mail

def send_register_confirmation_email(user):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(
        user.email,
        salt=current_app.config['REGISTER_EMAIL_CONFIRMATION_SALT']
    )

    confirm_url = url_for('confirmation_reg.confirm_email', token=token, _external=True)

    html = render_template(
        '/emails/confirm_email.html',
        username=user.username,
        confirmation_url=confirm_url
    )

    msg = Message(
        'Подтверждение регистер - ApexRiders',
        recipients=[user.email],
        html=html
    )

    mail.send(msg)
