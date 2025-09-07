// Элементы DOM
const registerForm = document.getElementById('registerForm');
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('confirmPassword');
const strengthMeter = document.getElementById('strengthMeter');
const strengthText = document.getElementById('strengthText');
const policyCheckbox = document.getElementById('policy');
const policyLink = document.getElementById('policyLink');
const policyModal = document.getElementById('policyModal');
const closeModal = document.querySelector('.close-modal');
const registerBtn = document.getElementById('registerBtn');

// Проверка сложности пароля
passwordInput.addEventListener('input', function() {
    const password = this.value;
    let strength = 0;
    let message = '';

    if (password.length > 0) {
        // Проверяем длину пароля
        if (password.length > 7) strength += 1;
        
        // Проверяем наличие строчных букв
        if (password.match(/[a-zа-я]/)) strength += 1;
        
        // Проверяем наличие заглавных букв
        if (password.match(/[A-ZА-Я]/)) strength += 1;
        
        // Проверяем наличие цифр
        if (password.match(/\d/)) strength += 1;
        
        // Проверяем наличие специальных символов
        if (password.match(/[^a-zA-Zа-яА-Я0-9]/)) strength += 1;
    }

    // Обновляем индикатор сложности пароля
    switch(strength) {
        case 0:
            strengthMeter.className = 'strength-meter';
            strengthMeter.style.width = '0';
            message = 'Введите пароль';
            break;
        case 1:
        case 2:
            strengthMeter.className = 'strength-meter strength-weak';
            message = 'Слабый пароль';
            break;
        case 3:
        case 4:
            strengthMeter.className = 'strength-meter strength-medium';
            message = 'Средний пароль';
            break;
        case 5:
            strengthMeter.className = 'strength-meter strength-strong';
            message = 'Сильный пароль';
            break;
    }
    
    strengthText.textContent = message;
});

// Проверка совпадения паролей
confirmInput.addEventListener('input', function() {
    if (this.value !== passwordInput.value) {
        this.style.boxShadow = 'inset 2px 2px 4px var(--shadow-dark), inset -2px -2px 4px var(--shadow-light), 0 0 0 2px var(--accent)';
    } else {
        this.style.boxShadow = 'inset 2px 2px 4px var(--shadow-dark), inset -2px -2px 4px var(--shadow-light), 0 0 0 2px var(--success)';
    }
});

// Открытие модального окна с политикой
policyLink.addEventListener('click', function(e) {
    e.preventDefault();
    policyModal.style.display = 'flex';
});

// Закрытие модального окна
closeModal.addEventListener('click', function() {
    policyModal.style.display = 'none';
});

// Закрытие модального окна при клике вне его
window.addEventListener('click', function(e) {
    if (e.target === policyModal) {
        policyModal.style.display = 'none';
    }
});

// Обработка отправки формы
registerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Проверяем, принята ли политика конфиденциальности
    if (!policyCheckbox.checked) {
        alert('Для регистрации необходимо принять условия использования и политику конфиденциальности');
        return;
    }
    
    // Проверяем совпадение паролей
    if (passwordInput.value !== confirmInput.value) {
        alert('Пароли не совпадают');
        return;
    }
    
    // Получаем данные формы
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = passwordInput.value;
    
    // Анимация загрузки
    registerBtn.textContent = 'Регистрация...';
    registerBtn.disabled = true;

    registerForm.submit();
});