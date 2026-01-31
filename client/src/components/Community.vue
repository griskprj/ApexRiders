<script setup>
import CreatePostModal from './community/CreatePostModal.vue';
import HeaderFilter from './community/HeaderFilter.vue';
import Paginatie from './community/Paginatie.vue';
import PostsArray from './community/PostsArray.vue';
import Sidebar from './community/Sidebar.vue';
</script>
<template>

    <!-- Сообщество -->
    <section class="community">
        <HeaderFilter 
            :active-filter="activeFilter"
            @filter-change="handleFilterChange"
            @create-post="openCreateModal"
        />

        <!-- Основной контент -->
        <div class="community-content">
            <!-- Список постов -->
            <div class="posts-section">
                <PostsArray
                    :filtered-posts="filteredPosts"
                    :format-date="formatDate"
                    :open-post="openPost"
                    :show-create-modal="showCreateModal"
                />
                
                <!-- Пагинация -->
                <Paginatie
                    :filtered-posts="filteredPosts"
                    :current-page="currentPage"
                    :total-pages="totalPages"
                    @page-change="handlePageChange"
                />
            </div>
            
            <Sidebar
                :active-users="activeUsers"
            />
        </div>

        <!-- Модальное окно создания/редактирования поста -->
        <CreatePostModal
            :show="showCreateModal"
            :form-data="newPost"
            :image-preview="imagePreview"
            :has-unsaved-draft="hasUnsavedDraft"
            :creating-post="creatingPost"
            :markdown-editor-key="markdownEditorKey"
            @close="closeCreateModal"
            @submit="createPost"
            @clear-draft="clearDraftAndForm"
            @remove-image="removeImage"
            @file-upload="handleFileUpload"
            @update-image-preview="updateImagePreview"
            @update:title="value => newPost.title = value"
            @update:content="value => newPost.content = value"
            @update:tags="value => newPost.tags = value"
            @update:imageUrl="value => newPost.imageUrl = value"
        />
    </section>
</template>

<script>
export default {
    name: 'Community',
    
    data() {
        return {
            activeFilter: 'all',
            posts: [],
            loading: true,
            currentPage: 1,
            postsPerPage: 6,
            totalPosts: 0,
            userStats: {
                posts: 0,
                comments: 0
            },
            activeUsers: [],
            showCreateModal: false,
            creatingPost: false,
            newPost: {
                title: '',
                content: '',
                tags: '',
                imageUrl: ''
            },

            draftKey: 'post_draft',
            currentUserId: null,
            autoSaveTimer: null,
            hasUnsavedDraft: false,

            imagePreview: null,
            uploadingImage: false,
            uploadProgress: 0,

            oldImageToDelete: null,

            markdownEditorKey: 0
        };
    },
    
    computed: {
        filteredPosts() {
            return this.posts;
        },
        
        totalPages() {
            return Math.ceil(this.totalPosts / this.postsPerPage);
        },

        hasImage() {
            return !!this.imagePreview || !!this.newPost.imageUrl;
        }
    },

    watch: {
        activeFilter() {
            this.currentPage = 1;
            this.fetchPosts();
        },
        
        'newPost.title'(newTitle) {
            if (newTitle || this.newPost.content || this.newPost.imageUrl) {
                this.saveDraft();
            } else if (!newTitle && !this.newPost.content && !this.newPost.imageUrl) {
                this.hasUnsavedDraft = false;
            }
        },
        'newPost.content'(newContent) {
            if (this.newPost.title || newContent || this.newPost.imageUrl) {
                this.saveDraft();
            } else if (!this.newPost.title && !newContent && !this.newPost.imageUrl) {
                this.hasUnsavedDraft = false;
            }
        },
        'newPost.tags'(newTags) {
            if (this.newPost.title || this.newPost.content || this.newPost.imageUrl) {
                this.saveDraft();
            }
        },
        'newPost.imageUrl'(newUrl) {
            if (this.newPost.title || this.newPost.content || newUrl) {
                this.saveDraft();
            } else if (!this.newPost.title && !this.newPost.content && !newUrl) {
                this.hasUnsavedDraft = false;
            }
        }
    },
    
    async mounted() {
        this.getCurrentUserId();

        window.addEventListener('beforeunload', this.handleBeforeUnload);

        await Promise.all([
            this.fetchPosts(),
            this.fetchCommunityStats()
        ]);
    },

    beforeUnmount() {
        window.removeEventListener('beforeunload', this.handleBeforeUnload);

        if (this.autoSaveTimer) {
            clearTimeout(this.autoSaveTimer);
        }
    },
    
    methods: {
        async fetchPosts() {
            try {
                this.loading = true;

                const token = localStorage.getItem('authToken');
                const params = new URLSearchParams({
                    page: this.currentPage,
                    per_page: this.postsPerPage,
                    filter: this.activeFilter
                });

                const response = await fetch(`/api/posts?${params}`, {
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
                this.posts = data.posts || [];
                this.totalPosts = data.total || 0;
                
                console.log(`Загружено ${this.posts.length} постов, страница ${this.currentPage}, всего: ${this.totalPosts}`);
            } catch (error) {
                console.error('Ошибка при загрузке постов:', error);
            } finally {
                this.loading = false;
            }
        },

        async fetchCommunityStats() {
            try {
                const token = localStorage.getItem('authToken');
                const response = await fetch('/api/community/stats', {
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
                this.userStats = data.userStats || { posts: 0, comments: 0 };
                this.activeUsers = data.activeUsers || [];
            } catch (error) {
                console.error('Ошибка при загрузке статистики:', error);
            }
        },
        
        formatDate(dateString) {
            const date = new Date(dateString);
            const now = new Date();
            const diffMs = now - date;
            const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
            
            if (diffDays === 0) {
                const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
                if (diffHours === 0) {
                    const diffMinutes = Math.floor(diffMs / (1000 * 60));
                    return `${diffMinutes} минут назад`;
                }
                return `${diffHours} часов назад`;
            } else if (diffDays === 1) {
                return 'Вчера';
            } else if (diffDays < 7) {
                return `${diffDays} дней назад`;
            } else {
                return date.toLocaleDateString('ru-RU', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                });
            }
        },

        handlePageChange(newPage) {
            if (newPage >= 1 && newPage <= this.totalPages && newPage !== this.currentPage) {
                this.currentPage = newPage;
                this.fetchPosts();
                
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        },

        async createPost() {
            const title = String(this.newPost.title || '').trim();
            const content = String(this.newPost.content || '');
            
            if (!title) {
                alert('Заголовок обязателен');
                return;
            }
            
            if (!content) {
                alert('Содержание поста обязательно');
                return;
            }
            
            this.creatingPost = true;
            
            try {
                const token = localStorage.getItem('authToken');
 
                const formData = new FormData();
                formData.append('title', title);
                formData.append('content', content);
                
                if (this.newPost.tags && this.newPost.tags.trim()) {
                    formData.append('tags', this.newPost.tags.trim());
                }
                
                const fileInput = this.$refs.fileInput;
                
                if (fileInput && fileInput.files && fileInput.files[0]) {
                    formData.append('image', fileInput.files[0]);
                } 
                else if (this.newPost.imageUrl && this.newPost.imageUrl.trim()) {
                    formData.append('imageUrl', this.newPost.imageUrl.trim());
                }
                else if (this.imagePreview && this.imagePreview.startsWith('data:')) {
                    alert('Пожалуйста, загрузите изображение заново или введите URL');
                    this.creatingPost = false;
                    return;
                }
                
                const response = await fetch('/api/posts', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: formData
                })

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Ошибка сервера:', errorText);
                    try {
                        const errorData = JSON.parse(errorText);
                        throw new Error(errorData.error || `Ошибка ${response.status}`);
                    } catch {
                        throw new Error(`Ошибка ${response.status}: ${errorText}`);
                    }
                }

                const newPostData = await response.json();
                this.clearDraft();
                this.clearForm();

                this.currentPage = 1;
                await this.fetchPosts();
                await this.fetchCommunityStats();
                
                this.showCreateModal = false;
                
                alert('Пост успешно создан!')
            } catch (error) {
                console.error('Ошибка при создании поста:', error);
                alert(`Не удалось создать пост: ${error.message}`);
            } finally {
                this.creatingPost = false;
            }
        },

        async handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) {
                return;
            }
            
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'];
            const fileExt = file.name.split('.').pop().toLowerCase();
            const validExts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'];
            
            if (!validTypes.includes(file.type) && !validExts.includes(fileExt)) {
                alert('Пожалуйста, выберите файл изображения (JPG, PNG, GIF, WebP, BMP)');
                this.resetFileInput();
                return;
            }
            
            if (file.size > 5 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер: 5MB');
                this.resetFileInput();
                return;
            }
            
            const reader = new FileReader();
            reader.onload = (e) => {
                this.imagePreview = e.target.result;
            };
            reader.readAsDataURL(file);
            
            this.uploadingImage = true;
            try {
                const formData = new FormData();
                formData.append('image', file);
                
                const token = localStorage.getItem('authToken');
                const response = await fetch('/api/posts/upload-image', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    this.newPost.imageUrl = data.image_url || data.imageUrl || '';
                } else {
                    alert(data.error || 'Ошибка загрузки изображения');
                    this.resetFileInput();
                    this.imagePreview = null;
                }
            } catch (error) {
                console.error('Ошибка загрузки:', error);
                alert('Не удалось загрузить изображение');
                this.resetFileInput();
                this.imagePreview = null;
            } finally {
                this.uploadingImage = false;
            }
        },

        getCurrentUserId() {
            try {
                const token = localStorage.getItem('authToken')
                if (token) {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                    this.currentUserId = payload.sub || payload.identity;
                    this.draftKey = `post_draft_${this.currentUserId}`;
                }
            } catch (error) {
                console.error('Ошибка при получении ID пользователя: ', error);
                this.currentUserId = null;
            }
        },

        updateImagePreview() {
            if (this.newPost.imageUrl && this.newPost.imageUrl.trim()) {
                const url = this.newPost.imageUrl.trim();
                
                const urlPattern = /^(https?:\/\/.*\.(?:png|jpg|jpeg|gif|webp|bmp)(\?.*)?)$/i;
                
                if (urlPattern.test(url)) {
                    this.imagePreview = url;

                    if (this.$refs.fileInput) {
                        this.$refs.fileInput.value = '';
                    }
                } else {
                    this.imagePreview = null;
                    
                    if (url.startsWith('data:')) {
                        this.imagePreview = url;
                    }
                }
            } else {
                this.imagePreview = null;
            }
        },

        removeImage() {
            this.imagePreview = null;
            this.newPost.imageUrl = '';
            
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = '';
            }
        },
            
        resetForm() {
            this.newPost = {
                title: '',
                content: '',
                tags: '',
                imageUrl: ''
            }
            
            if (this.$refs.markdownEditor) {
                this.$refs.markdownEditor.internalValue = '';
            }
        },

        async toggleLike(post) {
            try {
                const token = localStorage.getItem('authToken');
                const response = await fetch(`/api/posts/${post.id}/like`, {
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
                post.likesCount = data.likesCount;
                
            } catch (error) {
                console.error('Ошибка при лайке:', error);
            }
        },

        openCreateModal() {
            this.getCurrentUserId();
    
            const hasDraft = this.loadDraft();
            this.showCreateModal = true;
            
            if (hasDraft) {
                setTimeout(() => {
                    this.$nextTick(() => {
                        const titleInput = document.getElementById('postTitle');
                        if (titleInput) {
                            titleInput.focus();
                        }
                        
                        if (confirm('У вас есть сохраненный черновик. Загрузить его?')) {
                            console.log('Черновик загружен');
                        } else {
                            this.clearForm();
                        }
                    });
                }, 100);
            } else {
                this.clearForm();
            }
            
            
            this.$nextTick(() => {
                const titleInput = document.getElementById('postTitle');
                if (titleInput) {
                    titleInput.focus();
                }
            });
        },

        closeCreateModal() {
            if (this.hasUnsavedDraft && (this.newPost.title || this.newPost.content || this.newPost.imageUrl)) {
                const shouldSave = confirm('Сохранить черновик?');
                
                if (shouldSave) {
                    this.saveDraft();
                } else {
                    this.clearDraft();
                    this.clearForm();
                }
            }
            
            this.showCreateModal = false;
        },

        clearForm() {
            this.newPost = {
                title: '',
                content: '',
                tags: '',
                imageUrl: ''
            }
            this.imagePreview = null;
            this.uploadingImage = false;
            this.hasUnsavedDraft = false;
            
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = '';
            }

            this.clearDraft()
        },

        clearDraftAndForm() {
            if (confirm('Удалить черновик и очистить форму?')) {
                this.clearDraft();
                this.clearForm();
                this.showCreateModal = false;
            }
        },

        openPost(post) {
            this.$router.push(`/community/post/${post.id}`);
        },

        saveDraft() {
            if (!this.currentUserId) {
                console.warn('ID пользователя не определен, черновик не сохранен');
                return;
            }

            if (this.autoSaveTimer) {
                clearTimeout(this.autoSaveTimer);
            }
            
            this.autoSaveTimer = setTimeout(() => {
                if (this.newPost.title || this.newPost.content || this.newPost.imageUrl) {
                    const draftData = {
                        title: this.newPost.title,
                        content: this.newPost.content,
                        tags: this.newPost.tags,
                        imageUrl: this.newPost.imageUrl,
                        imagePreview: this.imagePreview,
                        timestamp: new Date().toISOString()
                    }

                    try {
                        localStorage.setItem(this.draftKey, JSON.stringify(draftData));
                        this.hasUnsavedDraft = true;
                        console.log('Черновик сохранен: ', draftData);
                    } catch (e) {
                        console.error('Ошибка сохранения черновика: ', e);
                    }
                }
            }, 1500)
        },

        loadDraft() {
            if (!this.currentUserId) {
                this.getCurrentUserId();
            }
            
            try {
                const draft = localStorage.getItem(this.draftKey);
                if (draft) {
                    const parsed = JSON.parse(draft);
                    
                    const draftTime = new Date(parsed.timestamp);
                    const now = new Date();
                    const hoursDiff = (now - draftTime) / (1000 * 60 * 60);
                    
                    if (hoursDiff > 24) {
                        console.log('Черновик устарел (>24 часов), удаляем');
                        this.clearDraft();
                        return false;
                    }
                    
                    this.newPost = {
                        title: parsed.title || '',
                        content: parsed.content || '',
                        tags: parsed.tags || '',
                        imageUrl: parsed.imageUrl || ''
                    };
                    
                    if (parsed.imagePreview) {
                        this.imagePreview = parsed.imagePreview;
                    }
                    
                    this.hasUnsavedDraft = true;

                    this.markdownEditorKey += 1;

                    this.$nextTick(() => {
                        console.log('Черновик полностью загружен и отображен');
                    });
                    
                    console.log('Черновик загружен:', parsed);
                    return true;
                }
            } catch (e) {
                console.error('Ошибка загрузки черновика:', e);
                this.clearDraft();
            }
            return false;
        },

        clearDraft() {
            localStorage.removeItem(this.draftKey)
            this.hasUnsavedDraft = false;
        },

        confirmLoadDraft() {
            if (this.hasUnsavedDraft) {
                return confirm('У вас есть сохраненный черновик. Загрузить его?');
            }
            return false;
        },

        handleBeforeUnload(e) {
            if (this.hasUnsavedDraft && (this.newPost.title || this.newPost.content)) {
                e.preventDefault();
                e.returnValue = 'У вас есть несохраненный черновик. Вы уверены, что хотите уйти?';
                return e.returnValue;
            }
        },

        handleFilterChange(filterId) {
            this.activeFilter = filterId;
            this.currentPage = 1;
            this.fetchPosts();
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



/* ===== КОНТЕНТ СООБЩЕСТВА ===== */
.community-content {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 30px;
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





/* ===== ДЕКОРАТИВНЫЕ ЭЛЕМЕНТЫ ===== */


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

    .modal-header {
        flex-direction: column;
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