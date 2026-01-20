<template>
    <div class="about-page">
        <!-- Главный заголовок -->
        <section class="about-hero">
            <div class="about-hero-bg"></div>
            <h1>О проекте <span class="gradient-text">ApexRiders</span></h1>
            <p class="hero-subtitle">Пространство, где каждый райдер найдёт поддержку, знания и вдохновение</p>
        </section>

        <!-- Основное содержимое -->
        <section class="section about-content">
            <div class="about-intro">
                <h2><i class="fas fa-motorcycle"></i> Что такое ApexRiders?</h2>
                <p><strong>ApexRiders</strong> — это веб‑приложение для мотоциклистов, которое объединяет в одном месте всё необходимое: от технического обслуживания байка до общения с единомышленниками. Наша цель — создать пространство, где каждый райдер найдёт поддержку, знания и вдохновение.</p>
            </div>

            <!-- Инструменты -->
            <div class="about-section">
                <h2 class="section-title">Что вы получаете</h2>
                <p class="section-subtitle">Пять ключевых инструментов для мотоциклиста</p>

                <div class="tools-grid">
                    <div class="tool-card">
                        <div class="tool-icon">
                            <i class="fas fa-tools"></i>
                        </div>
                        <h3>«Гараж»</h3>
                        <p>Планировщик и дневник технического обслуживания мотоцикла. Записывайте ТО, отслеживайте сроки замены расходников и сохраняйте историю работ.</p>
                    </div>

                    <div class="tool-card">
                        <div class="tool-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <h3>«Сообщество»</h3>
                        <p>Небольшая социальная сеть для райдеров. Делитесь опытом, находите попутчиков и обсуждайте всё, что связано с мотокультурой.</p>
                    </div>

                    <div class="tool-card">
                        <div class="tool-icon">
                            <i class="fas fa-graduation-cap"></i>
                        </div>
                        <h3>«Курсы» <span class="badge">в разработке</span></h3>
                        <p>Обучающие материалы для совершенствования навыков. От базовых приёмов до сложных элементов мотоджимханы: выбирайте схему, тренируйтесь на время и получайте обратную связь.</p>
                    </div>

                    <div class="tool-card">
                        <div class="tool-icon">
                            <i class="fas fa-shopping-cart"></i>
                        </div>
                        <h3>«Маркет»</h3>
                        <p>Площадка для покупки и продажи мотоциклов, экипировки и запчастей.</p>
                    </div>

                    <div class="tool-card">
                        <div class="tool-icon">
                            <i class="fas fa-book"></i>
                        </div>
                        <h3>«Мануалы»</h3>
                        <p>База инструкций по ремонту и обслуживанию мототехники. Быстро находите ответы на технические вопросы.</p>
                    </div>
                </div>
            </div>

            <!-- Преимущества -->
            <div class="about-section advantages-section">
                <h2 class="section-title">Почему это удобно</h2>
                <p class="section-subtitle">ApexRiders решает три главные задачи мотоциклистов</p>

                <div class="advantages">
                    <div class="advantage">
                        <div class="advantage-number">01</div>
                        <h3>Организация ТО</h3>
                        <p>Больше не нужно держать сроки замены масла или колодок в голове — приложение напомнит вовремя.</p>
                    </div>

                    <div class="advantage">
                        <div class="advantage-number">02</div>
                        <h3>Доступ к знаниям</h3>
                        <p>Мануалы и будущие курсы помогут разобраться в ремонте и улучшить навыки езды без лишних затрат.</p>
                    </div>

                    <div class="advantage">
                        <div class="advantage-number">03</div>
                        <h3>Связь с сообществом</h3>
                        <p>Найдите тех, кто разделяет вашу страсть к мотоциклам, и делитесь опытом в дружественной атмосфере.</p>
                    </div>
                </div>
            </div>

            <!-- Философия -->
            <div class="about-section philosophy-section">
                <div class="philosophy-content">
                    <h2><i class="fas fa-heart"></i> Наша философия</h2>
                    <div class="philosophy-text">
                        <p>Мотоцикл — это не просто транспорт. Это <strong>культура, свобода и единство</strong>. Когда вы садитесь на байк, вы становитесь частью большого сообщества, где каждый готов поддержать другого.</p>
                        <p class="highlight">ApexRiders создан, чтобы укрепить эту связь: здесь нет места конкуренции — только взаимная помощь и уважение.</p>
                    </div>
                </div>
            </div>

            <!-- История -->
            <div class="about-section history-section">
                <h2 class="section-title">Как всё начиналось</h2>
                
                <div class="history-content">
                    <div class="history-timeline">
                        <div class="timeline-item">
                            <div class="timeline-content">
                                <div class="timeline-year">2 года назад</div>
                                <h3>Начало пути</h3>
                                <p>Проект родился как скромное приложение для учёта ТО и хранения мануалов.</p>
                            </div>
                        </div>
                        
                        <div class="timeline-item">
                            <div class="timeline-year">1 год назад</div>
                            <div class="timeline-content">
                                <h3>Техническое обновление</h3>
                                <p>Переписал код на Vue.js (фронтенд) и Flask (бэкенд), перешёл на PostgreSQL, добавил новые функции.</p>
                            </div>
                        </div>
                        
                        <div class="timeline-item">
                            <div class="timeline-year">Сейчас</div>
                            <div class="timeline-content">
                                <h3>Бета-тестирование</h3>
                                <p>Первый крупный проект, созданный в одиночку. Приложение находится на этапе бета‑теста — возможны недочёты, но мы верим в потенциал и готовы развивать его вместе с вами.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Планы -->
            <div class="about-section plans-section">
                <h2 class="section-title">Что дальше</h2>
                <p class="section-subtitle">Планы развития проекта</p>

                <div class="plans-grid">
                    <div class="plan-card">
                        <i class="fas fa-play-circle"></i>
                        <h4>Запуск обучающих курсов</h4>
                        <p>Система обучения с обратной связью от опытных райдеров.</p>
                    </div>

                    <div class="plan-card">
                        <i class="fas fa-user-shield"></i>
                        <h4>Система модерации</h4>
                        <p>Инструменты для поддержания качества контента в сообществе.</p>
                    </div>

                    <div class="plan-card">
                        <i class="fas fa-cogs"></i>
                        <h4>Админ‑панель</h4>
                        <p>Удобное управление сообществом и контентом.</p>
                    </div>

                    <div class="plan-card">
                        <i class="fas fa-comments"></i>
                        <h4>Обратная связь</h4>
                        <p>Расширение функционала на основе ваших предложений.</p>
                    </div>
                </div>

                <div class="current-status">
                    <h3>Текущий статус проекта</h3>
                    <ul>
                        <li><i class="fas fa-globe"></i> Работает только онлайн</li>
                        <li><i class="fas fa-mobile-alt"></i> Доступно на любых устройствах — от ПК до смартфонов</li>
                        <li><i class="fas fa-gift"></i> Бесплатно в течение ближайших 6 месяцев</li>
                        <li><i class="fas fa-star"></i> В будущем возможны добровольные донаты или премиум‑подписка</li>
                    </ul>
                </div>
            </div>

            <!-- Призыв к действию -->
            <div class="about-section cta-section">
                <div class="cta-content">
                    <h2><i class="fas fa-handshake"></i> Присоединяйтесь!</h2>
                    <p class="cta-text">ApexRiders только начинает свой путь. Мы ищем первых 10 постоянных пользователей, которые помогут нам стать лучше. Ваш отзыв, идея или даже просто присутствие в сообществе — уже огромный вклад в развитие проекта.</p>
                    <p class="cta-highlight">Давайте вместе создавать пространство, где мотокультура живёт и растёт!</p>
                    
                    <div class="cta-buttons">
                        <router-link to="/register" class="btn btn-primary">
                            <i class="fas fa-user-plus"></i> Стать частью сообщества
                        </router-link>
                        <a href="mailto:apexriders@yandex.ru" class="btn btn-outline">
                            <i class="fas fa-envelope"></i> Связаться с создателем
                        </a>
                    </div>
                    
                    <div class="ps-note">
                        <p><i class="fas fa-asterisk"></i> <strong>P.S.</strong> Если хотите поддержать проект или предложить сотрудничество — пишите. Я открыт к диалогу!</p>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'AboutPage',
    mounted() {
        window.scrollTo(0, 0);
    }
}
</script>

<style scoped>
.about-page {
    position: relative;
    min-height: 100vh;
    padding-bottom: 50px;
}

/* Герой секция - улучшенная */
.about-hero {
    padding: 180px 5% 120px;
    text-align: center;
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, 
        rgba(0, 0, 0, 0.9) 0%, 
        rgba(10, 25, 47, 0.95) 50%, 
        rgba(0, 0, 0, 0.9) 100%);
}

.about-hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(ellipse at 20% 20%, rgba(0, 191, 255, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(255, 69, 0, 0.1) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(0, 191, 255, 0.08) 0%, transparent 70%);
    z-index: 0;
}

.about-hero h1 {
    font-size: 3.8rem;
    font-weight: 800;
    margin-bottom: 25px;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    line-height: 1.1;
}

.gradient-text {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 50%, var(--warning) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    position: relative;
    display: inline-block;
}

.gradient-text::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--primary), transparent);
    border-radius: 2px;
}

.hero-subtitle {
    font-size: 1.4rem;
    color: var(--text-secondary);
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
    font-weight: 300;
    letter-spacing: 0.5px;
    position: relative;
    z-index: 1;
    opacity: 0.9;
}

/* Улучшенные заголовки секций */
.section-title {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 15px;
    position: relative;
    display: inline-block;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, var(--text) 0%, var(--text-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    border-radius: 2px;
}

.section-subtitle {
    font-size: 1.2rem;
    color: var(--text-secondary);
    margin-bottom: 40px;
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* Основной контент */
.about-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 5% 100px;
}

.about-intro {
    background: linear-gradient(135deg, var(--dark-light), rgba(0, 191, 255, 0.05));
    border-radius: 25px;
    padding: 50px;
    margin-bottom: 80px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.about-intro::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary), transparent);
}

.about-intro h2 {
    font-size: 2.3rem;
    margin-bottom: 25px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 15px;
    font-weight: 700;
}

.about-intro h2 i {
    color: var(--primary);
    font-size: 1.8rem;
    background: rgba(0, 191, 255, 0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.about-intro p {
    font-size: 1.15rem;
    line-height: 1.8;
    color: var(--text-secondary);
    letter-spacing: 0.2px;
}

/* Инструменты - улучшены */
.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 35px;
    margin-top: 50px;
}

.tool-card {
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.03) 0%, 
        rgba(255, 255, 255, 0.01) 100%);
    border-radius: 20px;
    padding: 35px 30px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.tool-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, 
        rgba(0, 191, 255, 0.05) 0%, 
        rgba(255, 69, 0, 0.02) 100%);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.tool-card:hover {
    transform: translateY(-10px) scale(1.02);
    border-color: var(--primary-dark);
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.4),
        0 0 0 1px rgba(0, 191, 255, 0.1);
}

.tool-card:hover::before {
    opacity: 1;
}

.tool-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--primary-light), rgba(0, 191, 255, 0.2));
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: var(--primary);
    margin-bottom: 25px;
    transition: all 0.3s ease;
}

.tool-card:hover .tool-icon {
    transform: rotateY(180deg) scale(1.1);
    background: linear-gradient(135deg, var(--primary), var(--accent));
}

.tool-card h3 {
    font-size: 1.4rem;
    margin-bottom: 15px;
    color: var(--text);
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.badge {
    background: linear-gradient(135deg, var(--warning), #ff9900);
    color: var(--dark);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(255, 165, 0, 0.3);
}

.tool-card p {
    color: var(--text-secondary);
    line-height: 1.7;
    font-size: 1rem;
    letter-spacing: 0.1px;
}

/* Улучшенные преимущества с яркими номерами */
.advantages-section {
    background: linear-gradient(135deg, 
        rgba(0, 0, 0, 0.3) 0%, 
        rgba(10, 25, 47, 0.4) 100%);
    border-radius: 25px;
    padding: 70px 40px;
    margin: 80px 0;
    border: 1px solid rgba(255, 255, 255, 0.08);
    position: relative;
    overflow: hidden;
}

.advantages-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary), transparent);
}

.advantages {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 50px;
    margin-top: 50px;
}

.advantage {
    text-align: center;
    padding: 35px 25px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
    position: relative;
}

.advantage:hover {
    transform: translateY(-5px);
    border-color: var(--primary-dark);
    background: rgba(255, 255, 255, 0.05);
}

.advantage-number {
    font-size: 4.5rem;
    font-weight: 900;
    margin-bottom: 20px;
    background: linear-gradient(135deg, 
        rgba(255, 69, 0, 0.8) 0%, 
        rgba(255, 140, 0, 0.6) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    text-shadow: 0 10px 30px rgba(255, 69, 0, 0.3);
    position: relative;
    display: inline-block;
}

.advantage-number::after {
    content: '';
    position: absolute;
    bottom: 10px;
    left: 10%;
    width: 80%;
    height: 3px;
    background: linear-gradient(90deg, transparent, rgba(255, 69, 0, 0.5), transparent);
    border-radius: 2px;
}

.advantage h3 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: var(--text);
    font-weight: 600;
    letter-spacing: 0.5px;
}

.advantage p {
    color: var(--text-secondary);
    line-height: 1.7;
    font-size: 1.05rem;
    max-width: 300px;
    margin: 0 auto;
}

/* Философия */
.philosophy-section {
    background: linear-gradient(135deg, 
        rgba(255, 69, 0, 0.08) 0%, 
        rgba(0, 191, 255, 0.08) 100%);
    border-radius: 25px;
    padding: 60px;
    margin: 80px 0;
    border: 1px solid rgba(255, 69, 0, 0.15);
    position: relative;
    overflow: hidden;
}

.philosophy-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ff4500' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
    opacity: 0.5;
}

.philosophy-content {
    position: relative;
    z-index: 1;
}

.philosophy-content h2 {
    font-size: 2.3rem;
    margin-bottom: 30px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 15px;
    font-weight: 700;
}

.philosophy-content h2 i {
    color: var(--danger);
    font-size: 1.8rem;
    background: rgba(255, 69, 0, 0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.philosophy-text p {
    font-size: 1.15rem;
    line-height: 1.8;
    margin-bottom: 25px;
    color: var(--text-secondary);
    letter-spacing: 0.2px;
}

.philosophy-text .highlight {
    background: linear-gradient(135deg, 
        rgba(255, 69, 0, 0.1) 0%, 
        rgba(0, 191, 255, 0.05) 100%);
    padding: 30px;
    border-radius: 20px;
    border-left: 4px solid var(--primary);
    font-size: 1.25rem;
    color: var(--text);
    font-style: italic;
    line-height: 1.7;
    margin-top: 20px;
    position: relative;
    overflow: hidden;
}

/* Исправленный и улучшенный Timeline */
.history-section {
    padding: 80px 0;
    position: relative;
}

.history-timeline {
    position: relative;
    max-width: 900px;
    margin: 60px auto 0;
    padding-left: 40px;
}

.history-timeline::before {
    content: '';
    position: absolute;
    left: 25px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        var(--primary) 10%, 
        var(--accent) 50%, 
        var(--primary) 90%, 
        transparent 100%);
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
}

.timeline-item {
    position: relative;
    margin-bottom: 60px;
    display: flex;
    flex-direction: column;
}

.timeline-year {
    font-weight: 800;
    color: var(--primary);
    font-size: 1.3rem;
    margin-bottom: 15px;
    padding-left: 50px;
    position: relative;
    letter-spacing: 1px;
}

.timeline-year::before {
    position: absolute;
    left: -40px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    background: var(--primary);
    border-radius: 50%;
    box-shadow: 
        0 0 0 5px rgba(0, 191, 255, 0.2),
        0 0 20px rgba(0, 191, 255, 0.5);
    z-index: 2;
    transition: all 0.3s ease;
}

.timeline-item:hover .timeline-year::before {
    background: var(--accent);
    transform: translateY(-50%) scale(1.2);
    box-shadow: 
        0 0 0 8px rgba(255, 69, 0, 0.2),
        0 0 30px rgba(255, 69, 0, 0.6);
}

.timeline-content {
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.04) 0%, 
        rgba(255, 255, 255, 0.01) 100%);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-left: 50px;
    position: relative;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.timeline-content:hover {
    transform: translateX(10px);
    border-color: rgba(0, 191, 255, 0.3);
    box-shadow: 
        0 15px 40px rgba(0, 0, 0, 0.3),
        0 0 0 1px rgba(0, 191, 255, 0.1);
}

.timeline-content::before {
    content: '';
    position: absolute;
    left: -15px;
    top: 30px;
    width: 30px;
    height: 30px;
    background: var(--primary);
    transform: rotate(45deg);
    border-radius: 6px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
}

.timeline-content h3 {
    font-size: 1.4rem;
    margin-bottom: 15px;
    color: var(--text);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
}

.timeline-content h3::before {
    content: '';
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
}

.timeline-content p {
    color: var(--text-secondary);
    line-height: 1.7;
    font-size: 1.05rem;
    letter-spacing: 0.1px;
}

/* Планы */
.plans-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: 30px;
    margin: 50px 0 70px;
}

.plan-card {
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.04) 0%, 
        rgba(255, 255, 255, 0.01) 100%);
    border-radius: 20px;
    padding: 30px 25px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.plan-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0, 191, 255, 0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.plan-card:hover {
    transform: translateY(-10px);
    border-color: var(--accent);
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.3),
        0 0 0 1px rgba(0, 191, 255, 0.2);
}

.plan-card:hover::before {
    opacity: 1;
}

.plan-card i {
    font-size: 2.8rem;
    color: var(--accent);
    margin-bottom: 25px;
    transition: all 0.3s ease;
}

.plan-card:hover i {
    transform: scale(1.2) rotate(5deg);
}

.plan-card h4 {
    font-size: 1.3rem;
    margin-bottom: 15px;
    color: var(--text);
    font-weight: 600;
}

.plan-card p {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.6;
    letter-spacing: 0.1px;
}

.current-status {
    background: linear-gradient(135deg, var(--dark-light), rgba(0, 191, 255, 0.05));
    border-radius: 20px;
    padding: 35px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.current-status::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, 
        transparent 0%, 
        rgba(0, 191, 255, 0.03) 100%);
}

.current-status h3 {
    font-size: 1.6rem;
    margin-bottom: 25px;
    color: var(--text);
    font-weight: 600;
    position: relative;
}

.current-status ul {
    list-style: none;
    padding: 0;
    position: relative;
}

.current-status li {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 20px;
    color: var(--text-secondary);
    font-size: 1.08rem;
    line-height: 1.6;
    padding-left: 10px;
    position: relative;
}

.current-status li::before {
    content: '✓';
    color: var(--success);
    font-weight: bold;
    font-size: 1.1rem;
    min-width: 25px;
    text-align: center;
}

.current-status li i {
    color: var(--primary);
    min-width: 30px;
    font-size: 1.2rem;
    margin-top: 2px;
}

/* Призыв к действию - улучшенный */
.cta-section {
    background: linear-gradient(135deg, 
        rgba(0, 191, 255, 0.1) 0%, 
        rgba(255, 69, 0, 0.08) 100%);
    border-radius: 25px;
    padding: 70px 40px;
    margin-top: 80px;
    text-align: center;
    border: 1px solid rgba(255, 69, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.cta-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%2300bfff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
    opacity: 0.3;
}

.cta-content {
    position: relative;
    z-index: 1;
}

.cta-content h2 {
    font-size: 2.4rem;
    margin-bottom: 25px;
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    font-weight: 700;
}

.cta-content h2 i {
    color: var(--success);
    font-size: 1.8rem;
    background: rgba(0, 255, 0, 0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.cta-text {
    font-size: 1.15rem;
    line-height: 1.8;
    max-width: 800px;
    margin: 0 auto 30px;
    color: var(--text-secondary);
    letter-spacing: 0.2px;
}

.cta-highlight {
    font-size: 1.35rem;
    color: var(--text);
    margin: 0 auto 45px;
    font-weight: 600;
    max-width: 800px;
    line-height: 1.6;
    background: linear-gradient(135deg, 
        transparent 0%, 
        rgba(0, 191, 255, 0.1) 100%);
    padding: 25px;
    border-radius: 15px;
    border-left: 4px solid var(--success);
}

.cta-buttons {
    display: flex;
    gap: 25px;
    justify-content: center;
    margin-bottom: 45px;
    flex-wrap: wrap;
}

.cta-buttons .btn {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 18px 35px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 12px;
    transition: all 0.3s ease;
    min-width: 250px;
    justify-content: center;
}

.cta-buttons .btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border: none;
    box-shadow: 0 10px 25px rgba(0, 191, 255, 0.3);
}

.cta-buttons .btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(0, 191, 255, 0.4);
}

.cta-buttons .btn-outline {
    border: 2px solid var(--primary);
    color: var(--primary);
    background: transparent;
}

.cta-buttons .btn-outline:hover {
    background: rgba(0, 191, 255, 0.1);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 191, 255, 0.2);
}

.ps-note {
    background: linear-gradient(135deg, 
        rgba(0, 0, 0, 0.4) 0%, 
        rgba(255, 165, 0, 0.05) 100%);
    border-radius: 15px;
    padding: 25px;
    max-width: 800px;
    margin: 0 auto;
    border-left: 4px solid var(--warning);
    position: relative;
    overflow: hidden;
}

.ps-note p {
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.7;
    display: flex;
    align-items: flex-start;
    gap: 15px;
    position: relative;
    z-index: 1;
}

.ps-note i {
    color: var(--warning);
    margin-top: 5px;
    font-size: 1.2rem;
}

/* Адаптивность */
@media (max-width: 992px) {
    .about-hero h1 {
        font-size: 3rem;
    }
    
    .section-title {
        font-size: 2.4rem;
    }
    
    .history-timeline {
        padding-left: 30px;
    }
    
    .history-timeline::before {
        left: 20px;
    }
    
    .timeline-year {
        padding-left: 40px;
    }
    
    .timeline-year::before {
        left: -30px;
    }
    
    .timeline-content {
        margin-left: 40px;
    }
    
    .timeline-content::before {
        left: -10px;
        width: 20px;
        height: 20px;
    }
}

@media (max-width: 768px) {
    .about-hero {
        padding: 150px 5% 80px;
    }
    
    .about-hero h1 {
        font-size: 2.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
    }
    
    .section-title {
        font-size: 2.2rem;
    }
    
    .about-intro,
    .philosophy-section,
    .advantages-section,
    .cta-section {
        padding: 40px 25px;
    }
    
    .tools-grid,
    .plans-grid {
        grid-template-columns: 1fr;
        gap: 25px;
    }
    
    .advantages {
        grid-template-columns: 1fr;
        gap: 30px;
    }
    
    .cta-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .cta-buttons .btn {
        width: 100%;
        max-width: 300px;
    }
    
    .timeline-item {
        margin-bottom: 40px;
    }
    
    .timeline-content {
        padding: 25px;
    }
}

@media (max-width: 480px) {
    .about-hero {
        padding: 120px 5% 60px;
    }
    
    .about-content {
        padding: 0 5% 60px;
    }
    
    .about-hero h1 {
        font-size: 2.2rem;
    }
    
    .section-title {
        font-size: 1.9rem;
    }
    
    .about-intro h2,
    .philosophy-content h2,
    .cta-content h2 {
        font-size: 1.8rem;
    }
    
    .advantage {
        padding: 25px 20px;
    }
    
    .advantage-number {
        font-size: 3.5rem;
    }
    
    .plan-card {
        padding: 25px 20px;
    }
    
    .cta-buttons .btn {
        padding: 16px 25px;
        font-size: 1rem;
    }
    
    .history-timeline {
        padding-left: 20px;
    }
    
    .timeline-year::before {
        width: 16px;
        height: 16px;
    }
    
    .timeline-content {
        margin-left: 30px;
        padding: 20px;
    }
}
</style>