// Базовая валидация подтверждения пароля
document.getElementById('registerForm').addEventListener('submit', function(e) {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password.value !== confirmPassword.value) {
        e.preventDefault();
        alert('Пароли не совпадают!');
        confirmPassword.focus();
    }
});

// Индикатор силы пароля
document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    const hint = this.parentNode.querySelector('.input-hint');
    
    if (password.length === 0) {
        hint.textContent = 'Минимум 6 символов, цифры и буквы';
    } else if (password.length < 6) {
        hint.textContent = 'Слишком короткий пароль';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
        hint.textContent = 'Добавьте заглавные буквы и цифры';
    } else {
        hint.textContent = 'Хороший пароль!';
    }
});