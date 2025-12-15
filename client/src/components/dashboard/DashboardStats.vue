<template>
    <div class="dashboard-card stat-card">
        <div class="card-header">
            <h3><i class="fas fa-chart-line"></i> Моя статистика</h3>
            <span class="card-badge">Сегодня</span>
        </div>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{{ manualCount }}</div>
                <div class="stat-label">Просмотрено мануалов</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ lessonCount }}</div>
                <div class="stat-label">Пройдено уроков</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ postCount }}</div>
                <div class="stat-label">Постов в сообществе</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ productActiveCount }}</div>
                <div class="stat-label">Активных объявлений</div>
            </div>
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

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }

    .stat-item {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        transition: all 0.3s ease;
    }

    .stat-item:hover {
        background: rgba(255, 69, 0, 0.1);
        transform: scale(1.05);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 5px;
    }

    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
</style>

<script>
    export default {
        props: {
            manualCount: Number,
            lessonCount: Number,
            postCount: Number,
            productActiveCount: Number,
        }
    }
</script>