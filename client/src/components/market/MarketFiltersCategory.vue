<template>
    <div class="market-filters">
        <div class="filter-tabs">
            <button 
                class="filter-tab" 
                :class="{ active: activeFilter === 'all' }"
                @click="setFilter('all')"
            >
                Все
            </button>
            <button 
                class="filter-tab" 
                :class="{ active: activeFilter === 'motorcycles' }"
                @click="setFilter('motorcycles')"
            >
                Мотоциклы
            </button>
            <button 
                class="filter-tab" 
                :class="{ active: activeFilter === 'parts' }"
                @click="setFilter('parts')"
            >
                Запчасти
            </button>
            <button 
                class="filter-tab" 
                :class="{ active: activeFilter === 'gear' }"
                @click="setFilter('gear')"
            >
                Экипировка
            </button>
            <button 
                class="filter-tab" 
                :class="{ active: activeFilter === 'my' && user }"
                @click="setFilter('my')"
                v-if="user"
            >
                Мои объявления
            </button>
        </div>
        
        <div class="filter-sort">
            <select v-model="sortBy" @change="handleSort">
                <option value="newest" selected>Сначала новые</option>
                <option value="price_low">Цена (низкая → высокая)</option>
                <option value="price_high">Цена (высокая → низкая)</option>
                <option value="popular">Популярные</option>
            </select>
            <div class="filter-tags">
                <span class="tag" v-for="tag in activeTags" :key="tag">
                    {{ tag }} <i class="fas fa-times" @click="removeTag(tag)"></i>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            activeTags: Array,
            setFilter: Function,
            removeTag: Function
        }
    }
</script>

<style scoped>
    .market-filters {
        background: var(--dark-light);
        border-radius: 15px;
        padding: 25px 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .filter-tabs {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }

    .filter-tab {
        padding: 10px 24px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        color: var(--text-secondary);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .filter-tab:hover {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text);
    }

    .filter-tab.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
    }

    .filter-sort {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }

    .filter-sort select {
        padding: 12px 20px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: var(--text);
        font-size: 1rem;
        min-width: 200px;
        cursor: pointer;
        outline: none;
    }

    .filter-sort select:focus {
        border-color: var(--primary);
    }

    .filter-tags {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .filter-tags .tag {
        padding: 8px 16px;
        background: rgba(255, 69, 0, 0.15);
        border-radius: 20px;
        font-size: 0.9rem;
        color: var(--primary);
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .filter-tags .tag:hover {
        background: rgba(255, 69, 0, 0.25);
    }

    .filter-tags .tag i {
        font-size: 12px;
        cursor: pointer;
    }

    @media (max-width: 768px) {
        .filter-tabs {
            justify-content: center;
        }
        
        .filter-sort {
            flex-direction: column;
            align-items: stretch;
        }
    }

    @media (max-width: 480px) {
        .market-filters {
            padding: 20px;
        }
        
        .filter-tab {
            padding: 8px 16px;
            font-size: 0.9rem;
        }
    }
</style>