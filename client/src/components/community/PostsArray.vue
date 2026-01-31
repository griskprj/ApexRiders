<template>
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
            <div class="post-image">
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
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PostsArray',
    
    props: {
        filteredPosts: Array,
        formatDate: Function,
        showCreateModal: Function,
        openPost: Function
    }
}
</script>

<style scoped>
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
</style>