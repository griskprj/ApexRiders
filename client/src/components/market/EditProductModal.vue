<template>
    <div class="modal" :class="{ active: showModal }">
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-edit"></i> Редактировать объявление</h3>
                <button class="modal-close" @click="closeModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="handleSubmit" id="editForm">
                    <div class="form-group">
                        <label>Заголовок объявления *</label>
                        <input type="text" v-model="formData.title" placeholder="Например: Шлем AGV K6, размер L" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Категория *</label>
                            <select v-model="formData.category" required>
                                <option value="">Выберите категорию</option>
                                <option value="motorcycles">Мотоциклы</option>
                                <option value="engines">Двигатели</option>
                                <option value="frames">Рамы и подвеска</option>
                                <option value="electronics">Электроника</option>
                                <option value="helmets">Шлемы</option>
                                <option value="clothing">Одежда</option>
                                <option value="accessories">Аксессуары</option>
                                <option value="parts">Запчасти</option>
                                <option value="gear">Экипировка</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Цена (₽) *</label>
                            <input type="number" v-model="formData.price" placeholder="25000" required min="0">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Описание *</label>
                        <textarea v-model="formData.description" placeholder="Подробное описание товара..." rows="4" required></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Город *</label>
                            <input type="text" v-model="formData.city" placeholder="Москва" required>
                        </div>
                        <div class="form-group">
                            <label>Телефон для связи *</label>
                            <input type="tel" v-model="formData.phone" placeholder="+7 (XXX) XXX-XX-XX" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Статус объявления</label>
                        <div class="status-options">
                            <label class="status-option">
                                <input type="checkbox" v-model="formData.is_active">
                                <span class="status-label">
                                    <i class="fas fa-check-circle"></i> Активно
                                </span>
                            </label>
                            <label class="status-option">
                                <input type="checkbox" v-model="formData.is_bargain">
                                <span class="status-label">
                                    <i class="fas fa-handshake"></i> Торг уместен
                                </span>
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Изображения (до 5 шт.)</label>
                        <div class="image-upload">
                            <!-- Существующие изображения -->
                            <div class="existing-images" v-if="existingImages.length > 0">
                                <h4>Текущие изображения:</h4>
                                <div class="existing-images-grid">
                                    <div class="existing-image-item" v-for="(img, index) in existingImages" :key="'existing-' + index">
                                        <img :src="getImageUrl(img)" :alt="`Изображение ${index + 1}`">
                                        <div class="existing-image-actions">
                                            <button type="button" class="btn-small btn-danger" @click="removeExistingImage(index)">
                                                <i class="fas fa-trash"></i> Удалить
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Загрузка новых изображений -->
                            <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>Добавить новые изображения</p>
                                <p class="upload-hint">Поддерживаются: JPG, PNG, GIF, WebP</p>
                            </div>
                            <input 
                                type="file" 
                                ref="fileInput" 
                                @change="handleImageUpload" 
                                multiple 
                                accept="image/*" 
                                style="display: none;"
                            >
                            
                            <!-- Preview новых файлов -->
                            <div class="image-preview" v-if="newFiles.length > 0">
                                <div class="preview-item" v-for="(file, index) in newFiles" :key="'new-' + index">
                                    <img :src="getPreviewUrl(file)" :alt="`Preview ${index + 1}`">
                                    <div class="preview-info">
                                        <span>{{ file.name }}</span>
                                        <span>{{ formatFileSize(file.size) }}</span>
                                    </div>
                                    <button type="button" class="remove-image" @click="removeNewImage(index)">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </div>
                            
                            <!-- Информация о загрузке -->
                            <div class="upload-info" v-if="newFiles.length > 0">
                                <p>Новых файлов: {{ newFiles.length }}</p>
                                <p class="file-size-info">Общий размер: {{ formatFileSize(totalFileSize) }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-outline" @click="closeModal">
                            Отмена
                        </button>
                        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                            <i class="fas fa-save"></i> 
                            {{ isSubmitting ? 'Сохранение...' : 'Сохранить изменения' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
        <div class="modal-overlay" @click="closeModal"></div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    props: {
        showModal: Boolean,
        productId: Number,
        productData: Object
    },
    data() {
        return {
            formData: {
                title: '',
                category: '',
                price: '',
                description: '',
                city: '',
                phone: '',
                is_active: true,
                is_bargain: false
            },
            existingImages: [],
            imagesToDelete: [],
            newFiles: [],
            isSubmitting: false,
            errors: []
        }
    },
    computed: {
        totalFileSize() {
            return this.newFiles.reduce((total, file) => total + file.size, 0)
        }
    },
    watch: {
        productData: {
            handler(newData) {
                if (newData) {
                    this.loadProductData(newData);
                }
            },
            immediate: true
        }
    },
    methods: {
        loadProductData(data) {
            this.formData = {
                title: data.title || '',
                category: data.category || '',
                price: data.cost || '',
                description: data.description || '',
                city: data.town || '',
                phone: data.phone_number || '',
                is_active: data.is_active || true,
                is_bargain: data.is_bargain || false
            };
            
            this.existingImages = data.images ? [...data.images] : [];
            this.imagesToDelete = [];
            this.newFiles = [];
        },
        
        getImageUrl(filename) {
            if (!filename) return '/DefaultListingPhoto.png';
            
            let processedFilename = filename;
            if (filename.includes('_PNG')) {
                processedFilename = filename.replace('_PNG', '.png');
            } else if (!filename.includes('.')) {
                processedFilename = filename + '.jpg';
            }
            return '/uploads/' + processedFilename;
        },
        
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        
        handleImageUpload(event) {
            const files = Array.from(event.target.files);
            this.addFiles(files);
            event.target.value = '';
        },
        
        handleDrop(event) {
            const files = Array.from(event.dataTransfer.files);
            this.addFiles(files);
        },
        
        addFiles(files) {
            const maxTotalImages = 5;
            const currentTotal = this.existingImages.length - this.imagesToDelete.length + this.newFiles.length;
            const remainingSlots = maxTotalImages - currentTotal;
            
            const filesToAdd = files.slice(0, remainingSlots);
            
            if (filesToAdd.length < files.length) {
                alert(`Можно загрузить максимум ${maxTotalImages} файлов всего. Доступно ${remainingSlots} слотов`);
            }
            
            filesToAdd.forEach(file => {
                if (!file.type.startsWith('image/')) {
                    alert(`Файл "${file.name}" не является изображением`);
                    return;
                }
                
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (file.size > maxSize) {
                    alert(`Файл "${file.name}" слишком большой. Максимальный размер: 5MB`);
                    return;
                }
                
                if (this.totalFileSize + file.size > 25 * 1024 * 1024) { // 25MB
                    alert(`Общий размер файлов не должен превышать 25MB`);
                    return;
                }
                
                this.newFiles.push(file);
            });
        },
        
        getPreviewUrl(file) {
            return URL.createObjectURL(file);
        },
        
        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        removeExistingImage(index) {
            if (this.existingImages[index]) {
                this.imagesToDelete.push(this.existingImages[index]);
                this.existingImages.splice(index, 1);
            }
        },
        
        removeNewImage(index) {
            if (this.newFiles[index]) {
                URL.revokeObjectURL(this.getPreviewUrl(this.newFiles[index]));
                this.newFiles.splice(index, 1);
            }
        },
        
        validateForm() {
            this.errors = [];
            
            const requiredFields = ['title', 'category', 'price', 'description', 'city', 'phone'];
            requiredFields.forEach(field => {
                if (!this.formData[field] || this.formData[field].toString().trim() === '') {
                    this.errors.push(`Поле "${this.getFieldLabel(field)}" обязательно для заполнения`);
                }
            });
            
            if (this.formData.price && (isNaN(this.formData.price) || this.formData.price < 0)) {
                this.errors.push('Цена должна быть положительным числом');
            }
            
            return this.errors.length === 0;
        },
        
        getFieldLabel(field) {
            const labels = {
                title: 'Заголовок',
                category: 'Категория',
                price: 'Цена',
                description: 'Описание',
                city: 'Город',
                phone: 'Телефон'
            };
            return labels[field] || field;
        },
        
        async handleSubmit() {
            if (!this.validateForm()) {
                alert('Пожалуйста, исправьте ошибки:\n' + this.errors.join('\n'));
                return;
            }
            
            this.isSubmitting = true;
            
            try {
                const formData = new FormData();
                
                Object.keys(this.formData).forEach(key => {
                    if (key === 'is_active' || key === 'is_bargain') {
                        formData.append(key, this.formData[key].toString());
                    } else {
                        formData.append(key, this.formData[key]);
                    }
                });
                
                if (this.newFiles.length > 0) {
                    this.newFiles.forEach((file, index) => {
                        formData.append('images', file);
                    });
                }
                
                if (this.imagesToDelete.length > 0) {
                    formData.append('images_to_delete', JSON.stringify(this.imagesToDelete));
                }
                
                const token = localStorage.getItem('authToken');
                const response = await axios.put(`/api/product/${this.productId}/edit`, formData, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                });
                
                if (response.data) {
                    this.$emit('update-success', response.data);
                    this.closeModal();
                }
            } catch (error) {
                console.error('Ошибка при обновлении:', error);
                const errorMessage = error.response?.data?.error || error.message || 'Ошибка при обновлении объявления';
                alert(`Ошибка: ${errorMessage}`);
            } finally {
                this.isSubmitting = false;
            }
        },
        
        closeModal() {
            this.newFiles.forEach(file => {
                URL.revokeObjectURL(this.getPreviewUrl(file));
            });
            
            this.$emit('close');
        }
    },
    
    beforeUnmount() {
        this.newFiles.forEach(file => {
            URL.revokeObjectURL(this.getPreviewUrl(file));
        });
    },
    
    emits: ['close', 'update-success']
}
</script>

<style scoped>
/* Стили модального окна (используйте стили из MarketModal.vue) */
/* Добавьте дополнительные стили для существующих изображений */

.existing-images {
    margin-bottom: 20px;
}

.existing-images h4 {
    color: var(--text);
    margin-bottom: 15px;
    font-size: 1rem;
    font-weight: 600;
}

.existing-images-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

.existing-image-item {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.existing-image-item img {
    width: 100%;
    height: 100px;
    object-fit: cover;
}

.existing-image-actions {
    padding: 10px;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
}

.btn-small {
    padding: 5px 10px;
    font-size: 0.8rem;
}

.btn-danger {
    background: rgba(255, 0, 0, 0.2);
    color: #ff6b6b;
    border: 1px solid rgba(255, 0, 0, 0.3);
}

.btn-danger:hover {
    background: rgba(255, 0, 0, 0.3);
}

.status-options {
    display: flex;
    gap: 20px;
    margin-top: 10px;
}

.status-option {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}

.status-option input[type="checkbox"] {
    width: 18px;
    height: 18px;
}

.status-label {
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--text);
    font-size: 0.95rem;
}

.status-label i {
    color: var(--primary);
}

.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2000;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.modal.active {
    display: flex;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
}

.modal-content {
    position: relative;
    z-index: 2;
    background: var(--dark-light);
    border-radius: 20px;
    width: 100%;
    max-width: 700px;
    max-height: 90vh;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 30px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
}

.modal-header h3 i {
    color: var(--primary);
}

.modal-close {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: var(--primary);
    border-color: var(--primary);
    transform: rotate(90deg);
}

.modal-body {
    padding: 30px;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
    color: var(--text);
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 15px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    outline: none;
    transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.image-upload {
    margin-top: 10px;
}

.upload-area {
    padding: 40px;
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.upload-area:hover {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.05);
}

.upload-area i {
    font-size: 3rem;
    color: var(--text-secondary);
    margin-bottom: 15px;
}

.upload-area p {
    color: var(--text-secondary);
}

.image-preview {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 15px;
}

.preview-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 10px;
    overflow: hidden;
}

.preview-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.remove-image {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 25px;
    height: 25px;
    background: rgba(255, 0, 0, 0.8);
    border-radius: 50%;
    border: none;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.3s ease;
}

.remove-image:hover {
    transform: scale(1.1);
}

.upload-area {
    cursor: pointer;
    position: relative;
}

.upload-area:hover {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.05);
}

.upload-hint {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 8px;
}

.image-preview {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
    margin-top: 20px;
}

.preview-item {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.preview-item img {
    width: 100%;
    height: 100px;
    object-fit: cover;
}

.preview-info {
    padding: 8px;
    background: rgba(0, 0, 0, 0.7);
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    color: white;
    font-size: 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.preview-info span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.upload-info {
    margin-top: 10px;
    font-size: 0.9rem;
    color: var(--text-secondary);
    display: flex;
    justify-content: space-between;
}

.file-size-info {
    color: var(--primary);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Drag and drop стили */
.upload-area.drag-over {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.1);
    border-style: solid;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 30px;
}

@media (max-width: 768px) {
    .modal-content {
        max-height: 95vh;
    }
}
</style>