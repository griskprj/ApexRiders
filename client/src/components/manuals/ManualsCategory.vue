<template>
    <h3 class="sidebar-title">
        <i class="fas fa-list"></i>
        Категории
    </h3>
    <div class="category-list">
        <button
            class="category-item"
            :class="{ active: activeFilter === 'all' }"
            @click="$emit('filter-change', 'all')"
        >
            <span class="category-name">Все мануалы</span>
            <span class="category-count">{{ manuals.length }}</span>
        </button>

        <button
            class="category-item"
            v-for="category in categories"
            :key="category.id"
            :class="{ active: activeFilter === category.id }"
            @click="$emit('filter-change', category.id)"
        >
            <span class="category-name">{{ category.name }}</span>
            <span class="category-count">{{ getCategoryCount(category.name) }}</span>
        </button>
    </div>
</template>

<script>
    export default {
        props: {
            manuals: Array,
            getCategoryCount: Function,
            activeFilter: String
        },
        data() {
            return {
                categories: [
                    { 'id': 'engine', name: 'Двигатель' },
                    { 'id': 'transmission', name: 'Трансмиссия' },
                    { 'id': 'brakes', name: 'Тормозная система' },
                    { 'id': 'suspension', name: 'Подвеска' },
                    { 'id': 'electronics', name: 'Электроника' },
                    { 'id': 'maintenance', name: 'Обслуживание' },
                ]
            }
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
        border-width: 0px;
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