<script setup>
    import DashboardHeader from './dashboard/DashboardHeader.vue';
    import DashboardStats from './dashboard/DashboardStats.vue';
    import QuickActions from './dashboard/QuickActions.vue';
    import MyCourses from './dashboard/MyCourses.vue';
    import MyProducts from './dashboard/MyProducts.vue';
    import SocialActivites from './dashboard/SocialActivites.vue';
</script>

<template>
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    <loading v-model:active="isLoading"
        :can-cancel="false"
        :is-full-page="true"
    />

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
            <MyProducts 
                :products="limitedProducts",
                :getStatusText="getStatusText"
            />

            <!-- Сообщество -->
            <SocialActivites 
                :postCount="postCount",
                :answerCount="answerCount"
                :totalLikes="totalLikes"
            />
        </div>
    </section>
</template>

<script>
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/css/index.css'
import axios from 'axios'

export default {
    components: { Loading },
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
            isLoading: false,
            showLimit: 2,

        }
    },

    computed: {
        limitedProducts() {
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
            this.isLoading = true
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