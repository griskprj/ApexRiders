<template>
    <!-- Заголовок и фильтры -->
    <div class="community-header">
        <div class="header-main">
            <h1 class="community-title">
                <i class="fas fa-users"></i>
                <span>Сообщество мотоциклистов</span>
            </h1>
            <p class="community-subtitle">Общайтесь, делитесь опытом и находите единоммысленников</p>
        </div>
        
        <div class="header-controls">
            <div class="filters">
                <button 
                    v-for="filter in filters" 
                    :key="filter.id"
                    @click="handleFilterClick(filter.id)"
                    :class="['filter-btn', { active: activeFilter === filter.id }]"
                >
                    <i :class="filter.icon"></i>
                    {{ filter.label }}
                </button>
            </div>
            
            <button class="btn btn-primary create-post-btn" @click="handleCreatePost">
                <i class="fas fa-plus"></i>
                Создать пост
            </button>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
    filters: {
        type: Array,
        required: true,
        default: () => [
            { id: 'all', label: 'Все посты', icon: 'fas fa-globe' },
            { id: 'popular', label: 'Популярные', icon: 'fas fa-fire' },
            { id: 'recent', label: 'Новые', icon: 'fas fa-clock' },
            { id: 'my', label: 'Мои посты', icon: 'fas fa-user' }
        ]
    },
    activeFilter: {
        type: String,
        default: 'all'
    }
})

const emit = defineEmits(['filter-change', 'create-post'])

const handleFilterClick = (filterId) => {
    emit('filter-change', filterId)
}

const handleCreatePost = () => {
    emit('create-post')
}
</script>

<style scoped>
    .community-header {
        margin-bottom: 40px;
    }

    .header-main {
        margin-bottom: 30px;
    }

    .community-title {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 10px;
        color: var(--text);
    }

    .community-title i {
        color: var(--primary);
        text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
    }

    .community-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }

    .header-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }

    .filters {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .filter-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        color: var(--text-secondary);
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .filter-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text);
    }

    .filter-btn.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
    }

    .create-post-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 25px;
    }
</style>