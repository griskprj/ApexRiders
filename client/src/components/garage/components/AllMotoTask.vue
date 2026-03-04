<template>
    <div class="tasks-card">
        <div class="card-header">
            <h2>
                <i class="fas fa-calendar-alt"></i> 
                {{ getHedaerTitle }} задачи ТО
            </h2>
            <div class="show-type">
                <BaseButton
                    :variant="showType === 'upcoming' ? 'primary' : 'outline'"
                    @click="changeShowType('upcoming')"
                >
                    <i class="fas fa-clock"></i>
                    Предстоящие
                </BaseButton>
                <BaseButton
                    :variant="showType === 'overdue' ? 'primary' : 'outline'"
                    @click="changeShowType('overdue')"
                >
                    <i class="fas fa-exclamation-triangle"></i>
                    Просроченные
                </BaseButton>
                <BaseButton
                    :variant="showType === 'all' ? 'primary' : 'outline'"
                    @click="changeShowType('all')"
                >
                    <i class="fas fa-list"></i>
                    Все
                </BaseButton>
            </div>
        </div>
        
        <div class="card-body">
            <div class="tasks-list">
                <div 
                    v-for="task in (getTypeTask())" 
                    :key="task.id" 
                    class="task-item"
                    :class="{ 
                        'overdue': task.status === 'overdue',
                        'high-priority': task.priority === 'high',
                        'medium-priority': task.priority === 'medium'
                    }"
                >
                    <!-- Индикатор приоритета -->
                    <div class="task-priority-indicator" :class="task.priority"></div>
                    
                    <div class="task-main">
                        <div class="task-header">
                            <div class="task-title-wrapper">
                                <h3 class="task-title">{{ task.title }}</h3>
                                <span class="task-badge" :class="task.priority">
                                    {{ getPriorityText(task.priority) }}
                                </span>
                            </div>
                            
                            <div class="task-actions">
                                <button 
                                    class="btn btn-icon btn-success" 
                                    @click="showCompleteModal(task)"
                                    title="Отметить выполненным"
                                >
                                    <i class="fas fa-check"></i>
                                </button>
                                <button 
                                    class="btn btn-icon btn-outline" 
                                    @click="openEditTaskModal(task)"
                                    title="Редактировать"
                                >
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button 
                                    class="btn btn-icon btn-outline" 
                                    @click="deleteTask(task)"
                                    title="Удалить"
                                >
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>

                        <div class="task-details-grid">
                            <div v-if="task.next_maintenance_date" class="detail-item">
                                <i class="fas fa-calendar-day detail-icon"></i>
                                <div class="detail-content">
                                    <span class="detail-label">Следующее ТО по дате</span>
                                    <span class="detail-value">
                                        {{ formatDateForDisplay(task.next_maintenance_date) }}
                                    </span>
                                </div>
                            </div>
                            
                            <div v-if="task.next_maintenance_mileage" class="detail-item">
                                <i class="fas fa-tachometer-alt detail-icon"></i>
                                <div class="detail-content">
                                    <span class="detail-label">Следующее ТО через</span>
                                    <span class="detail-value">
                                        {{ task.next_maintenance_mileage - motorcycle.current_mileage }} км
                                    </span>
                                </div>
                            </div>
                            
                            <div v-if="task.status === 'overdue' && task.next_maintenance_mileage" class="detail-item overdue">
                                <i class="fas fa-tachometer-alt detail-icon overdue"></i>
                                <div class="detail-content">
                                    <span class="detail-label">Просрочено по пробегу</span>
                                    <span class="detail-value">
                                        {{ Math.max(0, motorcycle.current_mileage - task.next_maintenance_mileage) }} км
                                    </span>
                                </div>
                            </div>
                            <div v-if="task.status === 'overdue' && task.next_maintenance_date" class="detail-item overdue">
                                <i class="fas fa-calendar detail-icon overdue"></i>
                                <div class="detail-content">
                                    <span class="detail-label">Просрочено по дате</span>
                                    <span class="detail-value"> 
                                        {{ getOverdueDays(task.next_maintenance_date) }} дней
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Дополнительная информация -->
                        <div v-if="task.motorcycle" class="motorcycle-info">
                            <i class="fas fa-motorcycle"></i>
                            <span>{{ task.motorcycle.brand }} {{ task.motorcycle.model }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Состояния пустого списка -->
            <div class="empty-state" v-if="showAllTasks && allTaskMaintenance.length === 0">
                <div class="empty-state-icon">
                    <i class="fas fa-wrench"></i>
                </div>
                <h3>Задач еще нет</h3>
                <p>Создайте первую задачу по техническому обслуживанию</p>
                <BaseButton variant="primary" @click="$emit('create-task')">
                    <i class="fas fa-plus"></i>
                    Создать задачу
                </BaseButton>
            </div>
            
            <div class="empty-state" v-else-if="showType === 'upcoming' && upcomingMaintenance.length === 0">
                <div class="empty-state-icon">
                    <i class="fas fa-check-circle" style="color: #4caf50;"></i>
                </div>
                <h3>Все задачи выполнены!</h3>
                <p>На данный момент нет предстоящих задач по обслуживанию</p>
            </div>
            
            <div class="empty-state" v-else-if="showType === 'overdue' && overdueTasks.length === 0">
                <div class="empty-state-icon">
                    <i class="fas fa-smile" style="color: #ff9800;"></i>
                </div>
                <h3>Просроченных задач нет</h3>
                <p>Вы вовремя проходите техническое обслуживание</p>
            </div>
        </div>
    </div>
</template>

<script>
import BaseButton from '../../ui/BaseButton.vue';

export default {
    name: 'AllMotoTask',

    components: {
        BaseButton
    },

    props: {
        allTaskMaintenance: {
            type: Array,
            default: () => []
        },
        upcomingMaintenance: {
            type: Array,
            default: () => []
        },
        overdueTasks: {
            type: Array,
            default: () => []
        },
        motorcycle: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            showType: 'upcoming'
        }
    },

    computed: {
        showAllTasks() {
            return this.showType === 'all';
        }
    },

    methods: {
        changeShowType(type) {
            this.showType = type;
            this.$emit('change-type', type);
        },

        getTypeTask() {
            if (this.showType === 'all') {
                return this.allTaskMaintenance;
            } else if (this.showType === 'upcoming') {
                return this.upcomingMaintenance;
            } else if (this.showType === 'overdue') {
                return this.overdueTasks;
            }
            return [];
        },

        getPriorityText(priority) {
            const priorities = {
                'low': 'Низкий',
                'medium': 'Средний',
                'high': 'Высокий'
            }
            return priorities[priority] || priority;
        },

        formatDateForDisplay(dateString) {
            if (!dateString) return 'Не указано';
            
            const date = new Date(dateString);
            if (isNaN(date.getTime())) return 'Не указано';
            
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        },

        showCompleteModal(task) {
            this.$emit('complete-task', task);
        },

        openEditTaskModal(task) {
            this.$emit('edit-task', task);
        },

        deleteTask(task) {
            if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
                this.$emit('delete-task', task);
            }
        },


        getOverdueDays(dateString) {
            if (!dateString) return 0;
            
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            const maintenanceDate = new Date(dateString);
            maintenanceDate.setHours(0, 0, 0, 0);
            
            // Если дата обслуживания еще не наступила
            if (maintenanceDate >= today) return 0;
            
            const diffTime = today - maintenanceDate;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            return diffDays;
        }
    }
}
</script>

<style scoped>
.tasks-card {
    background: rgba(20, 20, 30, 0.95);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.card-header {
    background: rgba(30, 30, 40, 0.9);
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.card-header h2 {
    margin: 0;
    font-size: 1.3em;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
}

.card-header h2 i {
    color: #00bcd4;
    font-size: 1.2em;
}

.show-type {
    display: flex;
    gap: 8px;
}

.show-type :deep(button) {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
}

.show-type :deep(button i) {
    font-size: 0.9em;
}

.card-body {
    padding: 24px;
}

.tasks-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.task-item {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 14px;
    padding: 20px;
    display: flex;
    gap: 20px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
}

.task-item:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(0, 188, 212, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.task-item.overdue {
    background: rgba(244, 67, 54, 0.05);
    border-left: 4px solid #f44336 !important;
}

.task-item.high-priority {
    border: 1px solid rgba(244, 67, 54, 0.3);
}

.task-item.medium-priority {
    border: 1px solid rgba(255, 152, 0, 0.3);
}

.task-priority-indicator {
    width: 4px;
    height: 100%;
    border-radius: 2px;
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
}

.task-priority-indicator.high {
    background: linear-gradient(180deg, #f44336, #d32f2f);
}

.task-priority-indicator.medium {
    background: linear-gradient(180deg, #ff9800, #f57c00);
}

.task-priority-indicator.low {
    background: linear-gradient(180deg, #4caf50, #388e3c);
}

.task-main {
    flex: 1;
    min-width: 0;
}

.task-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;
}

.task-title-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.task-title {
    margin: 0;
    font-size: 1.15em;
    font-weight: 600;
    color: #fff;
}

.task-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75em;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
}

.task-badge.high {
    background: rgba(244, 67, 54, 0.2);
    color: #ff8a80;
}

.task-badge.medium {
    background: rgba(255, 152, 0, 0.2);
    color: #ffb74d;
}

.task-badge.low {
    background: rgba(76, 175, 80, 0.2);
    color: #81c784;
}

.task-actions {
    display: flex;
    gap: 8px;
}

.btn-icon {
    width: 36px;
    height: 36px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1em;
}

.btn-icon.btn-success {
    background: linear-gradient(135deg, #4caf50, #388e3c);
    color: white;
}

.btn-icon.btn-success:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.btn-icon.btn-outline {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #fff;
}

.btn-icon.btn-outline:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}

.task-details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin-bottom: 16px;
}

.detail-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: rgba(0, 0, 0, 0.2);
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-item.overdue {
    background: rgba(244, 67, 54, 0.05);
    border-left: 4px solid #f44336;
}

.detail-icon {
    color: #00bcd4;
    font-size: 1.2em;
    width: 24px;
    text-align: center;
}

.detail-icon.overdue {
    color: rgb(244, 67, 54);
}

.detail-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.detail-label {
    font-size: 0.8em;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.detail-value {
    font-size: 1.1em;
    font-weight: 600;
    color: #fff;
}

.motorcycle-info {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 188, 212, 0.1);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9em;
    color: #00bcd4;
    border: 1px solid rgba(0, 188, 212, 0.2);
}

.motorcycle-info i {
    font-size: 0.9em;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 16px;
    border: 1px dashed rgba(255, 255, 255, 0.1);
}

.empty-state-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5em;
    color: rgba(255, 255, 255, 0.3);
}

.empty-state h3 {
    margin: 0 0 8px;
    font-size: 1.3em;
    color: #fff;
    font-weight: 500;
}

.empty-state p {
    margin: 0 0 24px;
    color: rgba(255, 255, 255, 0.5);
    font-size: 1em;
}

/* Адаптивность */
@media (max-width: 768px) {
    .card-header {
        flex-direction: column;
        align-items: stretch;
    }

    .show-type {
        flex-direction: column;
    }

    .task-header {
        flex-direction: column;
    }

    .task-actions {
        width: 100%;
        justify-content: flex-end;
    }

    .task-details-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .card-body {
        padding: 16px;
    }

    .task-item {
        padding: 16px;
    }

    .task-title-wrapper {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>