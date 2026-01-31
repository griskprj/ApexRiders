<template>
    <!-- Пагинация -->
    <div v-if="filteredPosts.length > 0" class="pagination">
        <button 
            class="pagination-btn"
            :disabled="currentPage === 1"
            @click="$emit('page-change', currentPage - 1)"
        >
            <i class="fas fa-chevron-left"></i>
            Назад
        </button>
        
        <div class="page-numbers">
            <span 
                v-for="page in visiblePages" 
                :key="page"
                :class="['page-number', { active: currentPage === page }]"
                @click="$emit('page-change', page)"
            >
                {{ page }}
            </span>
        </div>
        
        <button 
            class="pagination-btn"
            :disabled="currentPage === totalPages"
            @click="$emit('page-change', currentPage + 1)"
        >
            Вперед
            <i class="fas fa-chevron-right"></i>
        </button>
    </div>
</template>

<script>
export default {
    name: 'PostsPaginate',
    props: {
        filteredPosts: Array,
        currentPage: Number,
        totalPages: Number
    },
    computed: {
        visiblePages() {
            const pages = [];
            const maxVisible = 5; // Максимальное количество видимых страниц
            
            let start = Math.max(1, this.currentPage - 2);
            let end = Math.min(this.totalPages, start + maxVisible - 1);
            
            // Корректировка начала, если мы в конце списка
            if (end - start + 1 < maxVisible) {
                start = Math.max(1, end - maxVisible + 1);
            }
            
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            
            return pages;
        }
    },
    emits: ['page-change']
}
</script>

<style scoped>
/* ===== ПАГИНАЦИЯ ===== */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 40px;
}

.pagination-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    color: var(--text);
    cursor: pointer;
    transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-numbers {
    display: flex;
    gap: 10px;
}

.page-number {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}

.page-number:hover {
    background: rgba(255, 255, 255, 0.1);
}

.page-number.active {
    background: var(--primary);
    color: white;
}
</style>