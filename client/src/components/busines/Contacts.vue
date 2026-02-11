<template>
    <div class="contacts-page">
        <div class="decoration decoration-1"></div>
        <div class="decoration decoration-2"></div>
        
        <div class="contacts-header">
            <h1><i class="fas fa-envelope-open-text"></i> Контакты</h1>
            <p class="contacts-subtitle">Мы всегда на связи с нашим сообществом</p>
        </div>
        
        <div class="contacts-content">
            <div class="contacts-card">
                <div class="intro-section">
                    <p class="intro-text">
                        Здравствуйте! Мы всегда рады обратной связи от наших пользователей. 
                        Ниже — способы связаться с командой ApexRiders.
                    </p>
                </div>
                
                <!-- Основные каналы связи -->
                <section class="channels-section">
                    <h2><span class="section-icon"><i class="fas fa-comments"></i></span> Основные каналы связи</h2>
                    
                    <div class="channels-grid">
                        <div class="channel-card email">
                            <div class="channel-header">
                                <div class="channel-icon">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <h3>Электронная почта</h3>
                            </div>
                            
                            <div class="channel-body">
                                <div class="contact-detail">
                                    <i class="fas fa-at"></i>
                                    <div>
                                        <h4>Для общих вопросов, предложений и жалоб:</h4>
                                        <p class="contact-address">apexriders@yandex.ru</p>
                                    </div>
                                </div>
                                
                                <div class="contact-info">
                                    <h4><i class="fas fa-info-circle"></i> Рекомендации:</h4>
                                    <ul>
                                        <li>Укажите в теме письма суть обращения (например: «Предложение по функционалу», «Жалоба на пользователя», «Подтверждение статуса»)</li>
                                        <li>Мы отвечаем в течение <strong>1–3 рабочих дней</strong></li>
                                    </ul>
                                </div>
                                
                                <div class="response-time">
                                    <i class="fas fa-clock"></i>
                                    <span>Время ответа: 1-3 рабочих дня</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="channel-card telegram">
                            <div class="channel-header">
                                <div class="channel-icon">
                                    <i class="fab fa-telegram"></i>
                                </div>
                                <h3>Telegram</h3>
                            </div>
                            
                            <div class="channel-body">
                                <div class="contact-detail">
                                    <i class="fas fa-paper-plane"></i>
                                    <div>
                                        <h4>Для оперативного общения:</h4>
                                        <p class="contact-address">@griskyy</p>
                                    </div>
                                </div>
                                
                                <div class="contact-info">
                                    <h4><i class="fas fa-check-circle"></i> Подходит для:</h4>
                                    <ul>
                                        <li>Подтверждения статуса пользователя (отправьте фото с мотоциклом, телефон и ник на сервисе)</li>
                                        <li>Срочных вопросов по работе платформы</li>
                                        <li>Оперативной консультации</li>
                                    </ul>
                                </div>
                                
                                <div class="response-time">
                                    <i class="fas fa-clock"></i>
                                    <span>Время ответа: в пределах 24 часов (кроме выходных)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                
                <!-- Частые вопросы -->
                <section class="faq-section">
                    <h2><span class="section-icon"><i class="fas fa-question-circle"></i></span> Частые вопросы</h2>
                    
                    <div class="faq-grid">
                        <div class="faq-item">
                            <div class="faq-question">
                                <i class="fas fa-user-check"></i>
                                <h4>Как подтвердить статус пользователя?</h4>
                            </div>
                            <p class="faq-answer">
                                Отправьте на почту или в Telegram: фото с мотоциклом, номер телефона и ваш ник на сервисе
                            </p>
                        </div>
                        
                        <div class="faq-item">
                            <div class="faq-question">
                                <i class="fas fa-book"></i>
                                <h4>Где найти инструкцию по публикации мануала?</h4>
                            </div>
                            <p class="faq-answer">
                                Инструкция доступна в разделе «Мануалы» после подтверждения статуса пользователя
                            </p>
                        </div>
                        
                        <div class="faq-item">
                            <div class="faq-question">
                                <i class="fas fa-flag"></i>
                                <h4>Как подать жалобу на объявление или комментарий?</h4>
                            </div>
                            <p class="faq-answer">
                                Отправьте ссылку на материал и скриншоты на почту с темой «Жалоба на контент»
                            </p>
                        </div>
                        
                        <div class="faq-item">
                            <div class="faq-question">
                                <i class="fas fa-bullhorn"></i>
                                <h4>Правила размещения рекламы в сообществе?</h4>
                            </div>
                            <p class="faq-answer">
                                Только после согласования с администрацией. Укажите название организации без призывов к действию
                            </p>
                        </div>
                        
                        <div class="faq-item">
                            <div class="faq-question">
                                <i class="fas fa-bug"></i>
                                <h4>Технические проблемы (ошибки, медленная загрузка и т. п.)?</h4>
                            </div>
                            <p class="faq-answer">
                                Опишите проблему подробно, укажите устройство и браузер. Приложите скриншоты ошибки
                            </p>
                        </div>
                    </div>
                </section>
                
                <!-- Важная информация -->
                <section class="important-section">
                    <h2><span class="section-icon"><i class="fas fa-exclamation-triangle"></i></span> Важно</h2>
                    
                    <div class="important-cards">
                        <div class="important-card">
                            <div class="important-header">
                                <i class="fas fa-store"></i>
                                <h3>Раздел «Маркет»</h3>
                            </div>
                            <p>
                                Для решения вопросов по сделкам в разделе «Маркет» (объявления о продаже) обращайтесь 
                                напрямую к продавцу — сервис не участвует в расчётах и доставке.
                            </p>
                        </div>
                        
                        <div class="important-card">
                            <div class="important-header">
                                <i class="fas fa-shield-alt"></i>
                                <h3>Сообщения о нарушениях</h3>
                            </div>
                            <p>
                                Если вы сообщаете о нарушении правил (спам, оскорбления, запрещённый контент), 
                                приложите <strong>скриншоты</strong> или ссылки на проблемные материалы.
                            </p>
                        </div>
                        
                        <div class="important-card">
                            <div class="important-header">
                                <i class="fas fa-gavel"></i>
                                <h3>Апелляции на блокировки</h3>
                            </div>
                            <p>
                                Апелляции на блокировки аккаунтов отправляйте на <strong>apexriders@yandex.ru</strong> 
                                с темой «Апелляция: [ваш ник]».
                            </p>
                        </div>
                    </div>
                </section>
                
                <!-- Юридическая информация -->
                <section class="legal-section">
                    <h2><span class="section-icon"><i class="fas fa-balance-scale"></i></span> Юридическая информация</h2>
                    
                    <div class="legal-info">
                        <div class="legal-item">
                            <i class="fas fa-server"></i>
                            <div>
                                <h4>Адрес сервера</h4>
                                <p>Санкт‑Петербург, РФ</p>
                            </div>
                        </div>
                        
                        <div class="legal-item">
                            <i class="fas fa-scale-balanced"></i>
                            <div>
                                <h4>Законодательство</h4>
                                <p>Сервис работает в соответствии с законодательством РФ</p>
                            </div>
                        </div>
                        
                        <div class="legal-item">
                            <i class="fas fa-file-contract"></i>
                            <div>
                                <h4>Документы</h4>
                                <p>Политика конфиденциальности и правила пользования размещены в разделе «Помощь»</p>
                            </div>
                        </div>
                    </div>
                </section>
                
                <!-- Заключительная часть -->
                <div class="closing-section">
                    <div class="closing-content">
                        <i class="fas fa-heart"></i>
                        <div>
                            <h3>Мы ценим ваше участие в развитии ApexRiders!</h3>
                            <p>Спасибо, что делаете наше сообщество лучше.</p>
                        </div>
                    </div>
                    <p class="team-signature">Команда ApexRiders</p>
                </div>
                
                <!-- Действия -->
                <div class="action-buttons">
                    <router-link to="/community-rules" class="btn btn-outline">
                        <i class="fas fa-book"></i> Правила сообщества
                    </router-link>
                    <router-link to="/about" class="btn btn-outline">
                        <i class="fas fa-info-circle"></i> О проекте
                    </router-link>
                    <a href="mailto:apexriders@yandex.ru" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i> Написать нам
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>

<style scoped>
.contacts-page {
    padding: 140px 5% 80px;
    position: relative;
    min-height: 100vh;
    background: transparent;
}

/* Декор */
.decoration {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.1;
    z-index: -1;
}

.decoration-1 {
    background: var(--primary);
    top: 10%;
    right: 10%;
}

.decoration-2 {
    background: var(--accent);
    bottom: 10%;
    left: 10%;
}

/* Заголовок */
.contacts-header {
    text-align: center;
    margin-bottom: 50px;
}

.contacts-header h1 {
    font-size: 2.8rem;
    color: var(--text);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.contacts-header h1 i {
    color: var(--primary);
    font-size: 2.5rem;
}

.contacts-subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
    opacity: 0.8;
}

/* Основной контент */
.contacts-content {
    max-width: 1200px;
    margin: 0 auto;
}

.contacts-card {
    background: rgba(20, 20, 30, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

/* Вступление */
.intro-section {
    text-align: center;
    margin-bottom: 50px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.intro-text {
    font-size: 1.2rem;
    line-height: 1.7;
    color: var(--text-secondary);
    max-width: 800px;
    margin: 0 auto;
}

/* Разделы */
section {
    margin-bottom: 60px;
    scroll-margin-top: 120px;
}

section h2 {
    color: var(--text);
    font-size: 1.8rem;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 15px;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.section-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: rgba(255, 69, 0, 0.1);
    color: var(--primary);
    border-radius: 50%;
    font-size: 1.2rem;
}

/* Каналы связи */
.channels-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
    margin-top: 20px;
}

.channel-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.channel-card:hover {
    border-color: var(--primary);
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(255, 69, 0, 0.1);
}

.channel-card.email:hover {
    border-color: var(--primary);
}

.channel-card.telegram:hover {
    border-color: var(--accent);
}

.channel-header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 25px 30px;
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.channel-icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
}

.email .channel-icon {
    background: rgba(255, 69, 0, 0.1);
    color: var(--primary);
}

.telegram .channel-icon {
    background: rgba(0, 191, 255, 0.1);
    color: var(--accent);
}

.channel-header h3 {
    color: var(--text);
    font-size: 1.3rem;
    margin: 0;
}

.channel-body {
    padding: 30px;
}

.contact-detail {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border-left: 4px solid var(--primary);
}

.contact-detail i {
    font-size: 1.5rem;
    color: var(--primary);
    flex-shrink: 0;
}

.contact-detail h4 {
    color: var(--text-secondary);
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 5px;
}

.contact-address {
    color: var(--text);
    font-size: 1.2rem;
    font-weight: 600;
    word-break: break-all;
}

.contact-info {
    margin-top: 25px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
}

.contact-info h4 {
    color: var(--text);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.1rem;
}

.contact-info ul {
    padding-left: 25px;
}

.contact-info li {
    margin-bottom: 10px;
    line-height: 1.6;
    color: var(--text-secondary);
}

.response-time {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 25px;
    padding: 15px;
    background: rgba(255, 165, 0, 0.1);
    border-radius: 8px;
    color: var(--warning);
    font-weight: 500;
}

.response-time i {
    font-size: 1.2rem;
}

/* Частые вопросы */
.faq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.faq-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 20px;
    transition: all 0.3s ease;
}

.faq-item:hover {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.05);
    transform: translateY(-3px);
}

.faq-question {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}

.faq-question i {
    color: var(--primary);
    font-size: 1.2rem;
    flex-shrink: 0;
}

.faq-question h4 {
    color: var(--text);
    font-size: 1.1rem;
    margin: 0;
}

.faq-answer {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
    padding-left: 35px;
}

/* Важная информация */
.important-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    margin-top: 20px;
}

.important-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 25px;
    transition: all 0.3s ease;
}

.important-card:hover {
    border-color: var(--warning);
    background: rgba(255, 165, 0, 0.05);
}

.important-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.important-header i {
    font-size: 1.5rem;
    color: var(--warning);
}

.important-header h3 {
    color: var(--text);
    font-size: 1.2rem;
    margin: 0;
}

.important-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
}

/* Юридическая информация */
.legal-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.legal-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    transition: all 0.3s ease;
}

.legal-item:hover {
    border-color: var(--accent);
    background: rgba(0, 191, 255, 0.05);
    transform: translateY(-3px);
}

.legal-item i {
    font-size: 1.8rem;
    color: var(--accent);
    flex-shrink: 0;
}

.legal-item h4 {
    color: var(--text);
    margin-bottom: 5px;
    font-size: 1.1rem;
}

.legal-item p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0;
}

/* Заключительная часть */
.closing-section {
    text-align: center;
    padding: 40px;
    background: rgba(255, 69, 0, 0.05);
    border-radius: 15px;
    margin: 50px 0;
    border: 1px solid rgba(255, 69, 0, 0.2);
}

.closing-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 20px;
}

.closing-content i {
    font-size: 2.5rem;
    color: var(--primary);
}

.closing-content h3 {
    color: var(--text);
    font-size: 1.4rem;
    margin-bottom: 10px;
}

.closing-content p {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

.team-signature {
    color: var(--text);
    font-size: 1.2rem;
    font-weight: 600;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Кнопки действий */
.action-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 40px;
    padding-top: 40px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 12px 25px;
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
    transform: translateY(-2px);
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

/* Адаптивность */
@media (max-width: 992px) {
    .contacts-page {
        padding: 120px 5% 60px;
    }
    
    .contacts-header h1 {
        font-size: 2.2rem;
    }
    
    .contacts-card {
        padding: 30px;
    }
    
    .channels-grid,
    .important-cards,
    .legal-info {
        grid-template-columns: 1fr;
    }
    
    .action-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .btn {
        width: 100%;
        max-width: 300px;
        justify-content: center;
    }
}

@media (max-width: 768px) {
    .contacts-page {
        padding: 100px 5% 40px;
    }
    
    .contacts-header h1 {
        font-size: 1.8rem;
    }
    
    .contacts-card {
        padding: 20px;
    }
    
    section h2 {
        font-size: 1.5rem;
    }
    
    .closing-content {
        flex-direction: column;
        text-align: center;
    }
    
    .faq-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .contacts-header h1 {
        font-size: 1.5rem;
    }
    
    .contacts-subtitle {
        font-size: 0.95rem;
    }
    
    .channel-body,
    .contact-detail,
    .contact-info {
        padding: 15px;
    }
    
    .contact-address {
        font-size: 1rem;
    }
}
</style>