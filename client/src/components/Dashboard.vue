<script setup>
    import DashboardHeader from './dashboard/DashboardHeader.vue';
    import DashboardStats from './dashboard/DashboardStats.vue';
    import QuickActions from './dashboard/QuickActions.vue';
    import MyCourses from './dashboard/MyCourses.vue';
</script>

<template>
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    <section class="dashboard">
         <DashboardHeader />
        

        <div class="dashboard-grid">
            <!-- Статистика пользователя -->
            <DashboardStats 
                :manualCount="manualCount"
                :lessonCount="lessonCount"
                :postCount="postCount"
                :productActiveCount="productActiveCount"
            />

            <!-- Быстрый доступ -->
            <QuickActions />

            <!-- Мои курсы -->
            <MyCourses 
                :courses="courses"
            />

            <!-- Объявления с маркета -->
            <div class="dashboard-card market-card">
                <div class="card-header">
                    <h3><i class="fas fa-shopping-cart"></i> Мои объявления</h3>
                    <a href="/market" class="card-link">В маркет →</a>
                </div>

                <div v-if="isLoading" class="market-loading">
                    <div class="loading-spinner-small"></div>
                    <p>Загрузка объявлений...</p>
                </div>
                <div v-else-if="products.length === 0" class="no-products">
                    <i class="fas fa-box-open"></i>
                    <p>У вас пока нет объявлений</p>
                </div>

                <div v-else class="market-list">
                    <div v-for="product in limitedProdcuts" :key="product.id" class="market-item">
                        <div class="market-status" :class="{
                            'active': product.is_active,
                            'inactive': !product.is_active,
                            'bargain': product.is_bargain
                        }"
                        >
                            <i class="fas fa-check-circle"></i>
                            {{ getStatusText(product) }}
                        </div>
                        <div class="market-title">{{ product.title }}</div>
                        <div class="market-price">{{ product.cost }} ₽</div>
                        <div class="market-views">
                            <i class="fas fa-eye"></i> {{ product.watchs }} просмотра
                        </div>
                    </div>
                </div>
            </div>

            <!-- Сообщество -->
            <div class="dashboard-card community-card">
                <div class="card-header">
                    <h3><i class="fas fa-users"></i> Активность в сообществе</h3>
                </div>
                <div class="community-stats">
                    <div class="community-stat">
                        <div class="stat-value">{{ postCount }}</div>
                        <div class="stat-label">Тем создано</div>
                    </div>
                    <div class="community-stat">
                        <div class="stat-value">{{ answerCount }}</div>
                        <div class="stat-label">Ответов</div>
                    </div>
                    <div class="community-stat">
                        <div class="stat-value">{{ totalLikes }}</div>
                        <div class="stat-label">Лайков</div>
                    </div>
                </div>
                <div class="community-actions">
                    <a href="/community/new" class="btn btn-outline">
                        <i class="fas fa-plus"></i> Новая тема
                    </a>
                    <a href="/community" class="btn btn-primary">
                        <i class="fas fa-comments"></i> К обсуждениям
                    </a>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Dashboard',

    data() {
        return {
            manualCount: 0,
            lessonCount: 0,
            postCount: 0,
            productActiveCount: 0,
            answerCount: 0,
            totalLikes: 0,

            products: [],
            courses: [],
            isLoading: true,
            showLimit: 2,

        }
    },

    computed: {
        limitedProdcuts() {
            return this.products.slice(0, this.showLimit)
        },
        limitedCourses() {
            return this.courses.slice(0, this.showLimit)
        }
    },

    mounted() {
        this.fetchDashboardStats()
    },

    methods: {
        async fetchDashboardStats() {
            try {
                const token = localStorage.getItem('authToken')

                const response = await axios.get('/api/statistic/dashboard', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data) {
                    this.manualCount = response.data.manuals_count || 0
                    this.lessonCount = response.data.lessons_count || 0
                    this.productActiveCount = response.data.product_active_count || 0
                    this.postCount = response.data.posts_count || 0
                    this.answerCount = response.data.answer_count || 0
                    this.totalLikes = response.data.total_likes || 0
                    this.courses = response.data.courses || []

                    this.products = response.data.active_product_data || []

                    this.products.sort((a, b) => {
                        if (a.is_active !== b.is_active) {
                            return b.is_active - a.is_active
                        }
                        return new Date(b.date_pub) - new Date(a.date_pub)
                    })
                }
            } catch (error) {
                console.error('Ошибка при получении количества мануалов: ', error)
            } finally {
                this.isLoading = false
            }
        },

        getStatusText(product) {
            if (product.is_active) return 'На паузе'
            if (product.is_bargain) return 'Торг уместен'
            return 'Активно'
        },
    }
}
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ ДАШБОРДА ===== */
.dashboard {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

/* ===== СЕТКА ДАШБОРДА ===== */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
}

.dashboard-card {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.dashboard-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary-dark);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.4rem;
    font-weight: 600;
}

.card-header i {
    color: var(--primary);
}

.card-badge {
    background: var(--primary);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.card-link {
    color: var(--primary);
    text-decoration: none;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}

.card-link:hover {
    gap: 5px;
}

/* ===== МАРКЕТ ===== */
.market-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.market-item {
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border-left: 4px solid var(--primary);
}

.market-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 12px;
    background: rgba(0, 255, 0, 0.1);
    color: limegreen;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-bottom: 10px;
}

.market-title {
    font-weight: 600;
    margin-bottom: 10px;
    font-size: 1.1rem;
}

.market-price {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 10px;
}

.market-views {
    font-size: 0.85rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 5px;
}

.market-loading, .no-products {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-secondary);
}

.no-products i {
    font-size: 48px;
    color: var(--text-secondary);
    margin-bottom: 15px;
    opacity: 0.5;
}

.no-products p {
    margin-bottom: 20px;
}

/* ===== СООБЩЕСТВО ===== */
.community-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}

.community-stat {
    text-align: center;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
}

.community-stat .stat-value {
    font-size: 2rem;
    color: var(--accent);
}

.community-stat .stat-label {
    font-size: 0.8rem;
}

.community-actions {
    display: flex;
    gap: 15px;
    margin-top: 20px;
}

.community-actions .btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 20px;
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

/* ==== СПИННЕР ЗАГРУЗКИ ==== */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    background: var(--dark-light);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.loading-spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 1200px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .dashboard {
        padding: 100px 5% 40px;
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .dashboard-title {
        font-size: 2rem;
    }
    
    .user-welcome {
        flex-direction: column;
        text-align: center;
        padding: 20px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .community-stats {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .community-actions {
        flex-direction: column;
    }
}

@media (max-width: 480px) {
    .dashboard-card {
        padding: 20px;
    }
    
    .card-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
    
    .card-header h3 {
        font-size: 1.2rem;
    }
    
    .course-item {
        flex-direction: column;
        text-align: center;
    }
}
</style>