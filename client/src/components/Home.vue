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
                
                <div class="feature-details">
                    <div class="feature-detail-item">
                        <i class="fas fa-check-circle"></i>
                        <span>Пошаговые инструкции с фото/видео</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-user-check"></i>
                        <span>Только от верифицированных экспертов</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-tasks"></i>
                        <span>Отмечайте пройденные шаги</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-search"></i>
                        <span>Поиск по марке, модели, названию</span>
                    </div>
                </div>
                
                <a href="#manuals" class="feature-link">Изучить мануалы <i class="fas fa-arrow-right"></i></a>
            </div>
            
            <!-- Курсы -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <span class="badge">В разработке</span>
                <h3>Курсы вождения</h3>
                <p>Видеоуроки и текстовые материалы для водителей любого уровня. От базовых навыков до продвинутых техник управления мотоциклом.</p>
                
                <div class="feature-details">
                    <div class="feature-detail-item">
                        <i class="fas fa-video"></i>
                        <span>Видеоуроки в HD качестве</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-chart-line"></i>
                        <span>Прогресс обучения с отслеживанием</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-certificate"></i>
                        <span>Сертификаты об окончании</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-road"></i>
                        <span>Для райдеров любого уровня</span>
                    </div>
                </div>
                
                <a href="#courses" class="feature-link">Начать обучение <i class="fas fa-arrow-right"></i></a>
            </div>
            
            <!-- Схемы тренировок -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-route"></i>
                </div>
                <span class="badge">В разработке</span>
                <h3>Схемы для мотоджимхан</h3>
                <p>Готовые схемы и траектории для тренировок и соревнований. Настраиваемые маршруты для отработки конкретных навыков.</p>
                
                <div class="feature-details">
                    <div class="feature-detail-item">
                        <i class="fas fa-download"></i>
                        <span>Скачиваемые схемы в PDF</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-sliders-h"></i>
                        <span>Настройка сложности маршрута</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-stopwatch"></i>
                        <span>Таймер для отслеживания времени</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-share-alt"></i>
                        <span>Делитесь своими схемами</span>
                    </div>
                </div>
                
                <a href="#training" class="feature-link">Посмотреть схемы <i class="fas fa-arrow-right"></i></a>
            </div>
            
            <!-- Маркет -->
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-shopping-cart"></i>
                </div>
                <h3>Маркет запчастей</h3>
                <p>Площадка для покупки и продажи мотоциклов, запчастей, экипировки. Безопасные сделки и проверенные продавцы.</p>
                
                <div class="feature-details">
                    <div class="feature-detail-item">
                        <i class="fas fa-filter"></i>
                        <span>Фильтры: цена, город, категория</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-shield-alt"></i>
                        <span>Проверенные продавцы</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-comments"></i>
                        <span>Широкий выбор категории товара</span>
                    </div>
                    <div class="feature-detail-item">
                        <i class="fas fa-star"></i>
                        <span>Система рейтингов и отзывов</span>
                    </div>
                </div>
                
                <a href="#market" class="feature-link">Перейти к объявлениям <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </section>

    <!-- Подробное описание разделов -->
    <section class="section section-detailed" id="detailed-features">
        <h2 class="section-title">Подробнее о функциях</h2>
        <p class="section-subtitle">Узнайте, как каждый раздел поможет вам в мото-жизни</p>
        
        <div class="detailed-features">
            <!-- Мануалы подробно -->
            <div class="detailed-feature">
                <div class="detailed-feature-icon">
                    <i class="fas fa-book"></i>
                </div>
                <div class="detailed-feature-content">
                    <h3>Интеллектуальные мануалы по ремонту</h3>
                    <p>Наша система мануалов создана профессионалами для профессионалов. Каждый мануал проходит модерацию и проверку на точность.</p>
                    <ul class="feature-benefits">
                        <li><i class="fas fa-check"></i> <strong>Только проверенные авторы</strong> — Все руководства создаются верифицированными экспертами, отобранными администрацией</li>
                        <li><i class="fas fa-check"></i> <strong>Интерактивное прохождение</strong> — Отмечайте пройденные шаги, сохраняйте прогресс</li>
                        <li><i class="fas fa-check"></i> <strong>Мультимедийный контент</strong> — Фото, видео и схемы для наглядности</li>
                        <li><i class="fas fa-check"></i> <strong>Система рейтингов</strong> — Сначала отображаются мануалы с выском рейтингом</li>
                    </ul>
                </div>
            </div>
            
            <!-- Курсы подробно -->
            <div class="detailed-feature">
                <div class="detailed-feature-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <div class="detailed-feature-content">
                    <h3>Структурированные курсы вождения</h3>
                    <p>От новичка до профи — учитесь в удобном темпе с профессиональными инструкторами.</p>
                    <ul class="feature-benefits">
                        <li><i class="fas fa-check"></i> <strong>Поэтапное обучение</strong> — Курсы разбиты на модули от простого к сложному</li>
                        <li><i class="fas fa-check"></i> <strong>Теория и практика</strong> — Видеоуроки, текстовые материалы и практические задания</li>
                        <li><i class="fas fa-check"></i> <strong>Личный кабинет ученика</strong> — Отслеживайте прогресс, сохраняйте любимые уроки</li>
                        <li><i class="fas fa-check"></i> <strong>Скоро в обновлении</strong> — В разработке: тесты, live-вебинары, органиязация живых встреч</li>
                    </ul>
                </div>
            </div>
            
            <!-- Маркет подробно -->
            <div class="detailed-feature">
                <div class="detailed-feature-icon">
                    <i class="fas fa-shopping-cart"></i>
                </div>
                <div class="detailed-feature-content">
                    <h3>Умная площадка для покупок</h3>
                    <p>Находите нужные запчасти, мотоциклы и экипировку с удобной системой поиска и фильтрации.</p>
                    <ul class="feature-benefits">
                        <li><i class="fas fa-check"></i> <strong>Расширенные фильтры</strong> — Ищите по цене, городу, состоянию, бренду и характеристикам</li>
                        <li><i class="fas fa-check"></i> <strong>Безопасные сделки</strong> — Вы не покупаете товар, а только связываетесь с продавцом</li>
                        <li><i class="fas fa-check"></i> <strong>Уведомления</strong> — Получайте оповещения о новых предложениях по вашим запросам</li>
                        <li><i class="fas fa-check"></i> <strong>Избранное</strong> — Сохраняйте понравившиеся товары для сравнения</li>
                    </ul>
                </div>
            </div>
            
            <!-- Сообщество подробно -->
            <div class="detailed-feature">
                <div class="detailed-feature-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="detailed-feature-content">
                    <h3>Мото-сообщество с соц. сетью</h3>
                    <p>Общайтесь, делитесь опытом и находите единомышленников в нашей встроенной социальной сети.</p>
                    <ul class="feature-benefits">
                        <li><i class="fas fa-check"></i> <strong>Публикация постов</strong> — Делитесь фото, видео и историями на мото-тематику</li>
                        <li><i class="fas fa-check"></i> <strong>Markdown-редактор</strong> — Форматируйте тексты, добавляйте код, списки и цитаты</li>
                        <li><i class="fas fa-check"></i> <strong>Лайки и комментарии</strong> — Взаимодействуйте с контентом других пользователей</li>
                        <li><i class="fas fa-check"></i> <strong>Группы по интересам</strong> — Присоединяйтесь к сообществам по маркам и темам</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
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
    display: flex;
    flex-direction: column;
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
    transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
}

.feature-card h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    font-weight: 600;
}

.badge {
    background: linear-gradient(135deg, var(--warning), #ff9900);
    color: var(--dark);
    padding: 5px 12px;
    margin-bottom: 10px;
    border-radius: 20px;
    width: 120px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(255, 165, 0, 0.3);
}

.feature-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 25px;
    flex-grow: 0;
}

/* Детали функций */
.feature-details {
    margin-bottom: 25px;
    flex-grow: 1;
}

.feature-detail-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.feature-detail-item i {
    color: var(--primary);
    font-size: 0.8rem;
    min-width: 16px;
}

.feature-link {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: gap 0.3s ease;
    margin-top: auto;
}

.feature-link:hover {
    gap: 12px;
}

/* ===== ПОДРОБНЫЕ ОПИСАНИЯ ===== */
.section-detailed {
    background: rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.detailed-features {
    max-width: 1200px;
    margin: 0 auto;
}

.detailed-feature {
    display: flex;
    align-items: flex-start;
    gap: 40px;
    margin-bottom: 60px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

.detailed-feature:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 69, 0, 0.2);
    transform: translateX(10px);
}

.detailed-feature-icon {
    min-width: 80px;
    height: 80px;
    background: var(--primary-light);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: var(--primary);
    flex-shrink: 0;
}

.detailed-feature-content {
    flex-grow: 1;
}

.detailed-feature-content h3 {
    font-size: 1.8rem;
    margin-bottom: 15px;
    color: var(--text);
}

.detailed-feature-content > p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 20px;
    font-size: 1.1rem;
}

.feature-benefits {
    list-style: none;
    padding: 0;
}

.feature-benefits li {
    margin-bottom: 15px;
    display: flex;
    align-items: flex-start;
    gap: 15px;
    color: var(--text-secondary);
    line-height: 1.5;
}

.feature-benefits li i {
    color: var(--primary);
    margin-top: 4px;
    flex-shrink: 0;
}

.feature-benefits li strong {
    color: var(--text);
    font-weight: 600;
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

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 992px) {
    .hero h1 {
        font-size: 2.8rem;
    }
    
    .detailed-feature {
        flex-direction: column;
        gap: 25px;
        padding: 30px;
    }
    
    .detailed-feature:hover {
        transform: translateY(-5px);
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
    
    .features {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .feature-detail-item {
        font-size: 0.85rem;
    }
}

@media (max-width: 480px) {
    .hero {
        padding: 150px 5% 80px;
    }
    
    .feature-card {
        padding: 25px 20px;
    }
    
    .detailed-feature {
        padding: 20px;
    }
    
    .detailed-feature-content h3 {
        font-size: 1.5rem;
    }
    
    .feature-benefits li {
        font-size: 0.9rem;
    }
}
</style>