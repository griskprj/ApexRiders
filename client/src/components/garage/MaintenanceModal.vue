<template>
    <div class="modal-overlay" @click.self="handleClose">
        <div class="maintenance-modal">
            <!-- Заголовок -->
            <div class="modal-header">
                <h2>{{ isEditing ? 'Редактировать задачу ТО' : 'Новая задача ТО' }}</h2>
                <button class="close-btn" @click="handleClose">
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <!-- Форма -->
            <form @submit.prevent="handleSubmit" class="modal-form">
                <!-- Основная информация -->
                <div class="form-section">
                    <h3>Основная информация</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="title">Название задачи *</label>
                            <input
                                id="title"
                                v-model="formData.title"
                                type="text"
                                placeholder="Например: Замена масла"
                                required
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="maintenance_type">Тип обслуживания</label>
                            <select id="maintenance_type" v-model="formData.maintenance_type">
                                <option value="regular">Регулярное</option>
                                <option value="scheduled">Плановое</option>
                                <option value="emergency">Экстренное</option>
                                <option value="upgrade">Апгрейд</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="description">Описание</label>
                        <textarea
                            id="description"
                            v-model="formData.description"
                            placeholder="Подробное описание работы..."
                            rows="3"
                        ></textarea>
                    </div>
                </div>

                <!-- Планирование -->
                <div class="form-section">
                    <h3>Планирование</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="schedule_type">Тип расписания *</label>
                            <select 
                                id="schedule_type" 
                                v-model="formData.schedule_type"
                                @change="handleScheduleTypeChange"
                            >
                                <option value="mileage">По пробегу</option>
                                <option value="time">По времени</option>
                                <option value="manual">Вручную</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="priority">Приоритет</label>
                            <select id="priority" v-model="formData.priority">
                                <option value="low">Низкий</option>
                                <option value="medium">Средний</option>
                                <option value="high">Высокий</option>
                                <option value="critical">Критический</option>
                            </select>
                        </div>
                    </div>

                    <!-- Интервал по пробегу -->
                    <div v-if="formData.schedule_type === 'mileage'" class="form-row">
                        <div class="form-group">
                            <label for="last_maintenance_mileage">Последний пробег (км)</label>
                            <input
                                id="last_maintenance_mileage"
                                v-model.number="formData.last_maintenance_mileage"
                                type="number"
                                min="0"
                                placeholder="Текущий пробег мотоцикла"
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="interval_value">Интервал (км) *</label>
                            <input
                                id="interval_value"
                                v-model.number="formData.interval_value"
                                type="number"
                                min="100"
                                step="100"
                                required
                                placeholder="Например: 5000"
                            />
                        </div>
                    </div>

                    <!-- Интервал по времени -->
                    <div v-if="formData.schedule_type === 'time'" class="form-row">
                        <div class="form-group">
                            <label for="interval_value_time">Интервал *</label>
                            <div class="interval-input">
                                <input
                                    id="interval_value_time"
                                    v-model.number="formData.interval_value"
                                    type="number"
                                    min="1"
                                    required
                                    placeholder="Например: 6"
                                />
                                <select v-model="formData.interval_unit">
                                    <option value="days">Дней</option>
                                    <option value="weeks">Недель</option>
                                    <option value="months">Месяцев</option>
                                    <option value="years">Лет</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="last_maintenance_date">Последнее выполнение</label>
                            <input
                                id="last_maintenance_date"
                                v-model="formData.last_maintenance_date"
                                type="date"
                            />
                        </div>
                    </div>

                    <div class="form-checkbox">
                        <input
                            id="is_recurring"
                            v-model="formData.is_recurring"
                            type="checkbox"
                        />
                        <label for="is_recurring">Повторяющаяся задача</label>
                    </div>
                </div>

                <!-- Детали выполнения -->
                <div class="form-section">
                    <h3>Детали выполнения</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="cost">Стоимость (руб)</label>
                            <input
                                id="cost"
                                v-model.number="formData.cost"
                                type="number"
                                min="0"
                                step="100"
                                placeholder="0"
                            />
                        </div>
                        
                        <div v-if="isEditing" class="form-group">
                            <label for="status">Статус</label>
                            <select id="status" v-model="formData.status">
                                <option value="pending">Ожидает</option>
                                <option value="in_progress">В процессе</option>
                                <option value="completed">Выполнено</option>
                                <option value="cancelled">Отменено</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="parts_used">Использованные запчасти</label>
                        <textarea
                            id="parts_used"
                            v-model="formData.parts_used"
                            placeholder="Например: Масло Motul 10W-40, фильтр масляный"
                            rows="2"
                        ></textarea>
                    </div>

                    <div class="form-group">
                        <label for="notes">Примечания</label>
                        <textarea
                            id="notes"
                            v-model="formData.notes"
                            placeholder="Дополнительная информация..."
                            rows="2"
                        ></textarea>
                    </div>
                </div>

                <!-- Информация о следующем обслуживании -->
                <div v-if="showNextMaintenanceInfo" class="next-maintenance-info">
                    <h4>Следующее обслуживание:</h4>
                    <div v-if="formData.schedule_type === 'mileage'" class="info-item">
                        <i class="fas fa-tachometer-alt"></i>
                        <span>Пробег: {{ nextMileage }} км</span>
                    </div>
                    <div v-if="formData.schedule_type === 'time' && nextDate" class="info-item">
                        <i class="far fa-calendar-alt"></i>
                        <span>Дата: {{ formatDate(nextDate) }}</span>
                    </div>
                </div>

                <!-- Кнопки -->
                <div class="modal-actions">
                    <button type="button" class="btn-secondary" @click="handleClose">
                        Отмена
                    </button>
                    <button type="submit" class="btn-primary" :disabled="isSubmitting">
                        <span v-if="isSubmitting">
                            <i class="fas fa-spinner fa-spin"></i>
                            Сохранение...
                        </span>
                        <span v-else>{{ isEditing ? 'Сохранить' : 'Создать' }}</span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'

export default {
    name: 'MaintenanceModal',
    
    props: {
        motorcycleId: {
            type: [String, Number],
            required: true
        },
        task: {
            type: Object,
            default: null
        }
    },
    
    emits: ['save', 'close'],
    
    setup(props, { emit }) {
        const isSubmitting = ref(false)
        const isEditing = computed(() => !!props.task?.id)

        // Данные формы
        const formData = ref({
            motorcycle_id: props.motorcycleId,
            title: '',
            description: '',
            maintenance_type: 'regular',
            schedule_type: 'mileage',
            interval_value: 5000,
            interval_unit: 'months',
            last_maintenance_date: '',
            last_maintenance_mileage: 0,
            priority: 'medium',
            is_recurring: true,
            cost: null,
            parts_used: '',
            notes: '',
            status: 'pending'
        })

        // Инициализация данных из props
        onMounted(() => {
            if (props.task) {
                formData.value = {
                    ...formData.value,
                    ...props.task,
                    motorcycle_id: props.motorcycleId
                }
            }
        })

        // Расчет следующего пробега
        const nextMileage = computed(() => {
            if (formData.value.schedule_type === 'mileage') {
                const lastMileage = formData.value.last_maintenance_mileage || 0
                const interval = formData.value.interval_value || 0
                return lastMileage + interval
            }
            return null
        })

        // Расчет следующей даты
        const nextDate = computed(() => {
            if (formData.value.schedule_type === 'time' && formData.value.last_maintenance_date) {
                const lastDate = new Date(formData.value.last_maintenance_date)
                const interval = formData.value.interval_value || 0
                const unit = formData.value.interval_unit
                
                const newDate = new Date(lastDate)
                
                switch (unit) {
                    case 'days':
                        newDate.setDate(newDate.getDate() + interval)
                        break
                    case 'weeks':
                        newDate.setDate(newDate.getDate() + interval * 7)
                        break
                    case 'months':
                        newDate.setMonth(newDate.getMonth() + interval)
                        break
                    case 'years':
                        newDate.setFullYear(newDate.getFullYear() + interval)
                        break
                }
                
                return newDate
            }
            return null
        })

        // Показывать информацию о следующем обслуживании
        const showNextMaintenanceInfo = computed(() => {
            return formData.value.schedule_type !== 'manual' && 
                   formData.value.interval_value > 0
        })

        // Обработчики
        const handleScheduleTypeChange = () => {
            // Сброс значений при изменении типа расписания
            if (formData.value.schedule_type === 'mileage') {
                formData.value.interval_value = 5000
                formData.value.last_maintenance_mileage = 0
            } else if (formData.value.schedule_type === 'time') {
                formData.value.interval_value = 6
                formData.value.interval_unit = 'months'
                formData.value.last_maintenance_date = new Date().toISOString().split('T')[0]
            }
        }

        const handleSubmit = async () => {
            isSubmitting.value = true
            
            try {
                // Подготовка данных для отправки
                const dataToSend = {
                    ...formData.value,
                    next_maintenance_mileage: formData.value.schedule_type === 'mileage' ? nextMileage.value : null,
                    next_maintenance_date: formData.value.schedule_type === 'time' ? nextDate.value?.toISOString() : null
                }
                
                // Удаляем лишние поля
                delete dataToSend.id
                delete dataToSend.created_at
                delete dataToSend.updated_at
                
                emit('save', dataToSend)
            } finally {
                isSubmitting.value = false
            }
        }

        const handleClose = () => {
            emit('close')
        }

        // Форматирование даты
        const formatDate = (date) => {
            return new Date(date).toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            })
        }

        return {
            formData,
            isSubmitting,
            isEditing,
            nextMileage,
            nextDate,
            showNextMaintenanceInfo,
            handleScheduleTypeChange,
            handleSubmit,
            handleClose,
            formatDate
        }
    }
}
</script>

<style scoped>
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
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.maintenance-modal {
    background: var(--dark-light);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideUp 0.3s ease;
}

@keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
    position: sticky;
    top: 0;
    z-index: 10;
}

.modal-header h2 {
    margin: 0;
    color: var(--light);
    font-size: 1.5rem;
}

.close-btn {
    background: none;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--gray);
    cursor: pointer;
    transition: all 0.3s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--light);
}

.modal-form {
    padding: 30px;
}

.form-section {
    margin-bottom: 30px;
    padding-bottom: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.form-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.form-section h3 {
    margin: 0 0 20px 0;
    color: var(--light);
    font-size: 1.2rem;
    font-weight: 500;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    color: var(--gray);
    font-size: 0.9rem;
    font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--light);
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(var(--primary-rgb), 0.2);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

.form-group textarea {
    resize: vertical;
    min-height: 60px;
}

.interval-input {
    display: flex;
    gap: 10px;
}

.interval-input input {
    flex: 1;
}

.interval-input select {
    min-width: 120px;
}

.form-checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}

.form-checkbox input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--primary);
}

.form-checkbox label {
    color: var(--light);
    font-size: 0.95rem;
    cursor: pointer;
}

.next-maintenance-info {
    background: rgba(var(--primary-rgb), 0.1);
    border: 1px solid rgba(var(--primary-rgb), 0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 25px 0;
}

.next-maintenance-info h4 {
    margin: 0 0 15px 0;
    color: var(--light);
    font-size: 1.1rem;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--light);
    margin-bottom: 8px;
}

.info-item:last-child {
    margin-bottom: 0;
}

.info-item i {
    color: var(--primary);
    font-size: 0.9rem;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 30px;
    padding-top: 25px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.btn-primary,
.btn-secondary {
    padding: 12px 30px;
    border-radius: 10px;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    display: flex;
    align-items: center;
    gap: 8px;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(var(--primary-rgb), 0.3);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--light);
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.15);
}

/* Адаптивность */
@media (max-width: 768px) {
    .maintenance-modal {
        max-height: 85vh;
    }
    
    .modal-header {
        padding: 20px;
    }
    
    .modal-form {
        padding: 20px;
    }
    
    .form-row {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .modal-actions {
        flex-direction: column;
    }
    
    .btn-primary,
    .btn-secondary {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .modal-overlay {
        padding: 10px;
    }
    
    .form-section h3 {
        font-size: 1.1rem;
    }
    
    .interval-input {
        flex-direction: column;
    }
    
    .interval-input select {
        min-width: auto;
    }
}
</style>