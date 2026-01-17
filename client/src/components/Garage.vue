<template>
    <div class="garage-page">
        <!-- Хедер с информацией о мотоцикле -->
        <div class="garage-header">
            <div class="header-content">
                <h1>{{ motorcycle.brand }} {{ motorcycle.model }}</h1>
                <div class="motorcycle-info">
                    <div class="info-item">
                        <span class="label">Год:</span>
                        <span class="value">{{ motorcycle.year || 'Не указан' }}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Объем:</span>
                        <span class="value">{{ motorcycle.engine_volume || 'Не указан' }}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Цвет:</span>
                        <span class="value">{{ motorcycle.color || 'Не указан' }}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Номер:</span>
                        <span class="value">{{ motorcycle.license_plate || 'Не указан' }}</span>
                    </div>
                </div>
            </div>
            <div class="header-actions">
                <div class="mileage-display">
                    <div class="mileage-info">
                        <span class="mileage-label">Пробег:</span>
                        <span class="mileage-value">{{ motorcycle.current_mileage || 0 }} км</span>
                    </div>
                    <button class="btn btn-small btn-outline" @click="showMileageModal = true">
                        <i class="fas fa-edit"></i> Изменить
                    </button>
                </div>
                <div class="action-buttons">
                    <button class="btn btn-primary" @click="showEditModal = true">
                        <i class="fas fa-edit"></i> Редактировать
                    </button>
                    <button class="btn btn-danger" @click="confirmDelete">
                        <i class="fas fa-trash"></i> Удалить
                    </button>
                </div>
            </div>
        </div>

        <!-- Основной контент -->
        <div class="garage-content">
            <!-- Карточка мотоцикла -->
            <div class="motorcycle-card">
                <div class="card-header">
                    <h2><i class="fas fa-info-circle"></i> Информация о мотоцикле</h2>
                </div>
                <div class="card-body">
                    <div class="info-grid">
                        <div class="info-row">
                            <span class="info-label">VIN:</span>
                            <span class="info-value">{{ motorcycle.vin || 'Не указан' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label"><i class="fas fa-shield-alt"></i> Страховка до:</span>
                            <span class="info-value" :class="{ 'text-warning': isInsuranceExpiring }">
                                {{ formatDate(motorcycle.insurance_expiry) }}
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="info-label"><i class="fas fa-file-alt"></i> Регистрация до:</span>
                            <span class="info-value" :class="{ 'text-warning': isRegistrationExpiring }">
                                {{ formatDate(motorcycle.registration_expiry) }}
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="info-label"><i class="fas fa-calendar-plus"></i> Добавлен:</span>
                            <span class="info-value">{{ formatDate(motorcycle.created_at) }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Статистика ТО -->
            <div class="stats-card">
                <div class="card-header">
                    <h2><i class="fas fa-chart-bar"></i> Статистика ТО</h2>
                </div>
                <div class="card-body">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-icon">
                                <i class="fas fa-tasks"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-value">{{ maintenanceStats.total_tasks || 0 }}</div>
                                <div class="stat-label">Всего задач</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon">
                                <i class="fas fa-check-circle"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-value">{{ maintenanceStats.completed || 0 }}</div>
                                <div class="stat-label">Выполнено</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-value">{{ maintenanceStats.pending || 0 }}</div>
                                <div class="stat-label">Ожидает</div>
                            </div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon">
                                <i class="fas fa-exclamation-triangle"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-value">{{ maintenanceStats.overdue || 0 }}</div>
                                <div class="stat-label">Просрочено</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Ближайшие задачи ТО -->
            <div class="tasks-card" v-if="upcomingMaintenance.length > 0">
                <div class="card-header">
                    <h2><i class="fas fa-calendar-alt"></i> Ближайшие задачи ТО</h2>
                </div>
                <div class="card-body">
                    <div class="tasks-list">
                        <div v-for="task in upcomingMaintenance.slice(0, 3)" :key="task.id" class="task-item">
                            <div class="task-icon">
                                <i class="fas fa-tools"></i>
                            </div>
                            <div class="task-content">
                                <div class="task-title">{{ task.title }}</div>
                                <div class="task-details">
                                    <span v-if="task.next_maintenance_date" class="task-date">
                                        <i class="far fa-calendar"></i> {{ formatDate(task.next_maintenance_date) }}
                                    </span>
                                    <span v-if="task.next_maintenance_mileage" class="task-mileage">
                                        <i class="fas fa-tachometer-alt"></i> {{ task.next_maintenance_mileage }} км
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Последние заметки -->
            <div class="notes-card" v-if="recentNotes.length > 0">
                <div class="card-header">
                    <h2><i class="fas fa-sticky-note"></i> Последние заметки</h2>
                </div>
                <div class="card-body">
                    <div class="notes-list">
                        <div v-for="note in recentNotes.slice(0, 3)" :key="note.id" class="note-item">
                            <div class="note-header">
                                <div class="note-title">
                                    <i class="fas fa-file-alt"></i> {{ note.title }}
                                </div>
                                <div class="note-date">
                                    <i class="far fa-clock"></i> {{ formatDate(note.updated_at) }}
                                </div>
                            </div>
                            <div class="note-content">{{ note.content.substring(0, 100) }}...</div>
                            <div class="note-tags" v-if="note.tags && note.tags.length > 0">
                                <span v-for="tag in note.tags.slice(0, 2)" :key="tag" class="tag">
                                    #{{ tag }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Модальное окно изменения пробега -->
        <div v-if="showMileageModal" class="modal-overlay">
            <div class="modal">
                <div class="modal-header">
                    <h3><i class="fas fa-tachometer-alt"></i> Изменение пробега</h3>
                    <button class="close-btn" @click="showMileageModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>Текущий пробег: {{ motorcycle.current_mileage || 0 }} км</label>
                        <div class="input-with-icon">
                            <i class="fas fa-road"></i>
                            <input 
                                type="number" 
                                v-model="newMileage" 
                                placeholder="Новый пробег в км" 
                                class="form-input"
                                min="0"
                            >
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="showMileageModal = false">Отмена</button>
                    <button class="btn btn-primary" @click="updateMileage" :disabled="!newMileage">
                        <i class="fas fa-save"></i> Сохранить
                    </button>
                </div>
            </div>
        </div>

        <!-- Модальное окно редактирования мотоцикла -->
        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal">
                <div class="modal-header">
                    <h3><i class="fas fa-motorcycle"></i> Редактирование мотоцикла</h3>
                    <button class="close-btn" @click="showEditModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-row">
                        <div class="form-group">
                            <label><i class="fas fa-tag"></i> Марка</label>
                            <div class="input-with-icon">
                                <i class="fas fa-tag"></i>
                                <input v-model="editForm.brand" class="form-input" placeholder="Например, Honda">
                            </div>
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-tag"></i> Модель</label>
                            <div class="input-with-icon">
                                <i class="fas fa-tag"></i>
                                <input v-model="editForm.model" class="form-input" placeholder="Например, CB500F">
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label><i class="fas fa-calendar"></i> Год выпуска</label>
                            <div class="input-with-icon">
                                <i class="fas fa-calendar"></i>
                                <input v-model="editForm.year" type="number" class="form-input" placeholder="2020">
                            </div>
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-motorcycle"></i> Объем двигателя (см³)</label>
                            <div class="input-with-icon">
                                <i class="fas fa-motorcycle"></i>
                                <input v-model="editForm.engine_volume" type="number" class="form-input" placeholder="500">
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label><i class="fas fa-palette"></i> Цвет</label>
                            <div class="input-with-icon">
                                <i class="fas fa-palette"></i>
                                <input v-model="editForm.color" class="form-input" placeholder="Черный">
                            </div>
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-hashtag"></i> Номерной знак</label>
                            <div class="input-with-icon">
                                <i class="fas fa-hashtag"></i>
                                <input v-model="editForm.license_plate" class="form-input" placeholder="А123БВ77">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="showEditModal = false">Отмена</button>
                    <button class="btn btn-primary" @click="updateMotorcycle">
                        <i class="fas fa-save"></i> Сохранить
                    </button>
                </div>
            </div>
        </div>

        <!-- Индикатор загрузки -->
        <div v-if="isLoading" class="loading-overlay">
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <p>Загрузка данных мотоцикла...</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'GaragePage',
    
    data() {
        return {
            isLoading: true,
            motorcycle: {
                id: null,
                brand: '',
                model: '',
                year: '',
                engine_volume: '',
                color: '',
                license_plate: '',
                current_mileage: 0,
                vin: '',
                insurance_expiry: null,
                registration_expiry: null,
                created_at: null
            },
            maintenanceStats: {},
            upcomingMaintenance: [],
            recentNotes: [],
            
            // Модальные окна
            showMileageModal: false,
            showEditModal: false,
            
            // Формы
            newMileage: null,
            editForm: {
                brand: '',
                model: '',
                year: '',
                engine_volume: '',
                color: '',
                license_plate: ''
            }
        }
    },
    
    computed: {
        isInsuranceExpiring() {
            if (!this.motorcycle.insurance_expiry) return false
            const expiryDate = new Date(this.motorcycle.insurance_expiry)
            const today = new Date()
            const daysUntil = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
            return daysUntil <= 30 && daysUntil > 0
        },
        
        isRegistrationExpiring() {
            if (!this.motorcycle.registration_expiry) return false
            const expiryDate = new Date(this.motorcycle.registration_expiry)
            const today = new Date()
            const daysUntil = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
            return daysUntil <= 30 && daysUntil > 0
        }
    },
    
    mounted() {
        this.fetchMotorcycleData()
    },
    
    methods: {
        // Получить данные мотоцикла
        async fetchMotorcycleData() {
            try {
                this.isLoading = true
                const token = localStorage.getItem('authToken')
                if (!token) {
                    this.$router.push('/login')
                    return
                }
                
                const motoId = this.$route.params.id
                const response = await axios.get(`/api/garage/motorcycle/${motoId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                const data = response.data
                this.motorcycle = data.motorcycle
                this.maintenanceStats = data.stats || {}
                this.upcomingMaintenance = data.upcoming_maintenance || []
                this.recentNotes = data.recent_notes || []
                
                // Заполняем форму редактирования
                this.editForm = {
                    brand: this.motorcycle.brand,
                    model: this.motorcycle.model,
                    year: this.motorcycle.year,
                    engine_volume: this.motorcycle.engine_volume,
                    color: this.motorcycle.color,
                    license_plate: this.motorcycle.license_plate
                }
                
            } catch (error) {
                console.error('Ошибка загрузки данных:', error)
                if (error.response && error.response.status === 404) {
                    this.$router.push('/garage')
                }
            } finally {
                this.isLoading = false
            }
        },
        
        // Обновить пробег
        async updateMileage() {
            try {
                const token = localStorage.getItem('authToken')
                await axios.put(
                    `/api/motorcycle/${this.motorcycle.id}/mileage`,
                    { mileage: this.newMileage },
                    { headers: { 'Authorization': `Bearer ${token}` } }
                )
                
                this.motorcycle.current_mileage = this.newMileage
                this.newMileage = null
                this.showMileageModal = false
                
                // Обновляем данные
                await this.fetchMotorcycleData()
                
            } catch (error) {
                console.error('Ошибка обновления пробега:', error)
                alert('Ошибка при обновлении пробега')
            }
        },
        
        // Обновить данные мотоцикла
        async updateMotorcycle() {
            try {
                const token = localStorage.getItem('authToken')
                await axios.put(
                    `/api/motorcycle/${this.motorcycle.id}`,
                    this.editForm,
                    { headers: { 'Authorization': `Bearer ${token}` } }
                )
                
                // Обновляем локальные данные
                Object.assign(this.motorcycle, this.editForm)
                this.showEditModal = false
                
            } catch (error) {
                console.error('Ошибка обновления мотоцикла:', error)
                alert('Ошибка при обновлении данных')
            }
        },
        
        // Подтверждение удаления
        confirmDelete() {
            if (confirm('Вы уверены, что хотите удалить этот мотоцикл? Это действие нельзя отменить.')) {
                this.deleteMotorcycle()
            }
        },
        
        // Удалить мотоцикл
        async deleteMotorcycle() {
            try {
                const token = localStorage.getItem('authToken')
                await axios.delete(`/api/motorcycle/${this.motorcycle.id}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                
                this.$router.push('/garage')
                
            } catch (error) {
                console.error('Ошибка удаления мотоцикла:', error)
                alert('Ошибка при удалении мотоцикла')
            }
        },
        
        // Форматирование даты
        formatDate(dateString) {
            if (!dateString) return 'Не указано'
            
            const date = new Date(dateString)
            if (isNaN(date.getTime())) return 'Неверная дата'
            
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
        }
    }
}
</script>

<style scoped>
.garage-page {
    padding: 120px 5% 60px;
    min-height: calc(100vh - 80px);
    position: relative;
}

/* Декоративные элементы */
.garage-page::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 10% 20%, rgba(255, 69, 0, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(0, 191, 255, 0.08) 0%, transparent 40%);
    z-index: -1;
}

/* Хедер */
.garage-header {
    background: rgba(10, 10, 15, 0.7);
    backdrop-filter: blur(20px);
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.garage-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

.header-content h1 {
    margin: 0 0 20px 0;
    font-size: 2.2em;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.motorcycle-info {
    display: flex;
    gap: 30px;
    flex-wrap: wrap;
}

.info-item {
    display: flex;
    flex-direction: column;
}

.info-item .label {
    font-size: 0.9em;
    color: var(--text-secondary);
    margin-bottom: 5px;
}

.info-item .value {
    font-size: 1.1em;
    font-weight: 600;
    color: var(--text);
}

.header-actions {
    margin-top: 20px;
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.mileage-display {
    display: flex;
    align-items: center;
    gap: 15px;
    background: rgba(255, 255, 255, 0.05);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    flex-grow: 1;
    min-width: 200px;
}

.mileage-info {
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex-grow: 1;
}

.mileage-label {
    font-size: 0.9em;
    color: var(--text-secondary);
}

.mileage-value {
    font-size: 1.5em;
    font-weight: 700;
    color: var(--accent);
    text-shadow: 0 0 10px rgba(0, 191, 255, 0.3);
}

.action-buttons {
    display: flex;
    gap: 10px;
}

/* Основной контент */
.garage-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    margin-top: 20px;
}

/* Карточки */
.motorcycle-card,
.stats-card,
.tasks-card,
.notes-card {
    background: rgba(10, 10, 15, 0.7);
    backdrop-filter: blur(20px);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    position: relative;
}

.motorcycle-card:hover,
.stats-card:hover,
.tasks-card:hover,
.notes-card:hover {
    border-color: var(--primary);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(255, 69, 0, 0.2);
}

.card-header {
    background: rgba(20, 20, 30, 0.8);
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header h2 {
    margin: 0;
    font-size: 1.2em;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-header i {
    color: var(--primary);
}

.card-body {
    padding: 20px;
}

/* Информационная сетка */
.info-grid {
    display: grid;
    gap: 15px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    font-weight: 500;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 8px;
}

.info-value {
    color: var(--text);
    font-weight: 500;
}

.text-warning {
    color: var(--warning);
    font-weight: 600;
}

/* Статистика */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.stat-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.stat-item:hover {
    background: rgba(var(--primary-rgb), 0.1);
    border-color: var(--primary);
    transform: translateY(-2px);
}

.stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2em;
    color: white;
}

.stat-content {
    display: flex;
    flex-direction: column;
}

.stat-value {
    font-size: 1.8em;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}

.stat-label {
    font-size: 0.85em;
    color: var(--text-secondary);
    margin-top: 5px;
}

/* Списки задач и заметок */
.tasks-list,
.notes-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.task-item,
.note-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 15px;
    display: flex;
    align-items: flex-start;
    gap: 15px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.task-item:hover,
.note-item:hover {
    background: rgba(var(--primary-rgb), 0.1);
    border-color: var(--primary);
    transform: translateX(5px);
}

.task-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--accent) 0%, rgba(0, 191, 255, 0.7) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.task-content {
    flex-grow: 1;
}

.task-title {
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
}

.task-details {
    display: flex;
    gap: 15px;
    font-size: 0.9em;
    color: var(--text-secondary);
}

.task-date,
.task-mileage {
    display: flex;
    align-items: center;
    gap: 5px;
}

/* Заметки */
.note-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
}

.note-title {
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
}

.note-date {
    font-size: 0.85em;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 5px;
}

.note-content {
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 10px;
}

.note-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.tag {
    background: rgba(var(--primary-rgb), 0.1);
    color: var(--primary);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85em;
    border: 1px solid var(--primary);
}

/* Модальные окна */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal {
    background: rgba(10, 10, 15, 0.95);
    border-radius: 15px;
    max-width: 500px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    margin: 0;
    color: var(--text);
    font-size: 1.3em;
    display: flex;
    align-items: center;
    gap: 10px;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.8em;
    cursor: pointer;
    color: var(--text-secondary);
    padding: 0;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.modal-body {
    padding: 25px;
}

.modal-footer {
    padding: 20px 25px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

/* Формы */
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
    }
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
}

.input-with-icon {
    position: relative;
}

.input-with-icon i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
}

.form-input {
    width: 100%;
    padding: 14px 15px 14px 45px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: var(--text);
    font-size: 1em;
    transition: all 0.3s ease;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.2);
}

/* Кнопки */
.btn {
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-size: 0.95em;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}

.btn:active {
    transform: translateY(0);
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border: 1px solid var(--primary);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #ff5500 0%, var(--primary) 100%);
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.5);
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.2);
}

.btn-danger {
    background: linear-gradient(135deg, var(--danger) 0%, var(--very-danger) 100%);
    color: white;
    border: 1px solid var(--danger);
}

.btn-danger:hover {
    background: linear-gradient(135deg, #ff5e6d 0%, var(--danger) 100%);
    box-shadow: 0 0 20px rgba(255, 71, 87, 0.5);
}

.btn-outline {
    background: transparent;
    border: 1px solid var(--primary);
    color: var(--text);
}

.btn-outline:hover {
    background: var(--primary-light);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
}

.btn-small {
    padding: 8px 16px;
    font-size: 0.85em;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

/* Индикатор загрузки */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1001;
}

.loading-content {
    text-align: center;
}

.loading-content p {
    margin-top: 20px;
    color: var(--text);
    font-size: 1.1em;
}

.loading-spinner {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-top: 4px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 768px) {
    .garage-page {
        padding: 100px 4% 40px;
    }
    
    .garage-header {
        padding: 20px;
    }
    
    .header-content h1 {
        font-size: 1.8em;
    }
    
    .motorcycle-info {
        gap: 20px;
    }
    
    .header-actions {
        flex-direction: column;
        gap: 15px;
    }
    
    .mileage-display,
    .action-buttons {
        width: 100%;
    }
    
    .action-buttons {
        flex-direction: column;
    }
    
    .garage-content {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>