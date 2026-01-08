<template>
    <div class="manuals-header">
        <h1 class="manuals-title">
            <i class="fas fa-book"></i>
            <span>Мануалы по ремонту</span>
        </h1>
        <p class="manuals-subtitle">Подробные руководства по обслуживанию и ремонту мотоциклов</p>
        
        <div class="manuals-controls">
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input 
                    type="text" 
                    class="search-input"
                    placeholder="Поиск по названию мануала..." 
                    v-model="searchQuery"
                    @input="handleSearch"
                >
                <button
                    v-if="searchQuery"
                    class="search-clear-btn"
                    @click="clearSearch"
                >
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <router-link to="/create-manual" class="btn btn-primary">
                <i class="fas fa-plus"></i> Создать мануал
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ManualsHeader',
    emits: ['search'],
    data() {
        return {
            searchQuery: ''
        }
    },
    
    methods: {
        handleSearch() {
            clearTimeout(this.searchTimeout)
            this.searchTimeout = setTimeout(() => {
                this.$emit('search', this.searchQuery.trim())
            }, 300)
        },

        clearSearch() {
            this.searchQuery = ''
            this.$emit('search', '')
        }
    }
}
</script>

<style scoped>
    .manuals-header {
        margin-bottom: 40px;
    }

    .manuals-title {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 2.8rem;
        font-weight: 300;
        margin-bottom: 15px;
        color: var(--text);
    }

    .manuals-title i {
        color: var(--primary);
        text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
    }

    .manuals-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 30px;
        max-width: 600px;
    }

    .manuals-controls {
        display: flex;
        gap: 15px;
        align-items: center;
        flex-wrap: wrap;
    }

    .search-box {
        position: relative;
        max-width: 600px;
    }

    .search-box i {
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-secondary);
        font-size: 1.1rem;  
        z-index: 20;
    }

    .search-input {
        width: 100%;
        padding: 18px 20px 18px 50px;
        background: var(--dark-light);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        font-size: 1rem;
        color: var(--text);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);    
    }

    .search-input:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.2);
        padding-right: 50px;
    }

    .search-input::placeholder {
        color: var(--text-secondary);
    }

    .search-clear-btn {
        position: absolute;
        right: 40px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 5px;
        font-size: 1.1rem;
        transition: color 0.3s ease;
        z-index: 2;
    }

    .search-clear-btn:hover {
        color: var(--text);
    }

    @media (max-width: 768px) {
        .manuals-controls {
            flex-direction: column;
            align-items: stretch;
        }
    }
</style>