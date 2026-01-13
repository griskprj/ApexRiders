<script setup>
import MarkdownEditor from './MarkdownEditor.vue';
</script>
<template>
    <section class="post-view">
        <!-- Декоративные элементы -->
        <div class="decoration decoration-1"></div>
        <div class="decoration decoration-2"></div>
        
        <!-- Кнопка назад -->
        <button class="back-btn" @click="$router.go(-1)">
            <i class="fas fa-arrow-left"></i>
            Назад к ленте
        </button>
        
        <!-- Основной контент поста -->
        <div class="post-container">
            <!-- Заголовок и мета-информация -->
            <div class="post-header">
                <div class="post-category">
                    <i :class="post.categoryIcon"></i>
                    {{ post.category }}
                </div>
                
                <h1 class="post-title">{{ post.title }}</h1>
                
                <div class="post-meta">
                    <div class="post-author">
                        <div class="author-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="author-info">
                            <div class="author-name">{{ post.author.username }} <i v-if="post.author.isVerified" class="fas fa-check"></i></div>
                            <div class="post-date">{{ formatDate(post.createdAt) }}</div>
                        </div>
                    </div>
                    
                    <div class="post-stats">
                        <span class="post-stat">
                            <i class="fas fa-eye"></i>
                            {{ post.views }} просмотров
                        </span>
                        <span class="post-stat">
                            <i class="fas fa-clock"></i>
                            {{ formatReadTime(post.content) }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Действия для автора поста -->
            <div class="author-actions" v-if="post.author.isVerified === true">
                <button
                    class="btn btn-outline"
                    @click="deletePost(post)"
                >
                    <i class="fas fa-trash"></i> Удалить
                </button>
                <button
                    class="btn btn-outline"
                    @click="openEditModal"
                >
                    <i class="fas fa-edit"></i> Редактировать
                </button>
            </div>
            
            <!-- Изображение поста -->
            <div v-if="post.imageUrl" class="post-image-main">
                <img :src="post.imageUrl" :alt="post.title" />
            </div>
            
            <!-- Содержание поста -->
            <div class="post-content">
                <div class="post-body" v-html="post.htmlContent"></div>
                
                <!-- Теги -->
                <div v-if="post.tags && post.tags.length > 0" class="post-tags">
                    <span 
                        v-for="tag in post.tags" 
                        :key="tag"
                        class="post-tag"
                    >
                        #{{ tag }}
                    </span>
                </div>

                
                <!-- Действия с постом -->
                <div class="post-actions">
                    <button 
                        class="action-btn like-btn"
                        :class="{ 'liked': post.isLiked }"
                        @click="toggleLike"
                    >
                        <i class="fas fa-heart"></i>
                        <span>{{ post.likesCount }}</span>
                    </button>
                    
                    <button class="action-btn comment-btn" @click="scrollToComments">
                        <i class="fas fa-comment"></i>
                        <span>{{ post.commentsCount }}</span>
                    </button>
                    
                    <button class="action-btn share-btn">
                        <i class="fas fa-share-alt"></i>
                        <span>Поделиться</span>
                    </button>
                </div>
            </div>
            
            <!-- Разделитель -->
            <div class="section-divider">
                <i class="fas fa-comments"></i>
                <span>Комментарии</span>
            </div>
            
            <!-- Форма добавления комментария -->
            <div class="comment-form">
                <div class="comment-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="comment-input-container">
                    <textarea
                        v-model="newComment"
                        placeholder="Напишите комментарий..."
                        rows="3"
                        @keydown.enter.prevent="addComment"
                    ></textarea>
                    <button 
                        class="btn btn-primary comment-submit"
                        :disabled="!newComment.trim() || addingComment"
                        @click="addComment"
                    >
                        <span v-if="addingComment">Отправка...</span>
                        <span v-else>Отправить</span>
                    </button>
                </div>
            </div>
            
            <!-- Список комментариев -->
            <div class="comments-section">
                <div v-if="loadingComments" class="loading-comments">
                    <div class="loading-spinner"></div>
                    <p>Загрузка комментариев...</p>
                </div>
                
                <div v-else-if="comments.length === 0" class="no-comments">
                    <i class="fas fa-comment-slash"></i>
                    <h3>Комментариев пока нет</h3>
                    <p>Будьте первым, кто оставит комментарий!</p>
                </div>
                
                <div v-else class="comments-list">
                    <div 
                        v-for="comment in comments" 
                        :key="comment.id"
                        class="comment-item"
                    >
                        <div class="comment-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        
                        <div class="comment-content">
                            <div class="comment-header">
                                <div class="comment-author">{{ comment.author.username }} <i class="fas fa-check" v-if="comment.author.isVerified"></i></div>
                                <div class="comment-date">{{ formatDate(comment.createdAt) }}</div>
                            </div>
                            
                            <div class="comment-text">{{ comment.content }}</div>
                            
                            <div class="comment-actions">
                                <button class="comment-action">
                                    <i class="fas fa-heart"></i>
                                    <span>{{ comment.likeCount }}</span>
                                </button>
                                <button class="comment-action">
                                    <i class="fas fa-reply"></i>
                                    <span>Ответить</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Пагинация комментариев -->
                    <div v-if="commentsTotal > commentsPerPage" class="comments-pagination">
                        <button 
                            class="pagination-btn"
                            :disabled="commentsPage === 1"
                            @click="commentsPage--"
                        >
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        
                        <span class="pagination-info">
                            Страница {{ commentsPage }} из {{ Math.ceil(commentsTotal / commentsPerPage) }}
                        </span>
                        
                        <button 
                            class="pagination-btn"
                            :disabled="commentsPage * commentsPerPage >= commentsTotal"
                            @click="commentsPage++"
                        >
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Похожие посты -->
            <div class="related-posts">
                <h3 class="related-title">
                    <i class="fas fa-fire"></i>
                    Похожие посты
                </h3>
                
                <div v-if="loadingRelated" class="loading-related">
                    <div class="loading-spinner small"></div>
                </div>
                
                <div v-else-if="relatedPosts.length === 0" class="no-related">
                    <p>Нет похожих постов</p>
                </div>
                
                <div v-else class="related-grid">
                    <div 
                        v-for="relatedPost in relatedPosts" 
                        :key="relatedPost.id"
                        class="related-card"
                        @click="openRelatedPost(relatedPost.id)"
                    >
                        <h4 class="related-post-title">{{ relatedPost.title }}</h4>
                        <div class="related-post-meta">
                            <span class="related-post-author">{{ relatedPost.author.username }}</span>
                            <span class="related-post-date">{{ formatDateShort(relatedPost.createdAt) }}</span>
                        </div>
                        <div class="related-post-stats">
                            <span><i class="fas fa-heart"></i> {{ relatedPost.likesCount }}</span>
                            <span><i class="fas fa-comment"></i> {{ relatedPost.commentsCount }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Модальное окно редактирования поста -->
     <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Редактировать пост</h2>
                <button class="modal-close" @click="closeEditModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div class="modal-body">
                <form @submit.prevent="updatePost">
                    <div class="form-group">
                        <label for="editTitle">Заголовок</label>
                        <input
                            id="editTitle"
                            v-model="editData.title"
                            type="text"
                            placeholder="Заголовок поста"
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="editContent">Содержание (Markdown)</label>
                        <MarkdownEditor
                            ref="markdownEditorRef"
                            v-model="editData.content"
                            :rows="8"
                            placeholder="Содержание поста..."
                        />
                    </div>
                    
                    <div class="form-actions">
                        <button 
                            type="button" 
                            class="btn btn-outline"
                            @click="closeEditModal"
                        >
                            Отмена
                        </button>
                        <button 
                            type="submit" 
                            class="btn btn-primary"
                            :disabled="updatingPost"
                        >
                            <span v-if="updatingPost">Сохранение...</span>
                            <span v-else>Сохранить изменения</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    </template>
<script>
import { formatDistanceToNow } from 'date-fns'
import { da, ru, tr } from 'date-fns/locale'
export default {
    name: 'PostView',
    components: {
        MarkdownEditor
    },
    
    data() {
        return {
            post: {
                id: null,
                title: '',
                content: '',
                author: {
                    id: null,
                    username: '',
                    name: '',
                    isVerified: false,
                    isUser: false
                },
                createdAt: '',
                updatedAt: '',
                views: 0,
                likesCount: 0,
                commentsCount: 0,
                category: 'General',
                categoryIcon: 'fas fa-comment',
                imageUrl: null,
                tags: [],
                isLiked: false
            },
            comments: [],
            relatedPosts: [],
            newComment: '',
            loadingComments: true,
            loadingRelated: true,
            addingComment: false,
            commentsPage: 1,
            commentsPerPage: 20,
            commentsTotal: 0,

            showEditModal: false,
            updatingPost: false,
            editData: {
                title: '',
                content: ''
            }
        };
    },
    
    computed: {
        postId() {
            return this.$route.params.id;
        }
    },
    
    watch: {
        commentsPage() {
            this.fetchComments();
        },
        
        postId: {
            immediate: true,
            handler() {
                this.fetchPost()
            }
        }
    },
    
    async mounted() {
        if (this.postId) {
            await this.fetchPost();
        }
    },
    
    methods: {
        resetState() {
            this.comments = []
            this.relatedPosts = []
            this.commentsPage = 1
            this.commentsTotal = 0
            this.newComment = ''
            this.loadingComments = true
            this.loadingRelated = true
        },
        
        async fetchPost() {
            try {
                this.resetState()

                const token = localStorage.getItem('authToken');
                const response = await fetch(`/api/posts/${this.postId}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                this.post = {
                    ...data,
                    category: 'General',
                    categoryIcon: 'fas fa-comment',
                };

                await Promise.all([
                    this.fetchComments(),
                    this.fetchRelatedPosts()
                ])

                console.log(this.post.author.isVerified)
            } catch (error) {
                console.error('Ошибка при загрузке поста:', error);
                alert('Не удалось загрузить пост');
                this.$router.push('/community');
            }
        },
        
        async fetchComments() {
            try {
                this.loadingComments = true;
                const token = localStorage.getItem('authToken');
                const params = new URLSearchParams({
                    page: this.commentsPage,
                    per_page: this.commentsPerPage
                });

                const response = await fetch(`/api/posts/${this.postId}/comments?${params}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                this.comments = data.comment || [];
                this.commentsTotal = data.total || 0;
            } catch (error) {
                console.error('Ошибка при загрузке комментариев:', error);
            } finally {
                this.loadingComments = false;
            }
        },
        
        async fetchRelatedPosts() {
            try {
                this.loadingRelated = true;
                const token = localStorage.getItem('authToken');
                
                const response = await fetch(`/api/posts?page=1&per_page=3&filter=recent`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    this.relatedPosts = (data.posts || [])
                        .filter(p => p.id !== this.post.id)
                        .slice(0, 3);
                }
            } catch (error) {
                console.error('Ошибка при загрузке похожих постов:', error);
            } finally {
                this.loadingRelated = false;
            }
        },
        
        async addComment() {
            if (!this.newComment.trim()) return;
            
            this.addingComment = true;
            
            try {
                const token = localStorage.getItem('authToken');
                const response = await fetch(`/api/posts/${this.postId}/comments`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        content: this.newComment
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const newComment = await response.json();
                this.comments.unshift(newComment);
                this.post.commentsCount++;
                this.newComment = '';
                
                this.$nextTick(() => {
                    const firstComment = document.querySelector('.comment-item');
                    if (firstComment) {
                        firstComment.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                });
            } catch (error) {
                console.error('Ошибка при добавлении комментария:', error);
                alert('Не удалось добавить комментарий');
            } finally {
                this.addingComment = false;
            }
        },
        
        async toggleLike() {
            try {
                const token = localStorage.getItem('authToken');
                const response = await fetch(`/api/posts/${this.postId}/like`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                this.post.likesCount = data.likesCount;
                this.post.isLiked = data.liked;
            } catch (error) {
                console.error('Ошибка при лайке:', error);
            }
        },

        async deletePost() {
            try {
                if (!confirm('Вы действительно хотите удалить пост? Отменить это действие невозможно')) return

                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/posts/${this.postId}/delete`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                } else {
                    alert('Пост успешно удален!')
                    this.$router.push('/community')
                }
            } catch (error) {
                console.error('Ошибка при удалении: ', error)
            }
        },

        async updatePost() {
            if (!this.editData.title.trim() || !this.editData.content.trim()) {
                alert('Заголовок и содержание обязательны')
                return
            }

            this.updatingPost = true

            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/posts/${this.postId}`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        title: this.editData.title,
                        content: this.editData.content
                    })
                })

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}))
                    throw new Error(errorData.error || `HTTP error! status ${response.status}`)
                }

                const updatedPost = await response.json()

                this.post.title = updatedPost.title
                this.post.content = updatedPost.content
                this.post.htmlContent = updatedPost.htmlContent
                this.post.updatedAt = updatedPost.updatedAt

                if (updatedPost.htmlContent) {
                    this.post.htmlContent = updatedPost.htmlContent
                }

                this.closeEditModal()
                alert('Пост обновлен успешно')
            } catch (error) {
                console.error('Ошибка при обновлении поста: ', error)
                alert(`Не удалось обновить пост: ${error.message}`)
            } finally {
                this.updatingPost = false
            }
        },
        
        openEditModal() {
            console.log('Открываем модалку редактирования')
            
            this.editData = {
                title: this.post.title || '',
                content: this.post.content || ''
            }
            
            this.showEditModal = true
            
            // Ждем пока компонент отрендерится
            this.$nextTick(() => {
                // Принудительно устанавливаем значение в редактор
                if (this.$refs.markdownEditorRef) {
                    console.log('Устанавливаем значение в редактор:', this.editData.content)
                    // Очищаем внутреннее состояние редактора
                    this.$refs.markdownEditorRef.internalValue = ''
                    // Даем Vue обновить DOM
                    this.$nextTick(() => {
                        // Теперь устанавливаем нужное значение
                        this.$refs.markdownEditorRef.internalValue = this.editData.content
                    })
                }
            })
        },

        closeEditModal() {
            this.showEditModal = false
            this.editData = {
                title: '',
                content: ''
            }

            if (this.$refs.markdownEditor) {
                this.$refs.markdownEditor.internalValue = ''
            }
        },
        
        formatDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            const now = new Date();
            const diff = now - date;
            
            const minutes = Math.floor(diff / 60000);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);
            
            if (minutes < 60) return `${minutes} мин назад`;
            if (hours < 24) return `${hours} час назад`;
            if (days < 7) return `${days} дн назад`;
            return date.toLocaleDateString('ru-RU');
        },

        formatDateShort(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                day: 'numeric',
                month: 'short'
            });
        },
        
        formatContent(content) {
            return content.replace(/\n/g, '<br>');
        },
        
        formatReadTime(content) {
            const wordsPerMinute = 200;
            const words = content.split(/\s+/).length;
            const minutes = Math.ceil(words / wordsPerMinute);
            return `${minutes} мин. чтения`;
        },
        
        scrollToComments() {
            const commentsSection = document.querySelector('.comments-section');
            if (commentsSection) {
                commentsSection.scrollIntoView({ behavior: 'smooth' });
            }
        },
        
        openRelatedPost(postId) {
            this.$router.push(`/community/post/${postId}`);
        }
    }
};
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ ===== */
.post-view {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
    max-width: 1200px;
    margin: 0 auto;
}

.back-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    color: var(--text-secondary);
    padding: 10px 20px;
    margin-bottom: 30px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.back-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.post-container {
    background: var(--dark-light);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 40px;
    margin-bottom: 40px;
}

/* ===== ШАПКА ПОСТА ===== */
.post-header {
    margin-bottom: 30px;
}

.post-category {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--primary);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    margin-bottom: 20px;
}

.post-title {
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 20px;
    color: var(--text);
}

.post-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

.post-author {
    display: flex;
    align-items: center;
    gap: 15px;
}

.author-avatar {
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: var(--text-secondary);
}

.author-info {
    display: flex;
    flex-direction: column;
}

.author-name {
    font-weight: 600;
    font-size: 1.1rem;
}

.post-date {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.post-stats {
    display: flex;
    gap: 20px;
}

.post-stat {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.95rem;
    color: var(--text-secondary);
}

.post-stat i {
    color: var(--primary);
}

/* ===== ДЕЙСТВИЯ ДЛЯ АВТОРА ПОСТА */
.author-actions {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

/* ===== ИЗОБРАЖЕНИЕ ПОСТА ===== */
.post-image-main {
    margin: 30px 0;
    border-radius: 15px;
    overflow: hidden;
    max-height: 500px;
}

.post-image-main img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* ===== СОДЕРЖАНИЕ ПОСТА ===== */
.post-content {
    line-height: 1.8;
}

.post-body {
    font-size: 1.1rem;
    color: var(--text);
    margin-bottom: 30px;
}

.post-body :deep(br) {
    margin-bottom: 1em;
    display: block;
    content: "";
}

.post-tags {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.post-tag {
    font-size: 0.9rem;
    color: var(--accent);
    background: rgba(0, 191, 255, 0.1);
    padding: 5px 12px;
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.post-tag:hover {
    background: rgba(0, 191, 255, 0.2);
    transform: translateY(-2px);
}

/* ===== ДЕЙСТВИЯ С ПОСТОМ ===== */
.post-actions {
    display: flex;
    gap: 15px;
    margin-bottom: 40px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.3s ease;
}

.action-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.action-btn i {
    font-size: 1.1rem;
}

.action-btn span {
    font-weight: 500;
}

.like-btn.liked {
    background: rgba(255, 69, 0, 0.2);
    border-color: var(--primary);
    color: var(--primary);
}

.like-btn.liked i {
    color: var(--primary);
}

/* ===== РАЗДЕЛИТЕЛЬ ===== */
.section-divider {
    display: flex;
    align-items: center;
    gap: 15px;
    margin: 40px 0;
    padding: 20px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text);
    font-size: 1.2rem;
    font-weight: 600;
}

.section-divider i {
    color: var(--primary);
}

/* ===== ФОРМА КОММЕНТАРИЯ ===== */
.comment-form {
    display: flex;
    gap: 15px;
    margin-bottom: 40px;
}

.comment-avatar {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--text-secondary);
    flex-shrink: 0;
}

.comment-input-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.comment-input-container textarea {
    width: 100%;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: var(--text);
    font-size: 1rem;
    resize: vertical;
    min-height: 80px;
    transition: all 0.3s ease;
}

.comment-input-container textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

.comment-submit {
    align-self: flex-end;
    padding: 10px 30px;
}

/* ===== СЕКЦИЯ КОММЕНТАРИЕВ ===== */
.comments-section {
    margin-bottom: 50px;
}

.loading-comments,
.no-comments {
    text-align: center;
    padding: 40px 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.loading-comments .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

.no-comments i {
    font-size: 48px;
    color: var(--text-secondary);
    margin-bottom: 20px;
    opacity: 0.5;
}

.no-comments h3 {
    font-size: 1.3rem;
    margin-bottom: 10px;
}

.no-comments p {
    color: var(--text-secondary);
}

.comments-list {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.comment-item {
    display: flex;
    gap: 15px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.comment-content {
    flex: 1;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
}

.comment-author {
    font-weight: 600;
    font-size: 1rem;
}

.comment-date {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.comment-text {
    line-height: 1.6;
    margin-bottom: 15px;
    color: var(--text);
}

.comment-actions {
    display: flex;
    gap: 15px;
}

.comment-action {
    display: flex;
    align-items: center;
    gap: 5px;
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 0.9rem;
    cursor: pointer;
    transition: color 0.3s ease;
}

.comment-action:hover {
    color: var(--primary);
}

.comments-pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 30px;
    padding-top: 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 50%;
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

.pagination-info {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

/* ===== ПОХОЖИЕ ПОСТЫ ===== */
.related-posts {
    padding-top: 40px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.related-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.3rem;
    margin-bottom: 25px;
    color: var(--text);
}

.related-title i {
    color: var(--primary);
}

.loading-related {
    text-align: center;
    padding: 30px;
}

.loading-related .loading-spinner.small {
    width: 30px;
    height: 30px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-top: 2px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

.no-related {
    text-align: center;
    padding: 30px;
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.related-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.related-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--primary-dark);
    transform: translateY(-5px);
}

.related-post-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--text);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.related-post-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.related-post-stats {
    display: flex;
    gap: 15px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.related-post-stats i {
    color: var(--primary);
    margin-right: 5px;
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
    z-index: 2000;
    padding: 20px;
}

.modal-content {
    background: var(--dark-light);
    border-radius: 20px;
    width: 100%;
    max-width: 800px;
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

.form-group input {
    width: 100%;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
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

@media (max-width: 768px) {
    .modal-content {
        margin: 20px;
    }
    
    .modal-body {
        padding: 20px;
    }
    
    .form-actions {
        flex-direction: column;
    }
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

/* ===== MARKDOWN стили */
.post-body :deep(h1) {
    font-size: 2em;
    margin: 1.5em 0 0.5em;
    color: var(--text);
    font-weight: 700;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 0.3em;
}

.post-body :deep(h2) {
    font-size: 1.7em;
    margin: 1.3em 0 0.5em;
    color: var(--text);
    font-weight: 600;
}

.post-body :deep(h3) {
    font-size: 1.4em;
    margin: 1.2em 0 0.5em;
    color: var(--text);
    font-weight: 600;
}

.post-body :deep(h4) {
    font-size: 1.2em;
    margin: 1em 0 0.5em;
    color: var(--text);
    font-weight: 600;
}

.post-body :deep(p) {
    margin-bottom: 1em;
    line-height: 1.7;
}

.post-body :deep(strong), 
.post-body :deep(b) {
    font-weight: 700;
    color: var(--text);
}

.post-body :deep(em),
.post-body :deep(i) {
    font-style: italic;
}

.post-body :deep(ul),
.post-body :deep(ol) {
    margin: 1em 0;
    padding-left: 2em;
}

.post-body :deep(li) {
    margin-bottom: 0.5em;
}

.post-body :deep(blockquote) {
    border-left: 4px solid var(--primary);
    padding: 0.5em 1em;
    margin: 1.5em 0;
    background: rgba(255, 69, 0, 0.05);
    border-radius: 0 5px 5px 0;
    color: var(--text-secondary);
}

.post-body :deep(code) {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    color: var(--accent);
}

.post-body :deep(pre) {
    background: rgba(0, 0, 0, 0.3);
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1.5em 0;
}

.post-body :deep(pre code) {
    background: none;
    padding: 0;
    color: inherit;
    font-size: 0.9em;
}

.post-body :deep(a) {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: all 0.3s ease;
}

.post-body :deep(a:hover) {
    border-bottom-color: var(--accent);
}

.post-body :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin: 1.5em 0;
    display: block;
}

.post-body :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
}

.post-body :deep(th),
.post-body :deep(td) {
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.75em 1em;
    text-align: left;
}

.post-body :deep(th) {
    background: rgba(255, 255, 255, 0.05);
    font-weight: 600;
    color: var(--text);
}

.post-body :deep(hr) {
    border: none;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 2em 0;
}

/* ===== АНИМАЦИЯ ===== */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 768px) {
    .post-view {
        padding: 100px 5% 40px;
    }
    
    .post-container {
        padding: 25px;
    }
    
    .post-title {
        font-size: 1.8rem;
    }
    
    .post-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .post-actions {
        flex-wrap: wrap;
    }
    
    .action-btn {
        flex: 1;
        min-width: 120px;
        justify-content: center;
    }
    
    .comment-form {
        flex-direction: column;
    }
    
    .comment-avatar {
        align-self: flex-start;
    }
    
    .related-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .post-title {
        font-size: 1.5rem;
    }
    
    .post-container {
        padding: 20px;
    }
    
    .post-actions {
        flex-direction: column;
    }
    
    .action-btn {
        width: 100%;
    }
    
    .comment-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>