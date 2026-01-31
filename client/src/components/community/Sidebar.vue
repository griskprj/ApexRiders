<template>
    <!-- Боковая панель -->
    <div class="sidebar">
        <!-- Активные пользователи -->
        <div class="sidebar-card users-card">
            <h3 class="sidebar-title">
                <i class="fas fa-trophy"></i>
                Активные пользователи
            </h3>
            <div class="users-list">
                <div 
                    v-for="user in activeUsers" 
                    :key="user.id"
                    class="user-item"
                >
                    <div class="user-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="user-info">
                        <div class="user-name">{{ user.name }}</div>
                        <div class="user-posts">{{ user.posts }} постов</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        activeUsers: Array
    }
}
</script>

<style scoped>
/* ===== БОКОВАЯ ПАНЕЛЬ ===== */
.sidebar {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.sidebar-card {
    background: var(--dark-light);
    border-radius: 15px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.2rem;
    margin-bottom: 20px;
    color: var(--text);
}

.sidebar-title i {
    color: var(--primary);
}

/* Пользователи */
.users-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.user-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

.user-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--text-secondary);
}

.user-info {
    flex: 1;
}

.user-name {
    font-weight: 500;
    font-size: 0.95rem;
}

.user-posts {
    font-size: 0.85rem;
    color: var(--text-secondary);
}
</style>