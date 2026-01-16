<template>
    <!-- Декоративные элементы -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    

    <!-- Главная секция -->
    <section class="hero" id="home">
        <div class="hero-bg"></div>
        <h1>Сообщество <span>мотоциклистов</span> нового поколения</h1>
        <p>Полный набор инструментов для ремонта, обучения и общения. Мануалы, курсы, схемы тренировок и площадка для покупки/продажи всего, что связано с мотоциклами.</p>
        
        <div class="hero-buttons">
            <a href="#features" class="btn btn-primary">Начать исследовать</a>
            <router-link to="/register" class="btn btn-outline">Присоединиться</router-link>
        </div>
    </section>

    <!-- Основной функционал -->
    <section class="section" id="features">
        <h2 class="section-title">Что мы предлагаем</h2>
        <p class="section-subtitle">Все инструменты для мотоциклиста в одном месте</p>
        
        <div class="features">
            <!-- Мануалы -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-book"></i>
                </div>
                <h3>Мануалы по ремонту</h3>
                <p>Подробные руководства по ремонту и обслуживанию мотоциклов различных марок и моделей. От замены масла до капитального ремонта двигателя.</p>
                <a href="#manuals" class="feature-link">Изучить мануалы <i class="fas fa-arrow-right"></i></a>
            </div>
            
            <!-- Курсы -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <h3>Курсы вождения</h3>
                <p>Видеоуроки и текстовые материалы для водителей любого уровня. От базовых навыков до продвинутых техник управления мотоциклом.</p>
                <a href="#courses" class="feature-link">Начать обучение <i class="fas fa-arrow-right"></i></a>
            </div>
            
            <!-- Схемы тренировок -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-route"></i>
                </div>
                <h3>Схемы для мотоджимхан</h3>
                <p>Готовые схемы и траектории для тренировок и соревнований. Настраиваемые маршруты для отработки конкретных навыков.</p>
                <a href="#training" class="feature-link">Посмотреть схемы <i class="fas fa-arrow-right"></i></a>
            </div>
            
            <!-- Маркет -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-shopping-cart"></i>
                </div>
                <h3>Маркет запчастей</h3>
                <p>Площадка для покупки и продажи мотоциклов, запчастей, экипировки. Безопасные сделки и проверенные продавцы.</p>
                <a href="#market" class="feature-link">Перейти к объявлениям <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </section>

    <!-- Футер -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-column">
                <h4>ApexRiders</h4>
                <p>Сообщество мотоциклистов, созданное для обмена знаниями, опытом и запчастями.</p>
                <div style="display: flex; gap: 15px; margin-top: 20px;">
                    <a href="#"><i class="fab fa-vk"></i></a>
                    <a href="#"><i class="fab fa-telegram"></i></a>
                    <a href="#"><i class="fab fa-youtube"></i></a>
                </div>
            </div>
            
            <div class="footer-column">
                <h4>Разделы</h4>
                <a href="#manuals">Мануалы</a>
                <a href="#courses">Курсы</a>
                <a href="#training">Схемы тренировок</a>
                <a href="#market">Маркет</a>
                <a href="#community">Сообщество</a>
            </div>
            
            <div class="footer-column">
                <h4>Помощь</h4>
                <a href="#">О проекте</a>
                <a href="#">Контакты</a>
                <a href="#">Правила</a>
                <a href="#">Поддержка</a>
            </div>
            
            <div class="footer-column">
                <h4>Контакты</h4>
                <p>Email: info@apexriders.ru</p>
                <p>Телефон: +7 (XXX) XXX-XX-XX</p>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>&copy; 2026 ApexRiders. Все права защищены.</p>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'Home'
}
</script>


<style scoped>
/* ===== ГЛАВНАЯ ГЕРОЙ СЕКЦИЯ ===== */
.hero {
    padding: 180px 5% 120px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse at center, rgba(255, 69, 0, 0.05) 0%, transparent 70%);
    z-index: -1;
}

.hero h1 {
    font-size: 3.5rem;
    font-weight: 300;
    margin-bottom: 20px;
    text-shadow: 0 0 20px rgba(255, 69, 0, 0.5);
    letter-spacing: 1px;
}

.hero h1 span {
    color: var(--primary);
    font-weight: 700;
}

.hero p {
    font-size: 1.2rem;
    color: var(--text-secondary);
    max-width: 700px;
    margin: 0 auto 40px;
    line-height: 1.6;
}

.hero-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 40px;
}

/* ===== ФУНКЦИОНАЛЬНЫЕ БЛОКИ ===== */
.section {
    padding: 100px 5%;
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 20px;
}

.section-subtitle {
    text-align: center;
    color: var(--text-secondary);
    max-width: 700px;
    margin: 0 auto 60px;
    font-size: 1.1rem;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 50px;
}

.feature-card {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 40px 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-10px);
    border-color: var(--primary-dark);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 69, 0, 0.1);
}

.feature-icon {
    width: 70px;
    height: 70px;
    background: var(--primary-light);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 25px;
    font-size: 28px;
    color: var(--primary);
}

.feature-card h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    font-weight: 600;
}

.feature-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 20px;
}

.feature-link {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: gap 0.3s ease;
}

.feature-link:hover {
    gap: 12px;
}

/* ===== ДЕКОРАТИВНЫЕ ЭЛЕМЕНТЫ ===== */
.decoration {
    position: fixed;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    z-index: -1;
}

.decoration-1 {
    background: var(--primary);
    top: 10%;
    right: 5%;
}

.decoration-2 {
    background: var(--accent);
    bottom: 10%;
    left: 5%;
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

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 992px) {
    .hero h1 {
        font-size: 2.8rem;
    }
}

@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.2rem;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .section-title {
        font-size: 2rem;
    }
}

@media (max-width: 480px) {
    .hero {
        padding: 150px 5% 80px;
    }
    
    .feature-card {
        padding: 30px 20px;
    }
    
    .footer-content {
        grid-template-columns: 1fr;
    }
}
</style>