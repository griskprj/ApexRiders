document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Здесь должна быть реальная логина аутентификации
    console.log('Попытка входа:', { email, password });
    
    // Анимация загрузки
    const loginBtn = document.querySelector('.btn-login');
    loginBtn.textContent = 'Вход...';
    loginBtn.disabled = true;
    
    // Имитация запроса на сервер
    setTimeout(() => {
        alert('Вход выполнен успешно! (Это демо, реальной авторизации нет)');
        loginBtn.textContent = 'Войти';
        loginBtn.disabled = false;
    }, 1500);
});

// Добавляем интерактивность для чекбокса
document.getElementById('remember').addEventListener('change', function() {
    const label = document.querySelector('.checkbox-group label');
    if (this.checked) {
        label.style.color = var('--text-primary');
    } else {
        label.style.color = var('--text-secondary');
    }
});