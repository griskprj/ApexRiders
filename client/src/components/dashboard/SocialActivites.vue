<template>
    <div class="dashboard-card community-card">
        <div class="card-header">
            <h3><i class="fas fa-users"></i> Активность в сообществе</h3>
        </div>
        <div class="community-stats">
            <div class="community-stat">
                <div class="stat-value">{{ postCount }}</div>
                <div class="stat-label">Тем создано</div>
            </div>
            <div class="community-stat">
                <div class="stat-value">{{ answerCount }}</div>
                <div class="stat-label">Ответов</div>
            </div>
            <div class="community-stat">
                <div class="stat-value">{{ totalLikes }}</div>
                <div class="stat-label">Лайков</div>
            </div>
        </div>
        <div class="community-actions">
            <a href="/community/new" class="btn btn-outline">
                <i class="fas fa-plus"></i> Новая тема
            </a>
            <a href="/community" class="btn btn-primary">
                <i class="fas fa-comments"></i> К обсуждениям
            </a>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            postCount: Number,
            answerCount: Number,
            totalLikes: Number
        }
    }
</script>

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

    /* ===== СООБЩЕСТВО ===== */
    .community-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 25px;
    }

    .community-stat {
        text-align: center;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
    }

    .community-stat .stat-value {
        font-size: 2rem;
        color: var(--accent);
    }

    .community-stat .stat-label {
        font-size: 0.8rem;
    }

    .community-actions {
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }

    .community-actions .btn {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px 20px;
    }

    @media (max-width: 768px) {
        .community-stats {
            grid-template-columns: repeat(2, 1fr);
        }
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
        
        .course-item {
            flex-direction: column;
            text-align: center;
        }
    }
</style>