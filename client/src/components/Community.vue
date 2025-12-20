<template>
    <!-- Декоративные элементы -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    <!-- Сообщество -->
    <section class="community">
        <!-- Заголовок и фильтры -->
        <div class="community-header">
            <div class="header-main">
                <h1 class="community-title">
                    <i class="fas fa-users"></i>
                    <span>Сообщество мотоциклистов</span>
                </h1>
                <p class="community-subtitle">Общайтесь, делитесь опытом и находите единомышленников</p>
            </div>
            
            <div class="header-controls">
                <div class="filters">
                    <button 
                        v-for="filter in filters" 
                        :key="filter.id"
                        @click="activeFilter = filter.id"
                        :class="['filter-btn', { active: activeFilter === filter.id }]"
                    >
                        <i :class="filter.icon"></i>
                        {{ filter.label }}
                    </button>
                </div>
                
                <button class="btn btn-primary create-post-btn" @click="showCreateModal = true">
                    <i class="fas fa-plus"></i>
                    Создать пост
                </button>
            </div>
        </div>

        <!-- Основной контент -->
        <div class="community-content">
            <!-- Список постов -->
            <div class="posts-section">
                <div v-if="loading" class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Загрузка постов...</p>
                </div>
                
                <div v-else-if="filteredPosts.length === 0" class="no-posts">
                    <i class="fas fa-comments"></i>
                    <h3>Пока нет постов</h3>
                    <p>Будьте первым, кто поделится своим опытом!</p>
                    <button class="btn btn-primary" @click="showCreateModal = true">
                        Создать первый пост
                    </button>
                </div>
                
                <div v-else class="posts-grid">
                    <div 
                        v-for="post in filteredPosts" 
                        :key="post.id" 
                        class="post-card"
                        @click="openPost(post)"
                    >
                        <!-- Изображение поста -->
                        <div class="post-image" v-if="post.imageUrl">
                            <img :src="post.imageUrl" :alt="post.title">
                            <div class="post-category">
                                <i :class="post.categoryIcon"></i>
                                {{ post.category }}
                            </div>
                        </div>
                        
                        <div class="post-content" :class="{ 'no-image': !post.imageUrl }">
                            <!-- Заголовок и мета-информация -->
                            <div class="post-header">
                                <h3 class="post-title">{{ post.title }}</h3>
                                <div class="post-meta">
                                    <div class="post-author">
                                        <div class="author-avatar">
                                            <i class="fas fa-user"></i>
                                        </div>
                                        <div class="author-info">
                                            <div class="author-name">{{ post.author.name }}</div>
                                            <div class="post-date">{{ formatDate(post.createdAt) }}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Краткое содержание -->
                            <p class="post-excerpt">{{ post.excerpt }}</p>
                            
                            <!-- Статистика и действия -->
                            <div class="post-footer">
                                <div class="post-stats">
                                    <span class="post-stat">
                                        <i class="fas fa-comment"></i>
                                        {{ post.commentsCount }}
                                    </span>
                                    <span class="post-stat">
                                        <i class="fas fa-heart"></i>
                                        {{ post.likesCount }}
                                    </span>
                                    <span class="post-stat">
                                        <i class="fas fa-eye"></i>
                                        {{ post.views }}
                                    </span>
                                </div>
                                
                                <div class="post-tags">
                                    <span 
                                        v-for="tag in post.tags" 
                                        :key="tag"
                                        class="post-tag"
                                    >
                                        #{{ tag }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Пагинация -->
                <div v-if="filteredPosts.length > 0" class="pagination">
                    <button 
                        class="pagination-btn"
                        :disabled="currentPage === 1"
                        @click="currentPage--"
                    >
                        <i class="fas fa-chevron-left"></i>
                        Назад
                    </button>
                    
                    <div class="page-numbers">
                        <span 
                            v-for="page in totalPages" 
                            :key="page"
                            :class="['page-number', { active: currentPage === page }]"
                            @click="currentPage = page"
                        >
                            {{ page }}
                        </span>
                    </div>
                    
                    <button 
                        class="pagination-btn"
                        :disabled="currentPage === totalPages"
                        @click="currentPage++"
                    >
                        Вперед
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
            
            <!-- Боковая панель -->
            <div class="sidebar">
                <!-- Моя активность -->
                <div class="sidebar-card activity-card">
                    <h3 class="sidebar-title">
                        <i class="fas fa-chart-line"></i>
                        Моя активность
                    </h3>
                    <div class="activity-stats">
                        <div class="activity-stat">
                            <div class="stat-value">{{ userStats.posts }}</div>
                            <div class="stat-label">Постов</div>
                        </div>
                        <div class="activity-stat">
                            <div class="stat-value">{{ userStats.comments }}</div>
                            <div class="stat-label">Комментариев</div>
                        </div>
                        <div class="activity-stat">
                            <div class="stat-value">{{ userStats.likes }}</div>
                            <div class="stat-label">Лайков</div>
                        </div>
                    </div>
                </div>
                
                <!-- Популярные теги -->
                <div class="sidebar-card tags-card">
                    <h3 class="sidebar-title">
                        <i class="fas fa-tags"></i>
                        Популярные теги
                    </h3>
                    <div class="tags-list">
                        <span 
                            v-for="tag in popularTags" 
                            :key="tag.name"
                            class="tag"
                            :style="{ fontSize: 0.8 + (tag.count / 10) + 'rem' }"
                            @click="filterByTag(tag.name)"
                        >
                            #{{ tag.name }}
                            <span class="tag-count">{{ tag.count }}</span>
                        </span>
                    </div>
                </div>
                
                <!-- Активные пользователи -->
                <div class="sidebar-card users-card">
                    <h3 class="sidebar-title">
                        <i class="fas fa-trophy"></i>
                        Активные пользователи
                    </h3>
                    <div class="users-list">
                        <div 
                            v-for="user in activeUsers" 
                            :key="user.id"
                            class="user-item"
                        >
                            <div class="user-avatar">
                                <i class="fas fa-user"></i>
                            </div>
                            <div class="user-info">
                                <div class="user-name">{{ user.name }}</div>
                                <div class="user-posts">{{ user.posts }} постов</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Модальное окно создания поста -->
        <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Создать новый пост</h2>
                    <button class="modal-close" @click="showCreateModal = false">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <div class="modal-body">
                    <form @submit.prevent="createPost">
                        <div class="form-group">
                            <label for="postTitle">Заголовок</label>
                            <input
                                id="postTitle"
                                v-model="newPost.title"
                                type="text"
                                placeholder="О чём хотите рассказать?"
                                required
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="postContent">Содержание</label>
                            <textarea
                                id="postContent"
                                v-model="newPost.content"
                                rows="6"
                                placeholder="Поделитесь своим опытом, задайте вопрос или расскажите историю..."
                                required
                            ></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="postTags">Теги (через запятую)</label>
                            <input
                                id="postTags"
                                v-model="newPost.tags"
                                type="text"
                                placeholder="ремонт, байк, путешествие"
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="postImage">Изображение (URL)</label>
                            <input
                                id="postImage"
                                v-model="newPost.imageUrl"
                                type="text"
                                placeholder="https://example.com/photo.jpg"
                            />
                            <div v-if="newPost.imageUrl" class="image-preview">
                                <img :src="newPost.imageUrl" alt="Preview" />
                            </div>
                        </div>
                        
                        <div class="form-actions">
                            <button 
                                type="button" 
                                class="btn btn-outline"
                                @click="showCreateModal = false"
                            >
                                Отмена
                            </button>
                            <button 
                                type="submit" 
                                class="btn btn-primary"
                                :disabled="creatingPost"
                            >
                                <span v-if="creatingPost">Публикация...</span>
                                <span v-else>Опубликовать</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'Community',
    
    data() {
        return {
            // Фильтры
            filters: [
                { id: 'all', label: 'Все посты', icon: 'fas fa-globe' },
                { id: 'popular', label: 'Популярные', icon: 'fas fa-fire' },
                { id: 'recent', label: 'Новые', icon: 'fas fa-clock' },
                { id: 'my', label: 'Мои посты', icon: 'fas fa-user' }
            ],
            activeFilter: 'all',
            
            // Посты
            posts: [],
            loading: true,
            
            // Пагинация
            currentPage: 1,
            postsPerPage: 6,
            
            // Пользовательская статистика
            userStats: {
                posts: 5,
                comments: 23,
                likes: 45
            },
            
            // Популярные теги
            popularTags: [
                { name: 'ремонт', count: 42 },
                { name: 'путешествие', count: 38 },
                { name: 'советы', count: 31 },
                { name: 'байк', count: 29 },
                { name: 'мото', count: 27 },
                { name: 'обзор', count: 21 },
                { name: 'тюнинг', count: 18 },
                { name: 'безопасность', count: 15 }
            ],
            
            // Активные пользователи
            activeUsers: [
                { id: 1, name: 'Алексей В.', posts: 12 },
                { id: 2, name: 'Марина К.', posts: 9 },
                { id: 3, name: 'Дмитрий С.', posts: 8 },
                { id: 4, name: 'Иван М.', posts: 7 },
                { id: 5, name: 'Ольга П.', posts: 6 }
            ],
            
            // Модальное окно создания поста
            showCreateModal: false,
            creatingPost: false,
            newPost: {
                title: '',
                content: '',
                tags: '',
                imageUrl: ''
            }
        };
    },
    
    computed: {
        filteredPosts() {
            let filtered = [...this.posts];
            
            switch (this.activeFilter) {
                case 'popular':
                    return filtered.sort((a, b) => b.likesCount - a.likesCount);
                case 'recent':
                    return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
                case 'my':
                    // Здесь должна быть логика фильтрации постов текущего пользователя
                    return filtered.filter(post => post.author.id === 'current-user');
                default:
                    return filtered;
            }
        },
        
        totalPages() {
            return Math.ceil(this.filteredPosts.length / this.postsPerPage);
        },
        
        paginatedPosts() {
            const start = (this.currentPage - 1) * this.postsPerPage;
            const end = start + this.postsPerPage;
            return this.filteredPosts.slice(start, end);
        },
    },
    
    mounted() {
        this.fetchPosts();
    },
    
    methods: {
        async fetchPosts() {
            try {
                // Имитация загрузки данных с API
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Примерные данные (в реальном приложении здесь будет запрос к API)
                this.posts = [
                    {
                        id: 1,
                        title: 'Как я восстановил старый мотоцикл',
                        excerpt: 'История восстановления Honda CB400 1985 года из ржавого металлолома в блестящий аппарат...',
                        content: 'Полный текст поста...',
                        imageUrl: 'https://images.unsplash.com/photo-1558981285-6f0c94958bb6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                        category: 'Ремонт',
                        categoryIcon: 'fas fa-tools',
                        author: { id: 1, name: 'Алексей В.' },
                        createdAt: '2024-01-15T14:30:00',
                        commentsCount: 12,
                        likesCount: 45,
                        views: 234,
                        tags: ['ремонт', 'реставрация', 'байк']
                    },
                    {
                        id: 2,
                        title: 'Мототур по Кавказу: 3000 км впечатлений',
                        excerpt: 'Недельное путешествие по горным серпантинам, где каждый поворот открывает новую картину...',
                        imageUrl: 'https://images.unsplash.com/photo-1511994717241-8e4e484dfa8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                        category: 'Путешествия',
                        categoryIcon: 'fas fa-map-marked-alt',
                        author: { id: 2, name: 'Марина К.' },
                        createdAt: '2024-01-14T10:15:00',
                        commentsCount: 8,
                        likesCount: 32,
                        views: 187,
                        tags: ['путешествие', 'мототур', 'горы']
                    },
                    {
                        id: 3,
                        title: 'Советы по зимнему хранению мотоцикла',
                        excerpt: 'Правильная подготовка и хранение мотоцикла зимой - залог его долгой службы...',
                        imageUrl: null,
                        category: 'Советы',
                        categoryIcon: 'fas fa-lightbulb',
                        author: { id: 3, name: 'Дмитрий С.' },
                        createdAt: '2024-01-13T16:45:00',
                        commentsCount: 15,
                        likesCount: 28,
                        views: 156,
                        tags: ['зима', 'хранение', 'советы']
                    }
                ];
                
                this.loading = false;
            } catch (error) {
                console.error('Ошибка при загрузке постов:', error);
                this.loading = false;
            }
        },
        
        formatDate(dateString) {
            const date = new Date(dateString);
            const now = new Date();
            const diffMs = now - date;
            const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
            
            if (diffDays === 0) {
                return 'Сегодня';
            } else if (diffDays === 1) {
                return 'Вчера';
            } else if (diffDays < 7) {
                return `${diffDays} дня назад`;
            } else {
                return date.toLocaleDateString('ru-RU', {
                    day: 'numeric',
                    month: 'long'
                });
            }
        },
        
        filterByTag(tagName) {
            // Фильтрация по тегу
            console.log('Фильтр по тегу:', tagName);
        },
        
        openPost(post) {
            // Навигация к полному посту
            this.$router.push(`/community/post/${post.id}`);
        },
        
        async createPost() {
            if (!this.newPost.title || !this.newPost.content) return;
            
            this.creatingPost = true;
            
            try {
                // Имитация отправки на сервер
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                const newPost = {
                    id: Date.now(),
                    title: this.newPost.title,
                    excerpt: this.newPost.content.substring(0, 150) + '...',
                    content: this.newPost.content,
                    imageUrl: this.newPost.imageUrl || null,
                    category: 'Общее',
                    categoryIcon: 'fas fa-comment',
                    author: { id: 'current-user', name: 'Вы' },
                    createdAt: new Date().toISOString(),
                    commentsCount: 0,
                    likesCount: 0,
                    views: 0,
                    tags: this.newPost.tags ? this.newPost.tags.split(',').map(tag => tag.trim()) : []
                };
                
                this.posts.unshift(newPost);
                this.userStats.posts++;
                
                // Сброс формы
                this.newPost = {
                    title: '',
                    content: '',
                    tags: '',
                    imageUrl: ''
                };
                
                this.showCreateModal = false;
                
                // Уведомление об успехе
                console.log('Пост успешно создан!');
                
            } catch (error) {
                console.error('Ошибка при создании поста:', error);
            } finally {
                this.creatingPost = false;
            }
        }
    }
};
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ СООБЩЕСТВА ===== */
.community {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

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

/* ===== КОНТЕНТ СООБЩЕСТВА ===== */
.community-content {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 30px;
}

/* ===== СЕКЦИЯ ПОСТОВ ===== */
.posts-section {
    flex: 1;
}

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

.no-posts {
    text-align: center;
    padding: 60px 20px;
    background: var(--dark-light);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.no-posts i {
    font-size: 64px;
    color: var(--text-secondary);
    margin-bottom: 20px;
    opacity: 0.5;
}

.no-posts h3 {
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.no-posts p {
    color: var(--text-secondary);
    margin-bottom: 25px;
}

.posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 30px;
}

.post-card {
    background: var(--dark-light);
    border-radius: 15px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
}

.post-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary-dark);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
}

.post-image {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.post-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.post-card:hover .post-image img {
    transform: scale(1.05);
}

.post-category {
    position: absolute;
    top: 15px;
    left: 15px;
    background: var(--primary);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

.post-content {
    padding: 20px;
}

.post-content.no-image {
    padding-top: 25px;
}

.post-header {
    margin-bottom: 15px;
}

.post-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 10px;
    line-height: 1.4;
}

.post-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.post-author {
    display: flex;
    align-items: center;
    gap: 10px;
}

.author-avatar {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--text-secondary);
}

.author-info {
    display: flex;
    flex-direction: column;
}

.author-name {
    font-weight: 500;
    font-size: 0.95rem;
}

.post-date {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.post-excerpt {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 20px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.post-stats {
    display: flex;
    gap: 15px;
}

.post-stat {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.post-stat i {
    color: var(--primary);
}

.post-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.post-tag {
    font-size: 0.8rem;
    color: var(--accent);
    background: rgba(0, 191, 255, 0.1);
    padding: 3px 10px;
    border-radius: 15px;
}

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

/* ===== БОКОВАЯ ПАНЕЛЬ ===== */
.sidebar {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.sidebar-card {
    background: var(--dark-light);
    border-radius: 15px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.2rem;
    margin-bottom: 20px;
    color: var(--text);
}

.sidebar-title i {
    color: var(--primary);
}

/* Активность */
.activity-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.activity-stat {
    text-align: center;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
}

.activity-stat .stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 5px;
}

.activity-stat .stat-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* Теги */
.tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 12px;
    background: rgba(0, 191, 255, 0.1);
    color: var(--accent);
    border-radius: 20px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tag:hover {
    background: rgba(0, 191, 255, 0.2);
    transform: translateY(-2px);
}

.tag-count {
    font-size: 0.8rem;
    opacity: 0.7;
}

/* Пользователи */
.users-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.user-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

.user-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--text-secondary);
}

.user-info {
    flex: 1;
}

.user-name {
    font-weight: 500;
    font-size: 0.95rem;
}

.user-posts {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ===== МОДАЛЬНОЕ ОКНО ===== */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content {
    background: var(--dark-light);
    border-radius: 20px;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
    font-size: 1.5rem;
    font-weight: 600;
}

.modal-close {
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.2rem;
    cursor: pointer;
    transition: color 0.3s ease;
}

.modal-close:hover {
    color: var(--text);
}

.modal-body {
    padding: 30px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--text);
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.image-preview {
    margin-top: 15px;
}

.image-preview img {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.form-actions {
    display: flex;
    gap: 15px;
    margin-top: 30px;
}

.form-actions .btn {
    flex: 1;
    justify-content: center;
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
@media (max-width: 1200px) {
    .community-content {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 992px) {
    .sidebar {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .community {
        padding: 100px 5% 40px;
    }
    
    .community-title {
        font-size: 2rem;
    }
    
    .header-controls {
        flex-direction: column;
        align-items: stretch;
    }
    
    .filters {
        justify-content: center;
    }
    
    .posts-grid {
        grid-template-columns: 1fr;
    }
    
    .post-footer {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .post-stats {
        width: 100%;
        justify-content: space-between;
    }
    
    .sidebar {
        grid-template-columns: 1fr;
    }
    
    .modal-content {
        margin: 20px;
    }
}

@media (max-width: 480px) {
    .filter-btn {
        flex: 1;
        justify-content: center;
    }
    
    .post-content {
        padding: 15px;
    }
    
    .modal-body {
        padding: 20px;
    }
    
    .form-actions {
        flex-direction: column;
    }
}
</style>