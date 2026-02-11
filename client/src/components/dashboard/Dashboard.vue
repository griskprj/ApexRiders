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
                :productActiveCount="productActiveCount",
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
import { ref, computed, onMounted, defineAsyncComponent } from 'vue'
import axios from 'axios'
import { authService } from '../../utils/checkAuth'

const DashboardHeader = defineAsyncComponent(() => 
    import('./DashboardHeader.vue')
)
const DashboardStats = defineAsyncComponent(() => 
    import('./DashboardStats.vue')
)
const QuickActions = defineAsyncComponent(() => 
    import('./QuickActions.vue')
)
const MyCourses = defineAsyncComponent(() => 
    import('./MyCourses.vue')
)
const MyProducts = defineAsyncComponent(() => 
    import('./MyProducts.vue')
)
const SocialActivites = defineAsyncComponent(() => 
    import('./SocialActivites.vue')
)

export default {
    name: 'Dashboard',
    
    components: {
        DashboardHeader,
        DashboardStats,
        QuickActions,
        MyCourses,
        MyProducts,
        SocialActivites
    },

    setup() {
        const manualCount = ref(0)
        const lessonCount = ref(0)
        const postCount = ref(0)
        const productActiveCount = ref(0)
        const answerCount = ref(0)
        const totalLikes = ref(0)
        const products = ref([])
        const courses = ref([])
        const isLoading = ref(true)
        const showLimit = ref(2)

        const limitedProducts = computed(() => {
            return products.value.slice(0, showLimit.value)
        })

        const limitedCourses = computed(() => {
            return courses.value.slice(0, showLimit.value)
        })

        const getStatusText = (product) => {
            if (product.status === 'active') {
                return 'Активно'
            } else if (product.status === 'inactive') {
                return 'На паузе'
            } else if (product.status === 'reserved') {
                return 'Зарезервирован'
            }
            if (product.is_bargain) return 'Торг уместен'
        }

        const fetchDashboardStats = async () => {
            try {
                const token = authService.getToken()
                
                if (!token) {
                    console.error('No authentication token found')
                    throw new Error('No token')
                }
                
                const response = await axios.get('/api/statistic/dashboard', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                if (response.data) {
                    manualCount.value = response.data.manuals_count || 0
                    lessonCount.value = response.data.lessons_count || 0
                    productActiveCount.value = response.data.product_active_count || 0
                    postCount.value = response.data.posts_count || 0
                    answerCount.value = response.data.answer_count || 0
                    totalLikes.value = response.data.total_likes || 0
                    courses.value = response.data.courses || []
                    
                    products.value = response.data.active_product_data || []
                    
                    products.value.sort((a, b) => {
                        if (a.is_active !== b.is_active) {
                            return b.is_active - a.is_active
                        }
                        return new Date(b.date_pub) - new Date(a.date_pub)
                    })
                }
            } catch (error) {
                console.error('Ошибка при получении данных дашборда:', error)
                
                if (error.response && error.response.status === 401) {
                    authService.clearAuth()
                }
                
                manualCount.value = 0
                lessonCount.value = 0
                productActiveCount.value = 0
                postCount.value = 0
                answerCount.value = 0
                totalLikes.value = 0
                products.value = []
                courses.value = []
            }
        }

        const loadDashboardData = async () => {
            isLoading.value = true
            
            try {
                const isAuth = authService.isAuthenticated()
                
                if (isAuth) {
                    await fetchDashboardStats()
                } else {
                    const user = await authService.checkAuth(true)
                    if (user) {
                        await fetchDashboardStats()
                    }
                }
            } catch (error) {
                console.error('Dashboard load error:', error)
            } finally {
                isLoading.value = false
            }
        }

        onMounted(() => {
            loadDashboardData()
        })

        return {
            manualCount,
            lessonCount,
            postCount,
            productActiveCount,
            answerCount,
            totalLikes,
            products,
            courses,
            isLoading,
            showLimit,
            limitedProducts,
            limitedCourses,
            getStatusText,
            fetchDashboardStats,
            loadDashboardData
        }
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