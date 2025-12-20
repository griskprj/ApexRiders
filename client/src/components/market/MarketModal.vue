<template>
    <div class="modal" :class="{ active: showModal }">
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-plus-circle"></i> Новое объявление</h3>
                <button class="modal-close" @click="showModal = false">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="submitNewAd">
                    <div class="form-group">
                        <label>Заголовок объявления *</label>
                        <input type="text" v-model="newAd.title" placeholder="Например: Шлем AGV K6, размер L" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Категория *</label>
                            <select v-model="newAd.category" required>
                                <option value="">Выберите категорию</option>
                                <option value="motorcycles">Мотоциклы</option>
                                <option value="parts">Запчасти</option>
                                <option value="gear">Экипировка</option>
                                <option value="accessories">Аксессуары</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Цена (₽) *</label>
                            <input type="number" v-model="newAd.price" placeholder="25000" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Описание *</label>
                        <textarea v-model="newAd.description" placeholder="Подробное описание товара..." rows="4" required></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Город *</label>
                            <input type="text" v-model="newAd.city" placeholder="Москва" required>
                        </div>
                        <div class="form-group">
                            <label>Телефон для связи *</label>
                            <input type="tel" v-model="newAd.phone" placeholder="+7 (XXX) XXX-XX-XX" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Изображения (до 5 шт.)</label>
                        <div class="image-upload">
                            <div class="upload-area" @click="triggerFileInput">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>Нажмите для загрузки изображений</p>
                            </div>
                            <input type="file" ref="fileInput" @change="handleImageUpload" multiple accept="image/*" style="display: none;">
                            <div class="image-preview" v-if="newAd.images.length > 0">
                                <div class="preview-item" v-for="(img, index) in newAd.images" :key="index">
                                    <img :src="img" alt="Preview">
                                    <button class="remove-image" @click="removeImage(index)">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-outline" @click="showModal = false">
                            Отмена
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i> Опубликовать
                        </button>
                    </div>
                </form>
            </div>
        </div>
        <div class="modal-overlay" @click="showModal = false"></div>
    </div>
</template>

<script>
    export default {
        props: {
            showModal: Function,
            submitNewAd: Function,
            triggerFileInput: Function,
            handleImageUpload: Function,
            removeImage: Function,
            newAd: {
                type: Object,
                required: true,
                default: () => ({
                    title: String,
                    category: String,
                    price: Number,
                    description: Text,
                    city: String,
                    phone: String,
                    images: Array
                })
            }
        }
    }
</script>

<style scoped>
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