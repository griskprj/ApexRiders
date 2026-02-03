<script setup>
    import BasicManualCard from './manuals/BasicManualCard.vue';
    import ManualsCategory from './manuals/ManualsCategory.vue';
    import ManualsHeader from './manuals/ManualsHeader.vue';
    import RecentManuals from './manuals/RecentManuals.vue';
</script>

<template>
    <!-- Декоративные элементы -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    <!-- Страница мануалов -->
    <section class="manuals">
        <!-- Заголовок и фильтры -->
        <ManualsHeader @search="handleSearch" />

        <!-- Боковая панель -->
        <div v-if="manuals.length > 0" class="manuals-sidebar">
            <!-- Категории -->
            <div class="sidebar-card">
                <ManualsCategory 
                    :manuals="manuals",
                    :getCategoryCount="getCategoryCount"
                    :activeFilter="activeFilter"
                    @filter-change="handleFilterChange"
                />
            </div>

            <!-- Недавно просмотренные -->
            <RecentManuals 
                :userManuals="userManuals"
                :formatTime="formatTime"
            />
        </div>

        <!-- Основной контент -->
        <div class="manuals-content" :class="{ 'no-content': manuals.length === 0 }">
            <!-- Сетка мануалов -->
            <div v-if="isLoading" class="manuals-loading">
                <div class="loading-spinner-small"></div>
                <p>Загрузка мануалов...</p>
            </div>
            
            <div v-else-if="filteredManuals.length === 0" class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-book-open"></i>
                </div>
                <h3>{{ searchQuery ? 'По вашему запросу ничего не найдено' : 'По выбранной категории нет мануалов'}}</h3>
                <p>{{ searchQuery ? 'Попробуйте изменить запрос' : 'Попробуйте выбрать другую категорию'}}</p>
                <button class="btn btn-primary" @click="resetFilter">
                    <i class="fas fa-undo"></i> Показать все мануалы
                </button>
            </div>

            <div v-else class="manuals-main">
                <div v-if="searchQuery" class="search-info">
                    <span class="search-results-count">
                        Найдено мануалов: {{ filteredManuals.length }}
                    </span>
                    <button v-if="searchQuery" class="search-clear-btn" @click="clearSearch">
                        <i class="fas fa-times"></i> Очистить поиск
                    </button>
                </div>

                <div v-if="searchQuery && serverSearchMode" class="search-filters">
                    <div class="filter-group">
                        <label>Сложность:</label>
                        <select v-model="searchFilters.difficulty" @change="updateSearchFilter('difficulty', $event.target.value)">
                            <option value="">Все уровни</option>
                            <option value="Начинающий">Начинающий</option>
                            <option value="Средний">Средний</option>
                            <option value="Сложный">Сложный</option>
                            <option value="Эксперт">Эксперт</option>
                        </select>
                    </div>
                    
                    <div class="filter-group">
                        <label>Сортировка:</label>
                        <select v-model="searchFilters.sort_by" @change="updateSearchFilter('sort_by', $event.target.value)">
                            <option value="relevance">По релевантности</option>
                            <option value="newest">Сначала новые</option>
                            <option value="rating">По рейтингу</option>
                            <option value="views">По просмотрам</option>
                        </select>
                    </div>
                    
                    <div class="search-stats" v-if="searchMeta">
                        <span>Найдено: {{ totalUsers || filteredManuals.length }} мануалов</span>
                    </div>
                </div>

                <div class="manuals-grid">
                    <BasicManualCard 
                        :limiterManuals="currentPageManuals",
                    />
                </div>

                <!-- Пагинация -->
                <div v-if="filteredManuals.length > itemsPerPage" class="pagination">
                    <button 
                        class="pagination-btn prev"
                        @click="prevPage"
                        :disabled="currentPage === 1"
                    >
                        <i class="fas fa-chevron-left"></i> Назад
                    </button>
                    <div class="pagination-pages">
                        <button
                            v-for="page in totalPages"
                            :key="page"
                            class="page-btn"
                            :class="{ active: currentPage === page }"
                            @click="goToPage(page)"
                        >
                            {{ page }}
                        </button>
                    </div>
                    <button 
                        class="pagination-btn next"
                        @click="nextPage"
                        :disabled="currentPage === totalPages"
                    >
                        Вперед <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Manuals',
    data() {
        return {
            allManuals: [],
            manuals: [],
            userManuals: [],
            isLoading: true,
            activeFilter: 'all',
            searchQuery: '',
            currentPage: 1,
            itemsPerPage: 6,

            categories: {
                'engine': 'Двигатель',
                'transmission': 'Трансмиссия',
                'brakes': 'Тормозная система',
                'suspension': 'Подвеска',
                'electrics': 'Электрика',
                'maintenance': 'Обслуживание'
            },

            serverSearchMode: true,
            searchFilters: {
                category: '',
                difficulty: '',
                sort_by: 'relevance'
            },
            searchMeta: {}
        }
    },

    computed: {
        filteredManuals() {
            if (this.serverSearchMode) {
                return this.manuals
            }

            // fallback
            let filtered = this.manuals

            if (this.activeFilter !== 'all') {
                const categoryName = this.categories[this.activeFilter]
                filtered = filtered.filter(manual =>
                    manual.category === categoryName || manual.moto_type === categoryName
                )
            }

            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase().trim()
                filtered = filtered.filter(manual =>
                    manual.title.toLowerCase().includes(query) ||
                    manual.description.toLowerCase().includes(query)
                )
            }

            return filtered
        },

        currentPageManuals() {
            const start = (this.currentPage - 1) * this.itemsPerPage
            const end = start + this.itemsPerPage
            return this.filteredManuals.slice(start, end)
        },

        totalPages() {
            return Math.ceil(this.filteredManuals.length / this.itemsPerPage)
        },
        
        limiterManuals() {
            return this.manuals.slice(0, 6)
        },
    },

    mounted() {
        this.fetchManuals()
    },

    watch: {
        activeFilter() {
            this.currentPage = 1
        },

        searchQuery() {
            this.currentPage = 1
        }
    },

    methods: {
        async fetchManuals() {
            try {
                this.isLoading = true
                const token = localStorage.getItem('authToken')

                if (this.serverSearchMode && this.searchQuery) {
                    await this.searchManuals()
                } else {
                    const response = await axios.get('/api/manuals/get', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
    
                    if (response.data) {
                        this.manuals = response.data.manuals_data || []
                        this.userManuals = response.data.user_manuals || []
                        this.allManuals = this.manuals

                        if (this.activeFilter !== 'all') {
                            const categoryName = this.categories[this.activeFilter]
                            this.manuals = this.manuals.filter(manual =>
                                manual.category === categoryName || manual.moto_type === categoryName
                            )
                        }
                    }
                }
                
            } catch (error) {
                console.error('Ошибка при получении мануалов: ', error)
                this.manuals = []
                this.userManuals = []
            } finally {
                this.isLoading = false
            }
        },

        async searchManuals() {
            this.isLoading = true
            try {
                const token = localStorage.getItem('authToken')
                
                const params = new URLSearchParams({
                    page: this.currentPage,
                    per_page: this.itemsPerPage
                })

                if (this.searchQuery) {
                    params.append('q', this.searchQuery)
                }

                if (this.activeFilter !== 'all') {
                    const category_name = this.categories[this.activeFilter]
                    params.append('category', categoryName)
                }

                if (this.searchFilters.difficulty) {
                    params.append('difficulty', this.searchFilters.difficulty)
                }

                if (this.searchFilters.sort_by) {
                    params.append('sort_by', this.searchFilters.sort_by)
                }

                const response = await axios.get(`/api/manuals/search?${params}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data) {
                    this.manuals = response.data.manuals || []
                    this.searchMeta = response.data.search_meta || {}

                    if (response.data.pagination) {
                        const pagination = response.data.pagination
                        this.totalPages = pagination.pages
                        this.totalUsers = pagination.total
                    }
                }
            } catch (error) {
                console.error('Ошибка при поиске мануалов: ', error)
                this.serverSearchMode = false
                this.applyClientSideFilter()
            } finally {
                this.isLoading = false
            }
        },

        applyClientSideFilter() {
            let filtered = this.allManuals || []

            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase().trim()
                filtered = filtered.filter(manual => 
                    manual.title.toLowerCase().includes(query) ||
                    manual.description.toLowerCase().includes(query)
                )
            }

            this.manuals = filtered.slice(0, this.itemsPerPage * this.currentPage)
        },
        
        getCategoryCount(categoryName) {
            return this.manuals.filter(manual =>
                manual.category === categoryName || manual.moto_type === categoryName
            ).length
        },

        handleFilterChange(filterId) {
            this.activeFilter = filterId
            this.currentPage = 1
            if (this.serverSearchMode) {
                this.searchManuals()
            }
        },

        handleSearch(query) {
            this.searchQuery = query
            this.currentPage = 1
            if (this.serverSearchMode) {
                this.searchManuals()
            }
        },

        resetFilter() {
            this.activeFilter = 'all'
            this.searchQuery = ''
            this.currentPage = 1
            if (this.serverSearchMode) {
                this.fetchManuals()
            }
        },

        clearSearch() {
            this.searchQuery = ''
            this.currentPage = 1
            if (this.serverSearchMode) {
                this.fetchManuals()
            }
        },

        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--
                if (this.serverSearchMode) {
                    this.searchManuals()
                }
            }
        },

        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++
                if (this.serverSearchMode) {
                    this.searchManuals()
                }
            }
        },

        goToPage(page) {
            this.currentPage = page
            if (this.serverSearchMode) {
                this.searchManuals()
            }
        },

        updateSearchFilter(filterType, value) {
            this.searchFilters[filterType] = value
            this.currentPage = 1
            if (this.serverSearchMode) {
                this.searchManuals()
            }
        },
        
        formatTime(timeString) {
            if (!timeString) return ''
            const date = new Date(timeString)
            const now = new Date()
            const diff = now - date
            
            const minutes = Math.floor(diff / 60000)
            const hours = Math.floor(minutes / 60)
            const days = Math.floor(hours / 24)
            
            if (minutes < 60) return `${minutes} мин назад`
            if (hours < 24) return `${hours} час назад`
            if (days < 7) return `${days} дн назад`
            return date.toLocaleDateString()
        },

        isManualAuthor (manual) {
            return manual.author_id === current_user_id
        }
    }
}
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ СТРАНИЦЫ МАНУАЛОВ ===== */
.manuals {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

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

/* ===== КОНТЕНТ С ГРИДОМ ===== */
.manuals-content {
    display: flex;
    flex-direction: column;
}

.manuals-content.no-content {
    min-height: 50vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.manuals-main {
    flex: 1;
}

/* ===== ИНФОРМАЦИЯ О ПОИСКЕ ===== */
.search-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 15px 20px;
    background: rgba(255, 69, 0, 0.1);
    border-radius: 10px;
    border-left: 4px solid var(--primary);
}

.search-results-count {
    font-size: 1rem;
    color: var(--text);
    font-weight: 500;
}

.search-info .search-clear-btn {
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 0.9rem;
    color: var(--text);
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    backdrop-filter: blur(10px);
}

.search-info .search-clear-btn:hover {
    background: rgba(255, 69, 0, 0.2);
    border-color: var(--primary);
}

.search-filters {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
    padding: 15px 20px;
    background: var(--dark-light);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    flex-wrap: wrap;
    align-items: center;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.filter-group label {
    color: var(--text-secondary);
    font-size: 14px;
    white-space: nowrap;
}

.filter-group select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    padding: 8px 12px;
    color: var(--text);
    min-width: 150px;
}

.filter-group select:focus {
    outline: none;
    border-color: var(--primary);
}

.search-stats {
    margin-left: auto;
    color: var(--text-secondary);
    font-size: 14px;
}

/* ===== СЕТКА МАНУАЛОВ ===== */
.manuals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 40px;
}

/* ===== СОСТОЯНИЕ ПУСТО ===== */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: var(--dark-light);
    border-radius: 20px;
    border: 2px dashed rgba(255, 255, 255, 0.1);
    margin: 40px 0;
}

.empty-icon {
    font-size: 80px;
    color: var(--text-secondary);
    margin-bottom: 20px;
    opacity: 0.5;
}

.empty-state h3 {
    font-size: 1.8rem;
    font-weight: 300;
    margin-bottom: 10px;
    color: var(--text);
}

.empty-state p {
    color: var(--text-secondary);
    margin-bottom: 30px;
    font-size: 1.1rem;
}

/* ===== ЗАГРУЗКА ===== */
.manuals-loading {
    text-align: center;
    padding: 100px 20px;
    color: var(--text-secondary);
    font-size: 1.1rem;
}

.loading-spinner-small {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    border-top-color: var(--primary);
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
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
}

.search-input::placeholder {
    color: var(--text-secondary);
}

.manual-card {
    background: var(--dark-light);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    position: relative;
    backdrop-filter: blur(10px);
}

.manual-card:hover {
    transform: translateY(-10px);
    border-color: var(--primary-dark);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 69, 0, 0.1);
}

.manual-badge {
    position: absolute;
    top: 15px;
    left: 15px;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 5px;
}

.manual-badge.popular {
    background: rgba(255, 69, 0, 0.9);
    color: white;
}

.manual-image {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.manual-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.manual-card:hover .manual-image img {
    transform: scale(1.05);
}

.manual-content {
    padding: 25px;
}

.manual-category {
    display: inline-block;
    padding: 5px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 10px;
}

.manual-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 12px;
    line-height: 1.4;
}

.manual-desc {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 20px;
    font-size: 0.95rem;
}

.manual-stats {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.stat i {
    color: var(--primary);
}

.btn-block {
    width: 100%;
    text-align: center;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

/* ===== БОКОВАЯ ПАНЕЛЬ ===== */
.manuals-sidebar {
    margin-top: 30px;
}

@media (min-width: 992px) {
    .manuals-content {
        display: grid;
        grid-template-columns: 1fr 300px;
        gap: 30px;
    }
    
    .manuals-sidebar {
        margin-top: 0;
    }
}

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

.upload-card {
    background: linear-gradient(135deg, var(--dark-light) 0%, rgba(255, 69, 0, 0.1) 100%);
    border: 1px solid var(--primary);
    text-align: center;
}

.upload-card p {
    color: var(--text-secondary);
    margin-bottom: 20px;
    font-size: 0.95rem;
}

/* ===== ПАГИНАЦИЯ ===== */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 30px;
    padding-top: 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-btn {
    padding: 12px 24px;
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text);
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
    backdrop-filter: blur(10px);
}

.pagination-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-pages {
    display: flex;
    gap: 8px;
}

.page-btn {
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.page-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.page-btn.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
}

/* ===== ДЕКОРАТИВНЫЕ ЭЛЕМЕНТЫ ===== */
.decoration {
    position: fixed;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    z-index: -1;
}

.decoration-1 {
    background: var(--primary);
    top: 10%;
    right: 5%;
}

.decoration-2 {
    background: var(--accent);
    bottom: 10%;
    left: 5%;
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 768px) {
    .manuals {
        padding: 100px 5% 40px;
    }
    
    .manuals-title {
        font-size: 2.2rem;
    }
    
    .manuals-grid {
        grid-template-columns: 1fr;
    }
    
    .empty-state {
        padding: 40px 20px;
    }
    
    .empty-icon {
        font-size: 60px;
    }
    
    .empty-state h3 {
        font-size: 1.5rem;
    }
}

@media (max-width: 480px) {
    .manuals-title {
        font-size: 1.8rem;
    }
    
    .manual-content {
        padding: 20px;
    }
    
    .manual-stats {
        flex-direction: column;
        gap: 10px;
    }
    
    .page-btn {
        width: 40px;
        height: 40px;
    }
}
</style>