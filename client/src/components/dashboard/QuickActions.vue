<template>
    <div class="dashboard-card quick-access">
        <div class="card-header">
            <h3><i class="fas fa-bolt"></i> Быстрый доступ</h3>
        </div>
        <div class="quick-links">
            <a href="/manuals" class="quick-link">
                <div class="quick-icon" style="background: rgba(255, 69, 0, 0.15);">
                    <i class="fas fa-book" style="color: var(--primary);"></i>
                </div>
                <div class="quick-text">
                    <div class="quick-title">Мануалы</div>
                    <div class="quick-desc">Руководства по ремонту</div>
                </div>
            </a>
            <a href="/courses" class="quick-link">
                <div class="quick-icon" style="background: rgba(0, 191, 255, 0.15);">
                    <i class="fas fa-graduation-cap" style="color: var(--accent);"></i>
                </div>
                <div class="quick-text">
                    <div class="quick-title">Курсы</div>
                    <div class="quick-desc">Продолжить обучение</div>
                </div>
            </a>
            <a href="/market" class="quick-link">
                <div class="quick-icon" style="background: rgba(50, 205, 50, 0.15);">
                    <i class="fas fa-shopping-cart" style="color: limegreen;"></i>
                </div>
                <div class="quick-text">
                    <div class="quick-title">Маркет</div>
                    <div class="quick-desc">Мои объявления</div>
                </div>
            </a>
            <a href="/community" class="quick-link">
                <div class="quick-icon" style="background: rgba(255, 215, 0, 0.15);">
                    <i class="fas fa-users" style="color: gold;"></i>
                </div>
                <div class="quick-text">
                    <div class="quick-title">Сообщество</div>
                    <div class="quick-desc">Новые обсуждения</div>
                </div>
            </a>
        </div>
    </div>
</template>

<style scoped>
    .dashboard-card {
        background: var(--dark-light);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary-dark);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .card-header h3 {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.4rem;
        font-weight: 600;
    }

    .card-header i {
        color: var(--primary);
    }

    .card-badge {
        background: var(--primary);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .card-link {
        color: var(--primary);
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .card-link:hover {
        gap: 5px;
    }

    .quick-links {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .quick-link {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .quick-link:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }

    .quick-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    .quick-title {
        font-weight: 600;
        margin-bottom: 3px;
    }

    .quick-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }

    @media (max-width: 480px) {
        .card-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 10px;
        }
        
        .card-header h3 {
            font-size: 1.2rem;
        }
    }
</style>