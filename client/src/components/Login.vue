<template>
  <div class="auth-page">
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>
    
    <div class="auth-container">
        <h1 class="auth-title">Запустите двигатель</h1>
        <p class="auth-subtitle">Ваше путешествие начинается здесь</p>
        
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label class="form-label">Электронная почта</label>
                <input 
                  type="email" 
                  class="form-input" 
                  placeholder="your.email@example.com" 
                  v-model="form.email"
                  required
                >
            </div>
            
            <div class="form-group">
                <label class="form-label">Пароль</label>
                <input 
                  type="password" 
                  class="form-input" 
                  placeholder="••••••••"
                  v-model="form.password"
                  required
                >
            </div>

            <div v-if="error" class="error-message">
                {{ error }}
            </div>
            
            <button type="submit" class="btn-login" :disabled="loading">
              {{ loading ? 'Вход...' : 'Войти в систему' }}
            </button>
            
            <div class="auth-links">
                  <router-link to="/register" class="auth-link">Создать аккаунт</router-link>
                  <router-link to="/login" class="auth-link">Забыли пароль?</router-link>
            </div>
        </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authService } from '../utils/checkAuth'

const router = useRouter()
const route = useRoute()
const emit = defineEmits(['user-updated'])

const form = reactive({
    email: '',
    password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
    error.value = ''
    loading.value = true
    
    try {
        const result = await authService.login(form.email, form.password)
        
        if (result && result.user) {
            emit('user-updated', { 
                user: result.user, 
                access_token: result.token 
            })
            
            const redirect = route.query.redirect || '/dashboard'
            router.push(redirect)
        } else {
            error.value = 'Не удалось получить данные пользователя'
        }
    } catch (err) {
        console.error('Login error:', err)
        error.value = err.error || 'Ошибка входа. Проверьте email и пароль.'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.error-message {
    color: #ff6b6b;
    background: rgba(255, 107, 107, 0.1);
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 14px;
    border-left: 3px solid #ff6b6b;
}

.auth-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 20px;
}

.auth-container {
    width: 100%;
    max-width: 420px;
    padding: 40px 30px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        0 0 0 1px rgba(255, 255, 255, 0.05),
        0 0 30px rgba(255, 69, 0, 0.1);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.auth-container:hover {
    transform: translateY(-5px);
    box-shadow: 
        0 12px 40px rgba(0, 0, 0, 0.4),
        0 0 0 1px rgba(255, 255, 255, 0.1),
        0 0 40px rgba(255, 69, 0, 0.15);
}

/* Эффект светящихся углов */
.auth-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 69, 0, 0.6), transparent);
}

.auth-title {
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: 300;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
    letter-spacing: 1px;
}

.auth-subtitle {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    margin-bottom: 35px;
    font-weight: 300;
}

.form-group {
    margin-bottom: 25px;
    position: relative;
}

.form-label {
    display: block;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: 400;
}

.form-input {
    width: 100%;
    padding: 14px 16px;
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    color: white;
    font-size: 15px;
    transition: all 0.3s ease;
    outline: none;
}

.form-input:focus {
    border-color: rgba(255, 69, 0, 0.6);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
    background: rgba(255, 255, 255, 0.1);
}

.form-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
}

.btn-login {
    width: 100%;
    padding: 15px;
    background: rgba(255, 69, 0, 0.15);
    border: 1px solid rgba(255, 69, 0, 0.4);
    border-radius: 10px;
    color: white;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    text-shadow: 0 0 8px rgba(255, 69, 0, 0.5);
    letter-spacing: 0.5px;
    margin-top: 10px;
}

.btn-login:hover:not(:disabled) {
    background: rgba(255, 69, 0, 0.25);
    border-color: rgba(255, 69, 0, 0.7);
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
    transform: translateY(-2px);
}

.btn-login:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.auth-links {
    display: flex;
    justify-content: space-between;
    margin-top: 25px;
    font-size: 14px;
}

.auth-link {
    color: rgba(255, 255, 255, 0.7);
    text-decoration: none;
    transition: all 0.3s ease;
    position: relative;
}

.auth-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 1px;
    background: rgba(255, 69, 0, 0.7);
    transition: width 0.3s ease;
}

.auth-link:hover {
    color: white;
    text-shadow: 0 0 8px rgba(255, 69, 0, 0.5);
}

.auth-link:hover::after {
    width: 100%;
}

/* Дополнительные декоративные элементы */
.decoration {
    position: fixed;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    z-index: 0;
}

.decoration-1 {
    background: #ff4500;
    top: -50px;
    right: -50px;
}

.decoration-2 {
    background: #00bfff;
    bottom: -50px;
    left: -50px;
}

/* Адаптивность */
@media (max-width: 480px) {
    .auth-page {
        margin-top: 10%;
    }
    
    .auth-container {
        padding: 30px 20px;
    }
    
    .auth-title {
        font-size: 24px;
    }
    
    .auth-links {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }
}
</style>