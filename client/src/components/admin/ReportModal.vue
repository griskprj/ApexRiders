<template>
    <div v-if="visible" class="report-modal-overlay" @click.self="closeModal">
        <div class="report-modal">
            <div class="modal-header">
                <h3><i class="fas fa-flag"></i> Пожаловаться на контент</h3>
                <button @click="closeModal" class="modal-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div class="modal-body">
                <div v-if="loading" class="loading">
                    <div class="spinner"></div>
                    <p>Загрузка...</p>
                </div>
                
                <div v-else class="report-form">
                    <!-- Информация о цели жалобы -->
                    <div class="target-info" v-if="targetContent">
                        <div class="target-header">
                            <i :class="getTargetIcon(targetType)"></i>
                            <span>Вы жалуетесь на {{ getTargetTypeText(targetType) }}</span>
                        </div>
                        
                        <div class="target-preview">
                            <div v-if="targetType === 'post'">
                                <h5>{{ targetContent.title }}</h5>
                                <p>{{ truncateText(targetContent.content, 150) }}</p>
                            </div>
                            
                            <div v-else-if="targetType === 'comment'">
                                <p>{{ truncateText(targetContent.content, 200) }}</p>
                            </div>
                            
                            <div v-else-if="targetType === 'product'">
                                <h5>{{ targetContent.title }}</h5>
                                <p>{{ truncateText(targetContent.description, 150) }}</p>
                            </div>
                            
                            <div v-else-if="targetType === 'manual'">
                                <h5>{{ targetContent.title }}</h5>
                                <p>{{ truncateText(targetContent.content, 150) }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Причина жалобы -->
                    <div class="form-group">
                        <label>
                            <i class="fas fa-exclamation-circle"></i>
                            Причина жалобы *
                        </label>
                        <select v-model="reportData.reason" @change="updatePriority" required>
                            <option value="">Выберите причину...</option>
                            <option value="spam">Спам</option>
                            <option value="abuse">Оскорбления, агрессия</option>
                            <option value="hate_speech">Разжигание ненависти</option>
                            <option value="adult_content">Контент для взрослых</option>
                            <option value="illegal_content">Незаконный контент</option>
                            <option value="misinformation">Ложная информация</option>
                            <option value="copyright_violation">Нарушение авторских прав</option>
                            <option value="impersonation">Выдача себя за другого</option>
                            <option value="harassment">Преследование</option>
                            <option value="other">Другое</option>
                        </select>
                    </div>
                    
                    <!-- Дополнительные детали -->
                    <div class="form-group">
                        <label>
                            <i class="fas fa-align-left"></i>
                            Дополнительные детали
                        </label>
                        <textarea 
                            v-model="reportData.details" 
                            placeholder="Опишите проблему подробнее..."
                            rows="4"
                            :maxlength="500"
                        ></textarea>
                        <div class="char-counter">
                            {{ reportData.details?.length || 0 }}/500 символов
                        </div>
                    </div>
                    
                    <!-- Приоритет (автоматический) -->
                    <div v-if="reportData.priority" class="priority-indicator">
                        <span class="priority-badge" :class="`priority-${reportData.priority}`">
                            <i class="fas fa-exclamation-triangle"></i>
                            Приоритет: {{ getPriorityText(reportData.priority) }}
                        </span>
                        <small>Приоритет определен автоматически на основе причины</small>
                    </div>
                    
                    <!-- Подтверждение -->
                    <div class="warning-box" v-if="userHasReported">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>Вы уже отправляли жалобу на этот контент</p>
                    </div>
                    
                    <div class="warning-box" v-else>
                        <i class="fas fa-info-circle"></i>
                        <p>
                            Жалобы проверяются модераторами в течение 24 часов. 
                            Ложные жалобы могут привести к ограничению вашего аккаунта.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button @click="closeModal" class="btn btn-outline" :disabled="submitting">
                    Отмена
                </button>
                <button 
                    @click="submitReport" 
                    class="btn btn-danger" 
                    :disabled="!canSubmit || submitting"
                >
                    <span v-if="submitting">
                        <i class="fas fa-spinner fa-spin"></i> Отправка...
                    </span>
                    <span v-else>
                        <i class="fas fa-paper-plane"></i> Отправить жалобу
                    </span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ReportModal',
    
    props: {
        visible: {
            type: Boolean,
            required: true
        },
        targetId: {
            type: [Number, String],
            required: true
        },
        targetType: {
            type: String,
            required: true,
            validator: (value) => ['post', 'comment', 'product', 'manual'].includes(value)
        },
        targetOwnerId: {
            type: [Number, String],
            required: true
        }
    },
    
    data() {
        return {
            loading: true,
            submitting: false,
            targetContent: null,
            userHasReported: false,
            
            reportData: {
                reason: '',
                details: '',
                priority: 'low'
            },
            
            reasonToPriority: {
                'spam': 'low',
                'abuse': 'high',
                'hate_speech': 'high',
                'adult_content': 'high',
                'illegal_content': 'high',
                'misinformation': 'medium',
                'copyright_violation': 'medium',
                'impersonation': 'medium',
                'harassment': 'high',
                'other': 'low'
            }
        }
    },
    
    computed: {
        canSubmit() {
            return this.reportData.reason.trim() !== '' && !this.userHasReported
        }
    },
    
    watch: {
        visible: {
            immediate: true,
            handler(newVal) {
                console.log('ReportModal visible изменился:', newVal);
                if (newVal) {
                    console.log('Загружаю данные для репорта:', {
                        targetId: this.targetId,
                        targetType: this.targetType,
                        targetOwnerId: this.targetOwnerId
                    });
                    this.loadData()
                } else {
                    console.log('Закрываю модалку, сбрасываю форму');
                    this.resetForm()
                }
            }
        }
    },
    
    methods: {
        async loadData() {
            this.loading = true
            
            try {
                // Загружаем информацию о контенте
                await this.fetchTargetContent()
                
                // Проверяем, отправлял ли пользователь уже жалобу
                await this.checkUserReport()
            } catch (error) {
                console.error('Error loading report data:', error)
            } finally {
                this.loading = false
            }
        },
        
        async fetchTargetContent() {
            try {
                let url = '';
                
                const token = localStorage.getItem('authToken');
                const headers = {
                    'Content-Type': 'application/json'
                };
                
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }
                
                // Используйте правильные endpoint'ы
                switch (this.targetType) {
                    case 'post':
                        url = `/api/posts/${this.targetId}`;
                        break;
                    case 'comment':
                        url = `/api/comments/${this.targetId}`;
                        break;
                    case 'product':
                        url = `/api/products/${this.targetId}`;
                        break;
                    case 'manual':
                        url = `/api/manuals/${this.targetId}`;
                        break;
                    default:
                        console.error('Неизвестный тип цели:', this.targetType);
                        this.targetContent = this.createStubContent();
                        return;
                }
                
                console.log('Запрашиваю URL:', url); // Для отладки
                
                const response = await fetch(url, { headers });
                
                if (!response.ok) {
                    console.error(`Ошибка ${response.status}: ${response.statusText}`);
                    this.targetContent = this.createStubContent();
                    return;
                }
                
                const data = await response.json();
                console.log('Получены данные:', data); // Для отладки
                
                // Обработка данных в зависимости от типа
                switch (this.targetType) {
                    case 'post':
                        this.targetContent = {
                            title: data.title || data.name || 'Без названия',
                            content: data.content || data.text || data.description || '',
                            description: data.description || ''
                        };
                        break;
                        
                    case 'comment':
                        this.targetContent = {
                            content: data.content || data.text || 'Комментарий',
                            author: data.author || {}
                        };
                        break;
                        
                    case 'product':
                        this.targetContent = {
                            title: data.title || data.name || 'Продукт',
                            description: data.description || data.content || ''
                        };
                        break;
                        
                    case 'manual':
                        this.targetContent = {
                            title: data.title || data.name || 'Мануал',
                            content: data.content || data.text || data.description || ''
                        };
                        break;
                }
                
            } catch (error) {
                console.error(`Ошибка при получении ${this.targetType}:`, error);
                this.targetContent = this.createStubContent();
            }
        },

        createStubContent() {
            const stubText = 'Контент временно недоступен';
            const stubTitle = 'Контент';
            
            return {
                title: stubTitle,
                content: stubText,
                description: stubText
            };
        },
        
        async checkUserReport() {
            try {
                const token = localStorage.getItem('authToken')
                
                if (!token) {
                    this.userHasReported = false
                    return
                }
                
                const response = await fetch(`/api/reports/check?target_id=${this.targetId}&target_type=${this.targetType}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                if (response.ok) {
                    const data = await response.json()
                    this.userHasReported = data.has_reported || false
                }
            } catch (error) {
                console.error('Error checking user report:', error)
            }
        },
        
        updatePriority() {
            if (this.reportData.reason && this.reasonToPriority[this.reportData.reason]) {
                this.reportData.priority = this.reasonToPriority[this.reportData.reason]
            }
        },
        
        async submitReport() {
            if (!this.canSubmit || this.submitting) return
            
            this.submitting = true
            
            try {
                const token = localStorage.getItem('authToken')
                
                if (!token) {
                    alert('Для отправки жалобы необходимо авторизоваться')
                    this.closeModal()
                    return
                }
                
                const response = await fetch('/api/reports', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        target_id: this.targetId,
                        target_type: this.targetType,
                        target_owner_id: this.targetOwnerId,
                        reason: this.reportData.reason,
                        details: this.reportData.details || '',
                        priority: this.reportData.priority
                    })
                })
                
                if (response.ok) {
                    const data = await response.json()
                    
                    // Показываем подтверждение
                    this.$emit('report-submitted', data)
                    
                    // Закрываем модалку с задержкой
                    setTimeout(() => {
                        this.closeModal()
                        alert('Жалоба успешно отправлена. Спасибо!')
                    }, 500)
                    
                } else {
                    const errorData = await response.json()
                    throw new Error(errorData.error || 'Ошибка при отправке жалобы')
                }
                
            } catch (error) {
                console.error('Error submitting report:', error)
                alert(`Ошибка при отправке жалобы: ${error.message}`)
            } finally {
                this.submitting = false
            }
        },
        
        closeModal() {
            this.$emit('update:visible', false)
        },
        
        resetForm() {
            this.reportData = {
                reason: '',
                details: '',
                priority: 'low'
            }
            this.loading = true
            this.submitting = false
            this.targetContent = null
            this.userHasReported = false
        },
        
        getTargetIcon(type) {
            const icons = {
                'post': 'fas fa-newspaper',
                'comment': 'fas fa-comment',
                'product': 'fas fa-shopping-cart',
                'manual': 'fas fa-book'
            }
            return icons[type] || 'fas fa-file'
        },
        
        getTargetTypeText(type) {
            const texts = {
                'post': 'пост',
                'comment': 'комментарий',
                'product': 'объявление',
                'manual': 'мануал'
            }
            return texts[type] || type
        },
        
        getPriorityText(priority) {
            const texts = {
                'high': 'Высокий',
                'medium': 'Средний',
                'low': 'Низкий'
            }
            return texts[priority] || priority
        },
        
        truncateText(text, maxLength) {
            if (!text) return ''
            if (text.length <= maxLength) return text
            return text.substring(0, maxLength) + '...'
        }
    }
}
</script>

<style scoped>
.report-modal-overlay {
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

.report-modal {
    background: var(--dark-light);
    border-radius: 15px;
    width: 100%;
    max-width: 500px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.2rem;
    color: var(--text);
}

.modal-header i {
    color: var(--danger);
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
    padding: 20px;
    max-height: 60vh;
    overflow-y: auto;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    padding: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    text-align: center;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--danger);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
}

.target-info {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.target-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.target-header i {
    color: var(--primary);
}

.target-preview {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    padding: 12px;
    border-left: 3px solid var(--primary);
}

.target-preview h5 {
    margin-bottom: 8px;
    color: var(--text);
    font-size: 1rem;
}

.target-preview p {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.4;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--text);
    font-size: 0.95rem;
}

.form-group label i {
    color: var(--danger);
}

.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text);
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--danger);
    box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
    font-family: inherit;
}

.char-counter {
    text-align: right;
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 5px;
}

.priority-indicator {
    margin: 20px 0;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    border-left: 3px solid var(--warning);
}

.priority-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 5px;
}

.priority-high {
    background: rgba(220, 53, 69, 0.2);
    color: var(--danger);
}

.priority-medium {
    background: rgba(255, 193, 7, 0.2);
    color: var(--warning);
}

.priority-low {
    background: rgba(40, 167, 69, 0.2);
    color: var(--success);
}

.priority-indicator small {
    display: block;
    color: var(--text-secondary);
    font-size: 0.8rem;
}

.warning-box {
    display: flex;
    gap: 12px;
    padding: 15px;
    background: rgba(255, 193, 7, 0.1);
    border: 1px solid rgba(255, 193, 7, 0.2);
    border-radius: 8px;
    margin-top: 20px;
}

.warning-box i {
    color: var(--warning);
    font-size: 1.2rem;
    flex-shrink: 0;
}

.warning-box p {
    color: var(--warning);
    font-size: 0.9rem;
    line-height: 1.4;
    margin: 0;
}

.btn {
    padding: 10px 25px;
    border-radius: 8px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.95rem;
}

.btn-outline {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: var(--text);
}

.btn-outline:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
}

.btn-danger {
    background: var(--danger);
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background: #dc3545;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(220, 53, 69, 0.3);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
    .report-modal {
        max-width: 100%;
        margin: 20px;
    }
    
    .modal-footer {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
    }
}
</style>