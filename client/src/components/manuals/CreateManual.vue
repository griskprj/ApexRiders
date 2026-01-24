<template>
    <section class="create-manual">
        <!-- Декоративные элементы -->
        <div class="decoration decoration-1"></div>
        <div class="decoration decoration-2"></div>

        <!-- Заголовок -->
        <div class="create-header">
            <h1 class="create-title">
                <i class="fas fa-tools"></i>
                <span>Конструктор мануалов</span>
            </h1>
            <p class="create-subtitle">Создайте пошаговое руководство по ремонту или обслуживанию</p>
        </div>

        <!-- Основная форма -->
        <div class="create-container">
            <!-- Информация о мануале -->
            <div class="create-card">
                <h3 class="card-title">
                    <i class="fas fa-info-circle"></i>
                    Основная информация
                </h3>
                
                <div class="form-group">
                    <label for="manual-title">Название мануала *</label>
                    <input 
                        type="text" 
                        id="manual-title" 
                        v-model="manual.title"
                        placeholder="Например: Замена масла в двигателе Yamaha R6"
                        class="form-input"
                        required
                    >
                </div>

                <div class="form-group">
                    <label for="manual-moto">Мотоцикл (марка, модель, год) *</label>
                    <input 
                        type="text" 
                        id="manual-moto" 
                        v-model="manual.moto_type"
                        placeholder="Например: Yamaha R6 2018"
                        class="form-input"
                        required
                    >
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="manual-category">Категория *</label>
                        <select id="manual-category" v-model="manual.category" class="form-select">
                            <option value="">Выберите категорию</option>
                            <option value="Двигатель">Двигатель</option>
                            <option value="Трансмиссия">Трансмиссия</option>
                            <option value="Тормозная система">Тормозная система</option>
                            <option value="Подвеска">Подвеска</option>
                            <option value="Электрика">Электрика</option>
                            <option value="Обслуживание">Обслуживание</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="manual-difficulty">Сложность *</label>
                        <select id="manual-difficulty" v-model="manual.difficulty" class="form-select">
                            <option value="">Уровень сложности</option>
                            <option value="Начинающий">Начинающий</option>
                            <option value="Средний">Средний</option>
                            <option value="Продвинутый">Продвинутый</option>
                            <option value="Эксперт">Эксперт</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label for="manual-desc">Описание мануала *</label>
                    <textarea 
                        id="manual-desc" 
                        v-model="manual.description"
                        rows="3"
                        placeholder="Кратко опишите, что пользователь сможет сделать с помощью этого мануала..."
                        class="form-textarea"
                        required
                    ></textarea>
                </div>

                <div class="form-group">
                    <label for="manual-time">Примерное время выполнения</label>
                    <input 
                        type="text" 
                        id="manual-time" 
                        v-model="manual.estimated_time"
                        placeholder="Например: 2-3 часа"
                        class="form-input"
                    >
                </div>
            </div>

            <!-- Шаги мануала -->
            <div class="create-card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-list-ol"></i>
                        Шаги мануала
                    </h3>
                    <button type="button" @click="addStep" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Добавить шаг
                    </button>
                </div>

                <div v-if="steps.length === 0" class="empty-steps">
                    <div class="empty-icon">
                        <i class="fas fa-list-ul"></i>
                    </div>
                    <p>Добавьте первый шаг вашего мануала</p>
                </div>

                <draggable 
                    v-model="steps" 
                    handle=".step-handle"
                    class="steps-list"
                >
                    <div v-for="(step, index) in steps" :key="step.id" class="step-item">
                        <div class="step-header">
                            <div class="step-number">
                                <i class="fas fa-grip-vertical step-handle"></i>
                                <span class="number">Шаг {{ index + 1 }}</span>
                            </div>
                            <button type="button" @click="removeStep(index)" class="btn-icon danger">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>

                        <div class="step-content">
                            <div class="form-group">
                                <label :for="'step-title-' + index">Заголовок шага *</label>
                                <input 
                                    type="text" 
                                    :id="'step-title-' + index"
                                    v-model="step.title"
                                    placeholder="Например: Сливаем старое масло"
                                    class="form-input"
                                    required
                                >
                            </div>

                            <div class="form-group">
                                <label :for="'step-desc-' + index">Описание действий *</label>
                                <textarea 
                                    :id="'step-desc-' + index"
                                    v-model="step.description"
                                    rows="4"
                                    placeholder="Подробно опишите, что нужно сделать на этом шаге. Укажите инструменты, материалы, предупреждения..."
                                    class="form-textarea"
                                    required
                                ></textarea>
                            </div>

                            <div class="step-media">
                                <div class="form-group">
                                    <label :for="'step-image-' + index">Изображение</label>
                                    <div class="image-upload">
                                        <input 
                                            type="file" 
                                            :id="'step-image-' + index"
                                            @change="handleImageUpload($event, index)"
                                            accept="image/*"
                                            class="file-input"
                                        >
                                        <div class="upload-area" @click="triggerFileInput(index)">
                                            <div v-if="step.image_url" class="image-preview">
                                                <img :src="step.image_url" alt="Превью">
                                                <button type="button" @click.stop="removeImage(index)" class="btn-icon danger">
                                                    <i class="fas fa-times"></i>
                                                </button>
                                            </div>
                                            <div v-else class="upload-placeholder">
                                                <i class="fas fa-camera"></i>
                                                <p>Нажмите для загрузки фото</p>
                                                <span class="upload-hint">JPG, PNG до 5MB</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label :for="'step-video-' + index">Видео (опционально)</label>
                                    <input 
                                        type="text" 
                                        :id="'step-video-' + index"
                                        v-model="step.video_url"
                                        placeholder="Ссылка на YouTube или Vimeo"
                                        class="form-input"
                                    >
                                </div>
                            </div>
                        </div>
                    </div>
                </draggable>
            </div>

            <!-- Дополнительная информация -->
            <div class="create-card">
                <h3 class="card-title">
                    <i class="fas fa-toolbox"></i>
                    Инструменты и материалы
                </h3>

                <div class="form-group">
                    <label>Необходимые инструменты</label>
                    <div class="tags-input">
                        <div class="tags-list">
                            <span v-for="(tool, index) in manual.tools" :key="index" class="tag">
                                {{ tool }}
                                <button type="button" @click="removeTag('tools', index)" class="tag-remove">
                                    <i class="fas fa-times"></i>
                                </button>
                            </span>
                        </div>
                        <div class="tag-input">
                            <input 
                                type="text" 
                                v-model="newTool"
                                @keydown.enter.prevent="addTag('tools')"
                                placeholder="Добавить инструмент и нажмите Enter"
                                class="tag-form-input"
                            >
                            <button type="button" @click="addTag('tools')" class="btn-icon">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label>Необходимые материалы</label>
                    <div class="tags-input">
                        <div class="tags-list">
                            <span v-for="(material, index) in manual.materials" :key="index" class="tag">
                                {{ material }}
                                <button type="button" @click="removeTag('materials', index)" class="tag-remove">
                                    <i class="fas fa-times"></i>
                                </button>
                            </span>
                        </div>
                        <div class="tag-input">
                            <input 
                                type="text" 
                                v-model="newMaterial"
                                @keydown.enter.prevent="addTag('materials')"
                                placeholder="Добавить материал и нажмите Enter"
                                class="tag-form-input"
                            >
                            <button type="button" @click="addTag('materials')" class="btn-icon">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="manual-warnings">Важные предупреждения</label>
                    <textarea 
                        id="manual-warnings" 
                        v-model="manual.warnings"
                        rows="3"
                        placeholder="Укажите потенциальные опасности, меры предосторожности..."
                        class="form-textarea"
                    ></textarea>
                </div>
            </div>

            <!-- Панель управления -->
            <div class="create-actions">
                <button type="button" @click="saveDraft" class="btn btn-secondary">
                    <i class="fas fa-save"></i> Сохранить черновик
                </button>
                <button type="button" @click="previewManual" class="btn btn-outline">
                    <i class="fas fa-eye"></i> Предпросмотр
                </button>
                <button type="button" @click="publishManual" :disabled="!isFormValid" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Опубликовать мануал
                </button>
            </div>
        </div>

        <!-- Модальное окно предпросмотра -->
        <div v-if="showPreview" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Предпросмотр мануала</h3>
                    <button @click="showPreview = false" class="btn-icon">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <!-- Здесь будет компонент предпросмотра -->
                    <ManualPreview :manual="manual" :steps="steps" />
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import ManualPreview from './ManualPreview.vue';

export default {
    name: 'CreateManual',
    components: {
        ManualPreview
    },

    setup() {
        const manual = ref({
            title: '',
            moto_type: '',
            category: '',
            difficulty: '',
            description: '',
            estimated_time: '',
            tools: [],
            materials: [],
            warnings: ''
        })

        const steps = ref([])
        const newTool = ref('')
        const newMaterial = ref('')
        const showPreview = ref(false)
        const stepCounter = ref(0)

        const isFormValid = computed(() => {
            return manual.value.title &&
                   manual.value.moto_type &&
                   manual.value.category &&
                   manual.value.difficulty &&
                   manual.value.description &&
                   steps.value.length > 0 &&
                   steps.value.every(step => step.title && step.description)
        })

        const generateStepId = () => {
            return `step_${Date.now()}_${stepCounter.value++}`
        }

        const addStep = () => {
            steps.value.push({
                id: generateStepId(),
                title: '',
                description: '',
                image_url: '',
                video_url: '',
                order: steps.value.length
            })
        }

        const removeStep = (index) => {
            steps.value.splice(index, 1)
            steps.value.forEach((step, idx) => {
                step.order = idx
            })
        }

        const handleImageUpload = (event, index) => {
            const file = event.target.files[0]
            if (!file) return

            if (file.size > 5 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер: 5MB')
                return
            }

            const reader = new FileReader()
            reader.onload = (e) => {
                steps.value[index].image_url = e.target.result
                uploadImageToServer(file, index)
            }
            reader.readAsDataURL(file)
        }

        const uploadImageToServer = async (file, stepIndex) => {
            const formData = new FormData()
            formData.append('image', file)
            formData.append('step_index', stepIndex)

            try {
                const token = localStorage.getItem('authToken')
                const response = await axios.post('/api/manuals/constructor/upload-image', formData, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                })
                
                if (response.data.success) {
                    steps.value[stepIndex].image_url = response.data.image_url
                }
            } catch (error) {
                console.error('Ошибка загрузки изображения:', error)
                alert('Не удалось загрузить изображение')
            }
        }

        const removeImage = (index) => {
            steps.value[index].image_url = ''
        }

        const triggerFileInput = (index) => {
            document.getElementById(`step-image-${index}`).click()
        }

        const addTag = (type) => {
            const value = type === 'tools' ? newTool.value : newMaterial.value
            if (value.trim()) {
                manual.value[type].push(value.trim())
                if (type === 'tools') newTool.value = ''
                else newMaterial.value = ''
            }
        }

        const removeTag = (type, index) => {
            manual.value[type].splice(index, 1)
        }

        const saveDraft = async () => {
            const draftData = {
                manual: manual.value,
                steps: steps.value,
                saved_at: new Date().toISOString()
            }

            try {
                const token = localStorage.getItem('authToken')
                await axios.post('/api/manuals/constructor/draft', draftData, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                alert('Черновик сохранен')
            } catch (error) {
                console.error('Ошибка сохранения черновика:', error)
                alert('Не удалось сохранить черновик')
            }
        }

        const previewManual = () => {
            showPreview.value = true
        }

        const publishManual = async () => {
            if (!isFormValid.value) {
                alert('Заполните все обязательные поля')
                return
            }

            const manualData = {
                ...manual.value,
                steps: steps.value,
                published_at: new Date().toISOString(),
                status: 'published'
            }

            try {
                const token = localStorage.getItem('authToken')
                const response = await axios.post('/api/manuals/constructor/create', manualData, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data.success) {
                    alert('Мануал успешно опубликован!')
                    window.location.href = `/manual/${response.data.manual_id}`
                }
            } catch (error) {
                console.error('Ошибка публикации:', error)
                alert('Не удалось опубликовать мануал')
            }
        }

        onMounted(async () => {
            const token = localStorage.getItem('authToken')
            if (!token) {
                window.location.href = '/login'
                return
            }

            try {
                const response = await axios.get('/api/manuals/constructor/verify-access', {
                    headers: { 'Authorization': `Bearer ${token}`}
                })

                if (response.data.admin_level < 1) {
                    alert('Только пользователи с уровнем админа 1 могут создать мануалы')
                    this.$router.push('/manuals')
                    return
                }

                const draftResponse = await axios.get('/api/manuals/constructor/draft', {
                    headers: { 'Authorization': `Bearer ${token}` }
                })

                if (draftResponse.data) {
                    manual.value = draftResponse.data.manual || manual.value
                    steps.value = draftResponse.data.steps || []

                    if (!manual.value.tools || !Array.isArray(manual.value.tools)) {
                        manual.value.tools = []
                    }
                    if (!manual.value.materials || !Array.isArray(manual.value.materials)) {
                        manual.value.materials = []
                    }
                }
            } catch (error) {
                console.error('Ошибка загрузки:', error)
            }
        })

        return {
            manual,
            steps,
            newTool,
            newMaterial,
            showPreview,
            isFormValid,
            addStep,
            removeStep,
            handleImageUpload,
            removeImage,
            triggerFileInput,
            addTag,
            removeTag,
            saveDraft,
            previewManual,
            publishManual
        }
    }
}
</script>

<style scoped>
.create-manual {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

.create-header {
    margin-bottom: 40px;
}

.create-title {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 2.8rem;
    font-weight: 300;
    margin-bottom: 15px;
    color: var(--text);
}

.create-title i {
    color: var(--primary);
    text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
}

.create-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: 30px;
    max-width: 600px;
}

.create-container {
    max-width: 900px;
    margin: 0 auto;
}

.create-card {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    margin-bottom: 25px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.card-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 25px;
    color: var(--text);
}

.card-title i {
    color: var(--primary);
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

.form-input,
.form-select,
.form-textarea {
    width: 100%;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

.form-textarea {
    resize: vertical;
    min-height: 80px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

/* Шаги */
.empty-steps {
    text-align: center;
    padding: 40px 20px;
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    margin-bottom: 20px;
}

.empty-steps .empty-icon {
    font-size: 48px;
    color: var(--text-secondary);
    margin-bottom: 15px;
    opacity: 0.5;
}

.empty-steps p {
    color: var(--text-secondary);
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.step-item {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 20px;
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.step-number {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--primary);
    font-weight: 600;
}

.step-handle {
    cursor: move;
    color: var(--text-secondary);
}

.step-handle:hover {
    color: var(--primary);
}

.step-media {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 15px;
}

.image-upload {
    margin-top: 5px;
}

.file-input {
    display: none;
}

.upload-area {
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.upload-area:hover {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.05);
}

.upload-placeholder {
    text-align: center;
    color: var(--text-secondary);
}

.upload-placeholder i {
    font-size: 32px;
    margin-bottom: 10px;
    opacity: 0.5;
}

.upload-hint {
    font-size: 0.85rem;
    opacity: 0.7;
}

.image-preview {
    position: relative;
    width: 100%;
    height: 100%;
}

.image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

.image-preview .btn-icon {
    position: absolute;
    top: 5px;
    right: 5px;
    background: rgba(0, 0, 0, 0.7);
}

/* Теги */
.tags-input {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 10px;
}

.tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255, 255, 255, 0.1);
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 0.9rem;
}

.tag-remove {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0;
    font-size: 0.8rem;
}

.tag-remove:hover {
    color: var(--danger);
}

.tag-input {
    display: flex;
    gap: 8px;
}

.tag-form-input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text);
    padding: 8px;
    font-size: 1rem;
}

.tag-form-input:focus {
    outline: none;
}

/* Кнопки */
.create-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    padding-top: 30px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn {
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: var(--primary-dark);
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--primary);
}

.btn-outline {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--primary);
}

.btn-outline:hover {
    background: rgba(255, 69, 0, 0.1);
}

.btn-icon {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 8px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-icon:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.btn-icon.danger:hover {
    background: rgba(220, 53, 69, 0.2);
    color: var(--danger);
}

/* Модальное окно */
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
    background: var(--dark);
    border-radius: 20px;
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    margin: 0;
    color: var(--text);
}

.modal-body {
    padding: 30px;
    overflow-y: auto;
    max-height: calc(90vh - 80px);
}

/* Адаптивность */
@media (max-width: 768px) {
    .create-manual {
        padding: 100px 5% 40px;
    }
    
    .create-title {
        font-size: 2.2rem;
    }
    
    .form-row,
    .step-media {
        grid-template-columns: 1fr;
    }
    
    .create-actions {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .create-title {
        font-size: 1.8rem;
    }
    
    .create-card {
        padding: 20px;
    }
    
    .step-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
}
</style>