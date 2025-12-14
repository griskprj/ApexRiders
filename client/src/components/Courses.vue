<template>
    <!-- Декоративные элементы -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>
    <div class="decoration decoration-3"></div>

    <!-- Страница курсов -->
    <section class="courses-page">
        <!-- Заголовок и фильтры -->
        <div class="courses-header">
            <h1 class="courses-title">
                <i class="fas fa-graduation-cap"></i>
                <span>Курсы по мотоциклам</span>
            </h1>
            <p class="courses-subtitle">Изучайте техники вождения, обслуживание и безопасность</p>
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="Поиск курсов..." 
                        class="search-input"
                    >
                </div>
        </div>

        <!-- Все курсы -->
        <div class="all-courses-content">
            <!-- Сетка курсов -->
            <div v-if="isLoading" class="courses-loading">
                <div class="loading-spinner-small"></div>
                <p>Загркузка всех курсов...</p>
            </div>
            <div v-else-if="courses.length === 0">
                <h2 class="section-title">
                    <i class="fas fa-book"></i>
                    Все курсы
                </h2>
                <div class="empty-state">
                    <div class="empty-icon">
                        <i class="fas fa-book"></i>
                    </div>
                    <h3>Пока что тут пусто</h3>
                    <p>Начните обучение из представленных выше курсов!</p>
                </div>
            </div>

            <div v-else class="courses-grid">
                <!-- Карточка курса 1 -->
                <div class="course-card" v-for="course in courses" :key="course.id">
                    <div class="course-badge" :class="course.level">
                        {{ course.level }}
                    </div>
                    
                    <div class="course-image">
                        <i :class="course.ico"></i>
                    </div>
                    
                    <div class="course-content">
                        <h3 class="course-title">{{ course.title }}</h3>
                        <p class="course-description">{{ course.description }}</p>
                        
                        <div class="course-meta">
                            <div class="meta-item">
                                <i class="fas fa-play-circle"></i>
                                <span>{{ course.lessons }} уроков</span>
                            </div>
                            <div class="meta-item">
                                <i class="fas fa-signal"></i>
                                <span>{{ course.level }}</span>
                            </div>
                        </div>
                        
                        <div class="course-actions">
                            <button 
                                class="btn btn-primary btn-sm"
                                @click="startCourse(course.id)"
                            >
                                <i class="fas fa-play"></i> Начать курс
                            </button>
                            
                            <button class="btn btn-outline btn-sm" @click="viewDetails(course.id)">
                                Подробнее
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    
        <!-- Мои активные курсы -->
        <div class="my-courses-section" v-if="userCourses.length > 0">
            <h2 class="section-title">
                <i class="fas fa-book-open"></i>
                Мои активные курсы
            </h2>
            
            <div class="active-courses-grid">
                <div class="active-course-card" v-for="course in userCourses" :key="course.id">
                    <div class="active-course-header">
                        <h3>{{ course.title }}</h3>
                        <span class="course-progress-badge">{{ course.progress }}%</span>
                    </div>
                    
                    <div class="active-course-progress">
                        <div class="progress-bar large">
                            <div class="progress-fill" :style="{ width: course.progress + '%' }"></div>
                        </div>
                    </div>
                    
                    <button class="btn btn-primary btn-block" @click="continueCourse(course.id)">
                        <i class="fas fa-play"></i> Продолжить обучение
                    </button>
                </div>
            </div>
        </div>
        <div v-else-if="userCourses.length === 0">
            <h2 class="section-title">
                <i class="fas fa-book-open"></i>
                Мои активные курсы
            </h2>
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-book-open"></i>
                </div>
                <h3>Пока что тут пусто</h3>
                <p>Начните обучение из представленных выше курсов!</p>
            </div>
        </div>

        <!-- Рекомендуемые курсы -->
        <div>
            <h2 class="section-title">
                <i class="fas fa-star"></i>
                Рекомендуемые курсы
            </h2>
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-star"></i>
                </div>
                <h3>Пока что тут пусто</h3>
                <p>Скоро здесь появятся лучшие из лучших курсов!</p>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Courses',
    data () {
        return {
            courses: [],
            userCourses: [],
            isLoading: true,
        }
    },

    computed: {
        limitedCourses() {
            return this.courses.slice(0, 6)
        },
    },

    mounted() {
        this.fetchCourses()
    },

    methods: {
        async fetchCourses() {
            try {
                const token = localStorage.getItem('authToken')

                const response = await axios.get('/api/courses/get', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data) {
                    this.courses = response.data.all_courses || []
                    this.userCourses = response.data.user_courses || []
                }
            } catch (error) {
                console.error('Ошибка при получении мануалов', error)
                this.courses = []
                this.userCourses = []
            } finally {
                this.isLoading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ СТРАНИЦЫ КУРСОВ ===== */
.courses-page {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

.courses-header {
    margin-bottom: 40px;
}

.courses-title {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 10px;
    color: var(--text);
}

.courses-title i {
    color: var(--primary);
    text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
}

.courses-subtitle {
    color: var(--text-secondary);
    font-size: 1.2rem;
    margin-bottom: 30px;
}

/* ===== ФИЛЬТРЫ И ПОИСК ===== */
.courses-filters {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
    background: var(--dark-light);
    padding: 20px 30px;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.filter-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.filter-btn {
    padding: 8px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.filter-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.filter-btn.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.search-box {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    padding: 10px 20px;
    min-width: 300px;
}

.search-box i {
    color: var(--text-secondary);
    margin-right: 10px;
}

.search-input {
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font-size: 1rem;
    width: 100%;
}

.search-input::placeholder {
    color: var(--text-secondary);
}

/* ===== СЕТКА КУРСОВ ===== */
.courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 60px;
}

.course-card {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.course-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary-dark);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
}

.course-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    z-index: 1;
}

.course-badge.beginner {
    background: rgba(0, 191, 255, 0.15);
    color: var(--accent);
    border: 1px solid rgba(0, 191, 255, 0.3);
}

.course-badge.intermediate {
    background: rgba(255, 215, 0, 0.15);
    color: gold;
    border: 1px solid rgba(255, 215, 0, 0.3);
}

.course-badge.advanced {
    background: rgba(255, 69, 0, 0.15);
    color: var(--primary);
    border: 1px solid rgba(255, 69, 0, 0.3);
}

.course-image {
    width: 80px;
    height: 80px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    font-size: 32px;
    color: var(--primary);
}

.course-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--text);
}

.course-description {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-bottom: 20px;
    line-height: 1.5;
}

.course-meta {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.meta-item i {
    color: var(--primary);
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
.courses-loading {
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

/* ===== ПРОГРЕСС-БАР ===== */
.course-progress {
    margin-bottom: 20px;
}

.progress-bar {
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 5px;
}

.progress-bar.large {
    height: 10px;
    border-radius: 5px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), #ff6b35);
    border-radius: 3px;
    transition: width 0.5s ease;
}

.progress-text {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ===== КНОПКИ ДЕЙСТВИЙ ===== */
.course-actions {
    display: flex;
    gap: 10px;
}

.btn-sm {
    padding: 8px 20px;
    font-size: 0.9rem;
}

.btn-block {
    width: 100%;
}

.btn-success {
    background: limegreen;
    border-color: limegreen;
    color: white;
}

.btn-success:hover {
    background: #32cd32;
    border-color: #32cd32;
}

/* ===== МОИ АКТИВНЫЕ КУРСЫ ===== */
.my-courses-section {
    margin-bottom: 60px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 2rem;
    font-weight: 300;
    margin-bottom: 30px;
    color: var(--text);
}

.section-title i {
    color: var(--primary);
}

.active-courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 25px;
}

.active-course-card {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.active-course-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.active-course-header h3 {
    font-size: 1.3rem;
    font-weight: 600;
}

.course-progress-badge {
    background: var(--primary);
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

.active-course-info {
    margin: 20px 0;
}

.info-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.info-item .label {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.info-item .value {
    color: var(--text);
    font-weight: 500;
}

/* ===== РЕКОМЕНДУЕМЫЕ КУРСЫ ===== */
.recommended-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}

.recommended-card {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    position: relative;
    transition: all 0.3s ease;
}

.recommended-card:hover {
    transform: translateY(-5px);
    border-color: var(--accent);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 191, 255, 0.1);
}

.recommended-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(255, 69, 0, 0.15);
    color: var(--primary);
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 5px;
}

.recommended-content h3 {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--text);
}

.recommended-content p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-bottom: 20px;
    line-height: 1.5;
}

.recommended-rating {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.stars {
    display: flex;
    gap: 2px;
}

.stars i {
    color: rgba(255, 255, 255, 0.2);
    font-size: 0.9rem;
}

.stars i.filled {
    color: gold;
}

.rating-text {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

/* ===== ДОПОЛНИТЕЛЬНЫЕ ДЕКОРАТИВНЫЕ ЭЛЕМЕНТЫ ===== */
.decoration-3 {
    position: fixed;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    filter: blur(50px);
    opacity: 0.1;
    z-index: -1;
    background: gold;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 1200px) {
    .courses-grid,
    .active-courses-grid,
    .recommended-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .courses-page {
        padding: 100px 5% 40px;
    }
    
    .courses-filters {
        flex-direction: column;
        align-items: stretch;
    }
    
    .search-box {
        min-width: auto;
    }
    
    .filter-buttons {
        justify-content: center;
    }
    
    .courses-grid,
    .active-courses-grid,
    .recommended-grid {
        grid-template-columns: 1fr;
    }
    
    .courses-title {
        font-size: 2rem;
    }
    
    .section-title {
        font-size: 1.5rem;
    }
}

@media (max-width: 480px) {
    .course-card,
    .active-course-card,
    .recommended-card {
        padding: 20px;
    }
    
    .course-actions {
        flex-direction: column;
    }
    
    .btn-sm {
        width: 100%;
    }
    
    .filter-buttons {
        flex-direction: column;
    }
    
    .filter-btn {
        width: 100%;
        text-align: center;
    }
}
</style>