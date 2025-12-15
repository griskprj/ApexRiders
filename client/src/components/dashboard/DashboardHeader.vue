<template>
    <div class="dashboard-header">
        <h1 class="dashboard-title">
            <i class="fas fa-tachometer-alt"></i>
            <span>Мой дашборд</span>
        </h1>
        <div class="user-welcome">
            <div class="user-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="user-info">
                <h2>Добро пожаловать!</h2>
                <p>Ваша активность и статистика</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .dashboard-header {
        margin-bottom: 40px;
    }

    .dashboard-title {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 30px;
        color: var(--text);
    }

    .dashboard-title i {
        color: var(--primary);
        text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
    }

    .user-welcome {
        display: flex;
        align-items: center;
        gap: 20px;
        background: var(--dark-light);
        padding: 25px 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .user-avatar {
        width: 70px;
        height: 70px;
        background: var(--primary-light);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: var(--primary);
    }

    .user-info h2 {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 5px;
    }

    .user-info p {
        color: var(--text-secondary);
        font-size: 1rem;
    }
</style>