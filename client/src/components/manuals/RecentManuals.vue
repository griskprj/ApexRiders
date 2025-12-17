<template>
    <div v-if="userManuals.length > 0" class="sidebar-card">
        <h3 class="sidebar-title">
            <i class="fas fa-history"></i>
            Недавно просмотренные
        </h3>
        <div class="recent-list">
            <a v-for="item in userManuals" :key="item.id" href="#" class="recent-item">
                <div class="recent-icon">
                    <i class="fas fa-motorcycle"></i>
                </div>
                <div class="recent-info">
                    <div class="recent-title">{{ item.title }}</div>
                    <div class="recent-time">{{ formatTime(item.viewed_at) }}</div>
                </div>
            </a>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            userManuals: Array,
            formatTime: Function
        }
    }
</script>

<style scoped>
    .sidebar-card {
        background: var(--dark-light);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
    }

    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: var(--text);
    }

    .sidebar-title i {
        color: var(--primary);
    }

    .recent-list {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .recent-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 12px 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        text-decoration: none;
        color: var(--text);
        transition: all 0.3s ease;
    }

    .recent-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }

    .recent-icon {
        width: 40px;
        height: 40px;
        background: var(--primary-light);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary);
        font-size: 1.1rem;
    }

    .recent-title {
        font-weight: 500;
        margin-bottom: 3px;
    }

    .recent-time {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
</style>