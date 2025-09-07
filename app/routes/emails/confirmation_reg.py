from flask import Blueprint, redirect, url_for, flash, current_app
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer
from app.models import User
from app.extensions import limiter, db
from app.utils.emails.register import send_register_confirmation_email

CONFIRMATION_EXPIRATION = 3600

confirmation_reg = Blueprint('confirmation_reg', __name__, url_prefix='/confirmation/registration')

""" EMAIL CONFIRMATION """
@confirmation_reg.route('/confirm/<token>')
@limiter.limit('5 per minute')
def confirm_email(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(
            token,
            salt=current_app.config['REGISTER_EMAIL_CONFIRMATION_SALT'],
            max_age=CONFIRMATION_EXPIRATION
        )
    
    except Exception as e:
        current_app.logger.error(f'Error confirmation email: {str(e)}')
        flash('Ссылка просрочена или недействительна', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first_or_404()

    if user.is_confirmed:
        flash('Аккаунт уже подтвержден', 'info')
    else:
        user.is_confirmed = True
        db.session.commit()
        flash('Email успешно подтвержден!', 'success')
    
    return redirect(url_for('main.dashboard'))

""" RESEND CONFIRMATION """
@confirmation_reg.route('/resend_confirmation')
@limiter.limit('5 per minute')
def resend_confirmation():
    if current_user.is_confirmed:
        flash('Ваш email уже подтверждег', 'info')
        return redirect(url_for('main.dashboard'))
    
    send_register_confirmation_email(current_user)
