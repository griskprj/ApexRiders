<script setup>
import MarkdownEditor from '../MarkdownEditor.vue';
</script>

<template>
    <!-- Модальное окно создания поста -->
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <div class="modal-header">
                <div>
                    <h2>Создать новый пост</h2>
                    <button class="modal-close" @click="$emit('close')">
                        <i class="fas fa-times"></i>
                    </button>
                    <button 
                        type="button" 
                        class="btn btn-outline"
                        @click="$emit('clear-draft')"
                        v-if="hasUnsavedDraft"
                    >
                        <i class="fas fa-trash"></i>
                        Удалить черновик
                    </button>
                </div>
                <div v-if="hasUnsavedDraft" class="draft-info">
                    <i class="fas fa-save"></i>
                    <span>Черновик сохранен</span>
                    <small>Автоматически сохраняется при изменении</small>
                </div>
            </div>
            
            <div class="modal-body">
                <form @submit.prevent="$emit('submit', formData)">
                    <div class="form-group">
                        <label for="postTitle">Заголовок</label>
                        <input
                            id="postTitle"
                            v-model="formData.title"
                            type="text"
                            placeholder="О чём хотите рассказать?"
                            required
                            @input="$emit('update:title', $event.target.value)"
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="postContent">Содержание (Markdown)</label>
                        <MarkdownEditor
                            v-if="show"
                            :key="markdownEditorKey"
                            v-model="formData.content"
                            :rows="8"
                            placeholder="Напишите ваш пост используя Markdown..."
                            @update:modelValue="$emit('update:content', $event)"
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="postTags">Теги (через запятую)</label>
                        <input
                            id="postTags"
                            v-model="formData.tags"
                            type="text"
                            placeholder="ремонт, байк, путешествие"
                            @input="$emit('update:tags', $event.target.value)"
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="postImage">Изображение</label>
                        
                        <div class="image-upload-container">
                            <!-- Превью изображения -->
                            <div v-if="imagePreview" class="image-preview">
                                <img :src="imagePreview" alt="Preview" />
                                <button type="button" class="remove-image" @click="$emit('remove-image')">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                            
                            <!-- Кнопки загрузки -->
                            <div class="upload-options" v-if="!imagePreview">
                                <input
                                    type="file"
                                    id="fileInput"
                                    ref="fileInput"
                                    @change="$emit('file-upload', $event)"
                                    accept="image/*"
                                    style="display: none"
                                />
                                
                                <div class="upload-buttons">
                                    <button 
                                        type="button" 
                                        class="btn btn-outline upload-btn"
                                        @click="$refs.fileInput.click()"
                                    >
                                        <i class="fas fa-upload"></i>
                                        Загрузить с устройства
                                    </button>
                                    
                                    <div class="upload-or">
                                        <span>или</span>
                                    </div>
                                    
                                    <div class="url-upload">
                                        <input
                                            type="text"
                                            v-model="formData.imageUrl"
                                            placeholder="Вставьте URL изображения"
                                            @blur="$emit('update-image-preview')"
                                            @keyup.enter="$emit('update-image-preview')"
                                            @input="$emit('update:imageUrl', $event.target.value)"
                                        />
                                    </div>
                                </div>
                                
                                <div class="upload-hints">
                                    <small>Поддерживаемые форматы: JPG, PNG, GIF, WebP</small>
                                    <small>Максимальный размер: 5MB</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button 
                            type="button" 
                            class="btn btn-outline"
                            @click="$emit('close')"
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
</template>

<script>

export default {
    name: 'CreatePostModal',
    components: {
        MarkdownEditor
    },
    props: {
        show: {
            type: Boolean,
            required: true
        },
        formData: {
            type: Object,
            required: true,
            default: () => ({
                title: '',
                content: '',
                tags: '',
                imageUrl: ''
            })
        },
        imagePreview: {
            type: String,
            default: null
        },
        hasUnsavedDraft: {
            type: Boolean,
            default: false
        },
        creatingPost: {
            type: Boolean,
            default: false
        },
        markdownEditorKey: {
            type: Number,
            default: 0
        }
    },
    emits: [
        'close',
        'submit',
        'clear-draft',
        'remove-image',
        'file-upload',
        'update-image-preview',
        'update:title',
        'update:content',
        'update:tags',
        'update:imageUrl'
    ],
    
    // Если нужны refs в шаблоне
    computed: {
        fileInput() {
            return this.$refs.fileInput;
        }
    }
}
</script>

<style scoped>
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
    overflow-x: hidden;
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

.draft-info {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(0, 191, 255, 0.1);
    border: 1px solid rgba(0, 191, 255, 0.2);
    border-radius: 8px;
    color: var(--accent);
    font-size: 0.9rem;
    margin-bottom: 15px;
}

.draft-info i {
    color: var(--accent);
}

.draft-info small {
    margin-left: auto;
    opacity: 0.7;
    font-size: 0.8rem;
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

.image-upload-container {
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.02);
}

.image-preview {
    position: relative;
    margin-bottom: 20px;
}

.image-preview img {
    width: 100%;
    max-height: 300px;
    object-fit: contain;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.remove-image {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.remove-image:hover {
    background: var(--primary);
    transform: scale(1.1);
}

.upload-buttons {
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: center;
}

.upload-btn {
    padding: 12px 25px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.95rem;
}

.upload-or {
    display: flex;
    align-items: center;
    width: 100%;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.upload-or::before,
.upload-or::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
}

.upload-or span {
    padding: 0 15px;
}

.url-upload {
    width: 100%;
}

.url-upload input {
    width: 100%;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text);
    font-size: 0.95rem;
}

.upload-hints {
    margin-top: 15px;
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.8rem;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.uploading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    z-index: 10;
}

.uploading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Адаптивность */
@media (max-width: 768px) {
    .upload-buttons {
        gap: 10px;
    }
    
    .upload-btn {
        width: 100%;
        justify-content: center;
        padding: 10px 15px;
    }
    
    .upload-or span {
        padding: 0 10px;
        font-size: 0.8rem;
    }
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
</style>