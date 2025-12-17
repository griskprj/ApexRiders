<template>
    <h3 class="sidebar-title">
        <i class="fas fa-list"></i>
        Категории
    </h3>
    <div class="category-list">
        <a href="#" class="category-item active">
            <span class="category-name">Все мануалы</span>
            <span class="category-count">{{ manuals.length }}</span>
        </a>
        <a href="#" class="category-item">
            <span class="category-name">Двигатель</span>
            <span class="category-count">{{ getCategoryCount('Двигатель') }}</span>
        </a>
        <a href="#" class="category-item">
            <span class="category-name">Трансмиссия</span>
            <span class="category-count">{{ getCategoryCount('Трансмиссия') }}</span>
        </a>
    </div>
</template>

<script>
    export default {
        props: {
            manuals: Array,
            getCategoryCount: Function
        }
    }
</script>

<style scoped>
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

    .category-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .category-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        text-decoration: none;
        transition: all 0.3s ease;
        color: var(--text);
    }

    .category-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }

    .category-item.active {
        background: var(--primary-light);
        border-left: 4px solid var(--primary);
    }

    .category-name {
        font-weight: 500;
    }

    .category-count {
        background: rgba(255, 255, 255, 0.1);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        min-width: 30px;
        text-align: center;
    }

    .category-item.active .category-count {
        background: var(--primary);
        color: white;
    }
</style>