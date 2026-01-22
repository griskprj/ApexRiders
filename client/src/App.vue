<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

    <div id="app">
        <!-- Навигация -->
        <nav class="navbar" :class="{ 'scrolled': isScrolled }">
            <router-link to="/" class="logo">
                <i class="fas fa-motorcycle"></i>
                <span>ApexRiders</span>
            </router-link>
            
            <div class="nav-links" v-if="!isMobile">
                <router-link to="/dashboard" class="nav-link" v-if="user">Главная</router-link>
                <router-link to="/manuals" class="nav-link" v-if="user">Мануалы</router-link>
                <router-link to="/courses" class="nav-link" v-if="user">Курсы</router-link>
                <router-link to="/market" class="nav-link" v-if="user">Маркет</router-link>
                <router-link to="/community" class="nav-link" v-if="user">Сообщество</router-link>
                <router-link to="/profile" class="nav-link" v-if="user">Профиль</router-link>
            </div>
            
            <div class="auth-buttons" v-if="!isMobile && !user">
                <router-link to="/login" class="btn btn-outline">Войти</router-link>
                <router-link to="/register" class="btn btn-primary">Регистрация</router-link>
            </div>
            <div class="auth-buttons" v-if="!isMobile && user">
                <button @click="logout" class="btn btn-outline">Выйти</button>
            </div>
            
            <button class="mobile-menu-btn" @click="toggleMobileMenu">
                <i class="fas fa-bars"></i>
            </button>
        </nav>

        <!-- Мобильное меню -->
        <div class="mobile-menu" :class="{ 'active': isMobileMenuOpen }" v-if="isMobile">
            <router-link to="/dashboard" class="nav-link" v-if="user" @click="closeMobileMenu">Главная</router-link>
            <router-link to="/manuals" class="nav-link" v-if="user" @click="closeMobileMenu">Мануалы</router-link>
            <router-link to="/courses" class="nav-link" v-if="user" @click="closeMobileMenu">Курсы</router-link>
            <router-link to="/market" class="nav-link" v-if="user" @click="closeMobileMenu">Маркет</router-link>
            <router-link to="/community" class="nav-link" v-if="user" @click="closeMobileMenu">Сообщество</router-link>
            <router-link to="/profile" class="nav-link" v-if="user">Профиль</router-link>
            
            <div class="mobile-auth">
                <router-link to="/login" class="btn btn-outline" v-if="!user" @click="closeMobileMenu">Войти</router-link>
                <router-link to="/register" class="btn btn-primary" v-if="!user" @click="closeMobileMenu">Регистрация</router-link>
                <button v-if="user" @click="logout" class="btn btn-outline">Выйти</button>
            </div>

            <div class="mobile-menu-overlay" @click="closeMobileMenu"></div>
        </div>

        <main class="main-content">
            <router-view @user-updated="handleUserUpdate"></router-view>
        </main>

    </div>
    <!-- Футер -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-column">
                <h4>ApexRiders</h4>
                <p>Сообщество мотоциклистов, созданное для обмена знаниями, опытом и запчастями.</p>
                <div style="display: flex; gap: 15px; margin-top: 20px;">
                </div>
            </div>

            <div class="footer-column">
                <h4>Правовые документы</h4>
                <router-link to="/privacy-policy" @click="closeMobileMenu">Политика конфеденциальности и обработки персональных данных</router-link>
                <router-link to="/community-rules" @click="closeMobileMenu">Правила</router-link>
            </div>

            <div class="footer-column" v-if="user">
                <h4>Разделы</h4>
                <router-link to="/manuals" @click="closeMobileMenu">Мануалы</router-link>
                <router-link to="/courses" @click="closeMobileMenu">Курсы</router-link>
                <router-link to="/market" @click="closeMobileMenu">Маркет</router-link>
                <router-link to="/community" @click="closeMobileMenu">Сообщество</router-link>
            </div>
            <div class="footer-column" v-else>
                <h4>Разделы</h4>
                <a href="#">Мануалы</a>
                <a href="#">Курсы</a>
                <a href="#">Маркет</a>
                <a href="#">Сообщество</a>
            </div>
            
            <div class="footer-column">
                <h4>Помощь</h4>
                <router-link to="/about" @click="closeMobileMenu">О проекте</router-link>
                <router-link to="/contacts" @click="closeMobileMenu">Контакты</router-link>
                <router-link to="/community-rules" @click="closeMobileMenu">Правила</router-link>
                <a href="#">Поддержка</a>
            </div>
            
            <div class="footer-column">
                <h4>Контакты</h4>
                <p>Email: apexriders@yandex.ru</p>
                <p>Телефон: +7 (988) 405-91-11</p>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>&copy; 2026 ApexRiders. Все права защищены.</p>
        </div>
    </footer>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from './utils/checkAuth'

const router = useRouter()
const isMobile = ref(false)
const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)
const user = ref(null)
const isLoading = ref(false)

const loadUser = async () => {
    isLoading.value = true
    
    try {
        const cachedUser = authService.getUser()
        user.value = cachedUser
        
        if (navigator.onLine) {
            const freshUser = await authService.checkAuth()
            if (freshUser) {
                user.value = freshUser
            } else if (!cachedUser) {
                if (router.currentRoute.value.meta.requiresAuth) {
                    await router.push('/login')
                }
            }
        }
    } catch (error) {
        console.error('Error loading user:', error)
    } finally {
        isLoading.value = false
    }
}

watch(
    () => router.currentRoute.value,
    (to) => {
        if (to.meta.requiresAuth && !user.value) {
            loadUser()
        }
    }
)

const handleUserUpdate = (userData) => {
    if (userData) {
        const userObj = userData.user || userData.member || userData
        if (userObj && (userObj.id || userObj.email)) {
            userObj._timestamp = Date.now()
            authService.saveUser(userObj)
            user.value = userObj
        }
    }
}

const logout = async () => {
    await authService.logout()
    user.value = null
    isMobileMenuOpen.value = false
    router.push('/')
}

const checkMobile = () => {
    isMobile.value = window.innerWidth <= 992
}

const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
    document.body.style.overflow = isMobileMenuOpen.value ? 'hidden' : 'auto'
}

const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
    document.body.style.overflow = 'auto'
}

const handleScroll = () => {
    isScrolled.value = window.scrollY > 50
}

onMounted(() => {
    checkMobile()
    loadUser()
    
    window.addEventListener('resize', checkMobile)
    window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
    window.removeEventListener('resize', checkMobile)
    window.removeEventListener('scroll', handleScroll)
})
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #FFFFFF;
}

:root {
    --primary: #ff4500;
    --primary-light: rgba(255, 69, 0, 0.15);
    --primary-dark: rgba(255, 69, 0, 0.7);
    --primary-rgb: 74, 108, 247;
    
    --bg-primary: #0a0a0f;
    --bg-secondary: #14141e;

    --dark: #0a0a0f;
    --dark-light: rgba(255, 255, 255, 0.08);
    
    --light: #ffffff;
    --gray: #a0a0c0;
    
    --text: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    
    --accent: #00bfff;
    --accent-rgb: 255, 107, 107;

    --success: #9DF29B;
    --success-rgb: 157, 242, 155;
    --warning: #ffa500;
    --warning-rgb: 255, 165, 0;
    --danger: #ff4757;
    --danger-rgb: 255, 71, 87;
    --very-danger: #911721;
    --very-danger-rgb: 145, 23, 33;
    

}

#app {
    min-height: 100vh;
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
    position: relative;
    overflow-x: hidden;
}

#app::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(255, 69, 0, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(0, 191, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(50, 205, 50, 0.05) 0%, transparent 50%);
    z-index: -1;
}

select option {
    background-color: rgb(99, 99, 99);
}

/* ===== НАВИГАЦИЯ ===== */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    padding: 20px 5%;
    background: rgba(10, 10, 15, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
    text-decoration: none;
}

.logo i {
    color: var(--primary);
    text-shadow: 0 0 10px var(--primary);
}

.nav-links {
    display: flex;
    gap: 30px;
}

.nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
    padding: 8px 0;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--primary);
    transition: width 0.3s ease;
}

.nav-link:hover {
    color: var(--text);
}

.nav-link:hover::after {
    width: 100%;
}

.nav-link.active {
    color: var(--text);
}

.nav-link.active::after {
    width: 100%;
}

.auth-buttons {
    display: flex;
    gap: 15px;
}

.btn {
    padding: 10px 24px;
    border-radius: 8px;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-size: 15px;
}

.btn-outline {
    background: transparent;
    border: 1px solid var(--primary);
    color: var(--text);
}

.btn-outline:hover {
    background: var(--primary-light);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
}

.btn-primary {
    background: var(--primary);
    color: white;
    border: 1px solid var(--primary);
}

.btn-primary:hover {
    background: #ff5500;
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.5);
    transform: translateY(-2px);
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.mobile-menu-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    color: var(--text);
    font-size: 24px;
    cursor: pointer;
}

.nav-links button:hover {
    background: rgba(255, 69, 0, 0.3);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
}

/* ===== ПОДВАЛ ===== */
.footer {
    background: rgba(0, 0, 0, 0.3);
    padding: 60px 5% 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 100px;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 40px;
    margin-bottom: 40px;
}

.footer-column h4 {
    font-size: 1.2rem;
    margin-bottom: 20px;
    color: var(--text);
    font-weight: 600;
}

.footer-column a {
    display: block;
    color: var(--text-secondary);
    text-decoration: none;
    margin-bottom: 12px;
    transition: color 0.3s ease;
}

.footer-column a:hover {
    color: var(--primary);
}

.footer-bottom {
    text-align: center;
    padding-top: 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    color: var(--text-secondary);
    font-size: 0.9rem;
}

/* Дополнительные стили для профиля */
.profile-badge {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    margin-top: 10px;
}

/* Стили для инпутов */
input, textarea, select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

/* Улучшенные стили для кнопок */
.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn:disabled:hover {
    transform: none;
    box-shadow: none;
}

/* ===== MARKDOWN стили ===== */
.markdown-content {
  line-height: 1.8;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  color: var(--text);
  font-weight: 600;
}

.markdown-content h1 { 
  font-size: 1.8em; 
  border-bottom: 2px solid var(--primary); 
  padding-bottom: 0.3em; 
}

.markdown-content pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1em 0;
}

.markdown-content code {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'Consolas', monospace;
  font-size: 0.9em;
}

.markdown-content blockquote {
  border-left: 4px solid var(--primary);
  padding-left: 1em;
  margin-left: 0;
  color: var(--text-secondary);
  background: rgba(255, 69, 0, 0.05);
}

@media (max-width: 992px) {
    .hero h1 {
        font-size: 2.8rem;
    }
    
    .nav-links, .auth-buttons {
        display: none;
    }
    
    .mobile-menu-btn {
        display: block;
    }
    
    .mobile-menu {
        position: fixed;
        top: 80px;
        right: 0;
        width: 300px;
        height: calc(100vh - 80px);
        z-index: 100;
        background: rgba(10, 10, 15, 0.98);
        backdrop-filter: blur(20px);
        padding: 40px;
        display: flex;
        flex-direction: column;
        gap: 25px;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    }
    
    .mobile-menu.active {
        transform: translateX(0);
    }
    
    .mobile-menu .nav-link {
        font-size: 1.2rem;
        padding: 10px 0;
    }
    
    .mobile-auth {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 30px;
    }
}

@media (max-width: 480px) {
    .footer-content {
        grid-template-columns: 1fr;
    }
}
</style>