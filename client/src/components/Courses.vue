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
            
            <div class="courses-filters">
                <div class="filter-buttons">
                    <button class="filter-btn active" @click="setFilter('all')">Все курсы</button>
                    <button class="filter-btn" @click="setFilter('beginner')">Для начинающих</button>
                    <button class="filter-btn" @click="setFilter('advanced')">Продвинутые</button>
                    <button class="filter-btn" @click="setFilter('technique')">Техника вождения</button>
                    <button class="filter-btn" @click="setFilter('maintenance')">Обслуживание</button>
                </div>
                
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
        </div>

        <!-- Сетка курсов -->
        <div class="courses-grid">
            <!-- Карточка курса 1 -->
            <div class="course-card" v-for="course in filteredCourses" :key="course.id">
                <div class="course-badge" :class="course.level">
                    {{ course.level === 'beginner' ? 'Для начинающих' : 
                       course.level === 'advanced' ? 'Продвинутый' : 'Средний уровень' }}
                </div>
                
                <div class="course-image">
                    <i :class="course.icon"></i>
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
                            <i class="fas fa-clock"></i>
                            <span>{{ course.duration }}</span>
                        </div>
                        <div class="meta-item">
                            <i class="fas fa-signal"></i>
                            <span>{{ course.difficulty }}</span>
                        </div>
                    </div>
                    
                    <div class="course-progress" v-if="course.progress">
                        <div class="progress-bar">
                            <div class="progress-fill" :style="{ width: course.progress + '%' }"></div>
                        </div>
                        <span class="progress-text">{{ course.progress }}% завершено</span>
                    </div>
                    
                    <div class="course-actions">
                        <button 
                            v-if="course.progress && course.progress < 100"
                            class="btn btn-primary btn-sm"
                            @click="continueCourse(course.id)"
                        >
                            <i class="fas fa-play"></i> Продолжить
                        </button>
                        <button 
                            v-else-if="course.progress === 100"
                            class="btn btn-success btn-sm"
                        >
                            <i class="fas fa-check"></i> Завершено
                        </button>
                        <button 
                            v-else
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

        <!-- Мои активные курсы -->
        <div class="my-courses-section" v-if="activeCourses.length > 0">
            <h2 class="section-title">
                <i class="fas fa-book-open"></i>
                Мои активные курсы
            </h2>
            
            <div class="active-courses-grid">
                <div class="active-course-card" v-for="course in activeCourses" :key="course.id">
                    <div class="active-course-header">
                        <h3>{{ course.title }}</h3>
                        <span class="course-progress-badge">{{ course.progress }}%</span>
                    </div>
                    
                    <div class="active-course-progress">
                        <div class="progress-bar large">
                            <div class="progress-fill" :style="{ width: course.progress + '%' }"></div>
                        </div>
                    </div>
                    
                    <div class="active-course-info">
                        <div class="info-item">
                            <span class="label">Последний урок:</span>
                            <span class="value">{{ course.lastLesson }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Следующий урок:</span>
                            <span class="value">{{ course.nextLesson }}</span>
                        </div>
                    </div>
                    
                    <button class="btn btn-primary btn-block" @click="continueCourse(course.id)">
                        <i class="fas fa-play"></i> Продолжить обучение
                    </button>
                </div>
            </div>
        </div>

        <!-- Рекомендуемые курсы -->
        <div class="recommended-section">
            <h2 class="section-title">
                <i class="fas fa-star"></i>
                Рекомендуемые курсы
            </h2>
            
            <div class="recommended-grid">
                <div class="recommended-card" v-for="course in recommendedCourses" :key="course.id">
                    <div class="recommended-badge">
                        <i class="fas fa-fire"></i> Популярный
                    </div>
                    
                    <div class="recommended-content">
                        <h3>{{ course.title }}</h3>
                        <p>{{ course.description }}</p>
                        
                        <div class="recommended-rating">
                            <div class="stars">
                                <i class="fas fa-star" v-for="n in 5" :key="n" 
                                   :class="{ filled: n <= course.rating }"></i>
                            </div>
                            <span class="rating-text">{{ course.rating }}/5 ({{ course.reviews }} отзывов)</span>
                        </div>
                        
                        <button class="btn btn-primary btn-block" @click="startCourse(course.id)">
                            Начать курс
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'Courses',
    data() {
        return {
            searchQuery: '',
            currentFilter: 'all',
            courses: [
                {
                    id: 1,
                    title: 'Базовое вождение',
                    description: 'Основы управления мотоциклом, старт и остановка, переключение передач',
                    icon: 'fas fa-motorcycle',
                    level: 'beginner',
                    lessons: 12,
                    duration: '8 часов',
                    difficulty: 'Начальный',
                    progress: 65,
                    category: ['beginner', 'technique']
                },
                {
                    id: 2,
                    title: 'Продвинутые техники',
                    description: 'Контрруление, трейлбрейкинг, прохождение поворотов',
                    icon: 'fas fa-tachometer-alt',
                    level: 'advanced',
                    lessons: 10,
                    duration: '6 часов',
                    difficulty: 'Продвинутый',
                    progress: 30,
                    category: ['advanced', 'technique']
                },
                {
                    id: 3,
                    title: 'Безопасность на дороге',
                    description: 'Как избегать аварийных ситуаций и быть заметным на дороге',
                    icon: 'fas fa-shield-alt',
                    level: 'beginner',
                    lessons: 8,
                    duration: '5 часов',
                    difficulty: 'Начальный',
                    progress: 0,
                    category: ['beginner', 'technique']
                },
                {
                    id: 4,
                    title: 'Техническое обслуживание',
                    description: 'Базовый ремонт, замена масла, проверка цепи и тормозов',
                    icon: 'fas fa-tools',
                    level: 'intermediate',
                    lessons: 14,
                    duration: '10 часов',
                    difficulty: 'Средний',
                    progress: 0,
                    category: ['maintenance']
                },
                {
                    id: 5,
                    title: 'Групповая езда',
                    description: 'Правила и безопасность при езде в группе, жесты и сигналы',
                    icon: 'fas fa-users',
                    level: 'intermediate',
                    lessons: 6,
                    duration: '4 часа',
                    difficulty: 'Средний',
                    progress: 0,
                    category: ['technique']
                },
                {
                    id: 6,
                    title: 'Экстремальное вождение',
                    description: 'Стрит-арт, вилли, стоппи и другие экстремальные элементы',
                    icon: 'fas fa-fire',
                    level: 'advanced',
                    lessons: 10,
                    duration: '7 часов',
                    difficulty: 'Эксперт',
                    progress: 0,
                    category: ['advanced']
                },
                {
                    id: 7,
                    title: 'Зимнее хранение',
                    description: 'Подготовка мотоцикла к зиме и правильное хранение',
                    icon: 'fas fa-snowflake',
                    level: 'beginner',
                    lessons: 5,
                    duration: '3 часа',
                    difficulty: 'Начальный',
                    progress: 0,
                    category: ['maintenance']
                },
                {
                    id: 8,
                    title: 'Электроника и тюнинг',
                    description: 'Установка дополнительного оборудования и чип-тюнинг',
                    icon: 'fas fa-bolt',
                    level: 'advanced',
                    lessons: 12,
                    duration: '9 часов',
                    difficulty: 'Продвинутый',
                    progress: 0,
                    category: ['advanced', 'maintenance']
                }
            ],
            activeCourses: [
                {
                    id: 1,
                    title: 'Базовое вождение',
                    progress: 65,
                    lastLesson: 'Урок 8: Торможение',
                    nextLesson: 'Урок 9: Контрруление'
                },
                {
                    id: 2,
                    title: 'Продвинутые техники',
                    progress: 30,
                    lastLesson: 'Урок 3: Трейлбрейкинг',
                    nextLesson: 'Урок 4: Контрсмещение'
                }
            ],
            recommendedCourses: [
                {
                    id: 3,
                    title: 'Безопасность на дороге',
                    description: 'Научитесь предвидеть опасности и избегать аварий',
                    rating: 4.8,
                    reviews: 124
                },
                {
                    id: 4,
                    title: 'Техническое обслуживание',
                    description: 'Экономьте на сервисе, обслуживая мотоцикл самостоятельно',
                    rating: 4.9,
                    reviews: 89
                },
                {
                    id: 5,
                    title: 'Групповая езда',
                    description: 'Безопасная и организованная езда в мотоколонне',
                    rating: 4.7,
                    reviews: 67
                }
            ]
        }
    },
    computed: {
        filteredCourses() {
            let filtered = this.courses
            
            // Фильтрация по выбранной категории
            if (this.currentFilter !== 'all') {
                filtered = filtered.filter(course => 
                    course.category.includes(this.currentFilter)
                )
            }
            
            // Фильтрация по поисковому запросу
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase()
                filtered = filtered.filter(course =>
                    course.title.toLowerCase().includes(query) ||
                    course.description.toLowerCase().includes(query)
                )
            }
            
            return filtered
        }
    },
    methods: {
        setFilter(filter) {
            this.currentFilter = filter
            
            // Обновляем активные кнопки фильтров
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active')
            })
            event.target.classList.add('active')
        },
        startCourse(courseId) {
            alert(`Начинаем курс ${courseId}!`)
            // Здесь будет логика начала курса
        },
        continueCourse(courseId) {
            alert(`Продолжаем курс ${courseId}!`)
            // Здесь будет логика продолжения курса
        },
        viewDetails(courseId) {
            alert(`Просмотр деталей курса ${courseId}`)
            // Здесь будет навигация к деталям курса
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