<template>
    <div class="maintenance-planner">
        <div class="planner-header">
            <h3>Планировщик ТО</h3>
            <button class="btn-add" @click="$emit('add-task')">
                <i class="fas fa-plus"></i> Добавить задачу
            </button>
        </div>
        
        <!-- Ближайшие задачи -->
        <div v-if="upcomingTasks.length > 0" class="upcoming-section">
            <h4>Ближайшие задачи</h4>
            <div class="upcoming-tasks">
                <div 
                    v-for="task in upcomingTasks" 
                    :key="task.id" 
                    class="task-card"
                    :class="{
                        'overdue': isTaskOverdue(task),
                        'priority-high': task.priority === 'high',
                        'priority-medium': task.priority === 'medium',
                        'priority-low': task.priority === 'low'
                    }"
                    @click="$emit('task-click', task)"
                >
                    <div class="task-header">
                        <span class="task-title">{{ task.title }}</span>
                        <span class="task-badge" :class="getPriorityClass(task)">
                            {{ getPriorityLabel(task) }}
                        </span>
                    </div>
                    
                    <div class="task-details">
                        <div class="task-info">
                            <i class="fas fa-calendar"></i>
                            <span v-if="task.next_maintenance_date">
                                {{ formatDate(task.next_maintenance_date) }}
                            </span>
                            <span v-else-if="task.next_maintenance_mileage">
                                При {{ formatMileage(task.next_maintenance_mileage) }} км
                            </span>
                        </div>
                        
                        <div class="task-info">
                            <i class="fas fa-clock"></i>
                            <span>{{ getTimeRemaining(task) }}</span>
                        </div>
                    </div>
                    
                    <div class="task-actions">
                        <button 
                            class="btn-complete" 
                            @click.stop="$emit('complete-task', task.id)"
                        >
                            Завершить
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Все задачи -->
        <div class="all-tasks-section">
            <div class="section-header">
                <h4>Все задачи ТО</h4>
                <div class="task-filters">
                    <span 
                        class="filter-btn"
                        :class="{ active: activeFilter === 'all' }"
                        @click="activeFilter = 'all'"
                    >
                        Все
                    </span>
                    <span 
                        class="filter-btn"
                        :class="{ active: activeFilter === 'pending' }"
                        @click="activeFilter = 'pending'"
                    >
                        Ожидают
                    </span>
                    <span 
                        class="filter-btn"
                        :class="{ active: activeFilter === 'completed' }"
                        @click="activeFilter = 'completed'"
                    >
                        Завершены
                    </span>
                </div>
            </div>
            
            <div class="tasks-table">
                <div class="table-header">
                    <div class="table-cell">Задача</div>
                    <div class="table-cell">Тип</div>
                    <div class="table-cell">Следующее</div>
                    <div class="table-cell">Приоритет</div>
                    <div class="table-cell">Статус</div>
                </div>
                
                <div class="table-body">
                    <div 
                        v-for="task in filteredTasks" 
                        :key="task.id" 
                        class="table-row"
                        :class="{
                            'completed': task.status === 'completed',
                            'overdue': isTaskOverdue(task) && task.status === 'pending'
                        }"
                        @click="$emit('task-click', task)"
                    >
                        <div class="table-cell">
                            <div class="task-cell">
                                <div class="task-icon">
                                    {{ getTaskIcon(task.maintenance_type) }}
                                </div>
                                <div class="task-content">
                                    <strong>{{ task.title }}</strong>
                                    <small v-if="task.description">{{ task.description }}</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="table-cell">
                            <span class="type-badge" :class="getTypeClass(task)">
                                {{ getTypeLabel(task) }}
                            </span>
                        </div>
                        
                        <div class="table-cell">
                            <div v-if="task.next_maintenance_date" class="date-cell">
                                <i class="fas fa-calendar"></i>
                                {{ formatDate(task.next_maintenance_date) }}
                            </div>
                            <div v-else-if="task.next_maintenance_mileage" class="mileage-cell">
                                <i class="fas fa-edit"></i>
                                {{ formatMileage(task.next_maintenance_mileage) }} км
                            </div>
                            <div v-else class="no-schedule">
                                <i class="fas fa-question"></i>
                                Не указано
                            </div>
                        </div>
                        
                        <div class="table-cell">
                            <span class="priority-badge" :class="getPriorityClass(task)">
                                {{ getPriorityLabel(task) }}
                            </span>
                        </div>
                        
                        <div class="table-cell">
                            <span class="status-badge" :class="getStatusClass(task)">
                                {{ getStatusLabel(task) }}
                            </span>
                        </div>
                    </div>
                    
                    <div v-if="filteredTasks.length === 0" class="empty-state">
                        <i class="fas fa-tasks empty-icon"></i>
                        <p>Задачи не найдены</p>
                    </div>
                </div>
            </div>
            
            <!-- Статистика -->
            <div class="tasks-stats">
                <div class="stat-item">
                    <div class="stat-value">{{ pendingTasksCount }}</div>
                    <div class="stat-label">Ожидают</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ overdueTasksCount }}</div>
                    <div class="stat-label">Просрочено</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ completedTasksCount }}</div>
                    <div class="stat-label">Завершено</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ totalTasksCount }}</div>
                    <div class="stat-label">Всего</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
    name: 'MaintenancePlanner',
    
    props: {
        tasks: {
            type: Array,
            default: () => []
        },
        upcomingTasks: {
            type: Array,
            default: () => []
        }
    },
    
    emits: ['task-click', 'add-task', 'complete-task'],
    
    setup(props) {
        const activeFilter = ref('all')
        
        // Вычисляемые свойства
        const filteredTasks = computed(() => {
            switch (activeFilter.value) {
                case 'pending':
                    return props.tasks.filter(task => task.status === 'pending')
                case 'completed':
                    return props.tasks.filter(task => task.status === 'completed')
                default:
                    return props.tasks
            }
        })
        
        const pendingTasksCount = computed(() => {
            return props.tasks.filter(task => task.status === 'pending').length
        })
        
        const overdueTasksCount = computed(() => {
            return props.tasks.filter(task => 
                task.status === 'pending' && isTaskOverdue(task)
            ).length
        })
        
        const completedTasksCount = computed(() => {
            return props.tasks.filter(task => task.status === 'completed').length
        })
        
        const totalTasksCount = computed(() => {
            return props.tasks.length
        })
        
        // Методы
        const isTaskOverdue = (task) => {
            if (task.status === 'completed') return false
            
            const today = new Date()
            if (task.next_maintenance_date) {
                const taskDate = new Date(task.next_maintenance_date)
                return taskDate < today
            }
            
            return false
        }
        
        const getTimeRemaining = (task) => {
            if (!task.next_maintenance_date || task.status === 'completed') {
                return '—'
            }
            
            const today = new Date()
            const taskDate = new Date(task.next_maintenance_date)
            const diffTime = taskDate - today
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
            
            if (diffDays < 0) {
                return `Просрочено на ${Math.abs(diffDays)} дн.`
            } else if (diffDays === 0) {
                return 'Сегодня'
            } else if (diffDays === 1) {
                return 'Завтра'
            } else if (diffDays < 7) {
                return `Через ${diffDays} дн.`
            } else if (diffDays < 30) {
                return `Через ${Math.floor(diffDays / 7)} нед.`
            } else {
                return `Через ${Math.floor(diffDays / 30)} мес.`
            }
        }
        
        const formatDate = (dateString) => {
            const date = new Date(dateString)
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            })
        }
        
        const formatMileage = (mileage) => {
            return mileage.toLocaleString('ru-RU')
        }
        
        const getPriorityClass = (task) => {
            return `priority-${task.priority || 'medium'}`
        }
        
        const getPriorityLabel = (task) => {
            const priorityMap = {
                high: 'Высокий',
                medium: 'Средний',
                low: 'Низкий'
            }
            return priorityMap[task.priority || 'medium']
        }
        
        const getTypeClass = (task) => {
            return `type-${task.maintenance_type || 'regular'}`
        }
        
        const getTypeLabel = (task) => {
            const typeMap = {
                regular: 'Регулярное',
                repair: 'Ремонт',
                inspection: 'Осмотр',
                replacement: 'Замена',
                custom: 'Пользовательское'
            }
            return typeMap[task.maintenance_type || 'regular']
        }
        
        const getStatusClass = (task) => {
            if (task.status === 'completed') return 'status-completed'
            if (isTaskOverdue(task)) return 'status-overdue'
            return 'status-pending'
        }
        
        const getStatusLabel = (task) => {
            if (task.status === 'completed') return 'Завершено'
            if (isTaskOverdue(task)) return 'Просрочено'
            return 'Ожидает'
        }
        
        const getTaskIcon = (type) => {
            const iconMap = {
                regular: '🔧',
                repair: '🛠️',
                inspection: '🔍',
                replacement: '🔄',
                custom: '📝'
            }
            return iconMap[type] || '📋'
        }
        
        return {
            activeFilter,
            filteredTasks,
            pendingTasksCount,
            overdueTasksCount,
            completedTasksCount,
            totalTasksCount,
            isTaskOverdue,
            getTimeRemaining,
            formatDate,
            formatMileage,
            getPriorityClass,
            getPriorityLabel,
            getTypeClass,
            getTypeLabel,
            getStatusClass,
            getStatusLabel,
            getTaskIcon
        }
    }
}
</script>

<style scoped>
.maintenance-planner {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    grid-column: 1 / -1;
    margin-bottom: 25px;
}

.planner-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.planner-header h3 {
    font-size: 1.5rem;
    color: var(--text-primary);
    margin: 0;
}

.btn-add {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 0.95rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
}

.btn-add:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(var(--primary-rgb), 0.3);
}

.btn-add .icon {
    font-size: 1.2rem;
    font-weight: bold;
}

/* Ближайшие задачи */
.upcoming-section h4 {
    font-size: 1.2rem;
    color: var(--text-primary);
    margin-bottom: 15px;
}

.upcoming-tasks {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}

.task-card {
    background: #ffffff33;
    border-radius: 12px;
    padding: 20px;
    border-left: 4px solid var(--primary);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    cursor: pointer;
    transition: all 0.3s ease;
}

.task-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.task-card.overdue {
    border-left-color: var(--danger);
}

.task-card.priority-high {
    border-left-color: var(--danger);
}

.task-card.priority-medium {
    border-left-color: var(--warning);
}

.task-card.priority-low {
    border-left-color: var(--success);
}

.task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.task-title {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 1.1rem;
}

.task-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.task-badge.priority-high {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
}

.task-badge.priority-medium {
    background: rgba(var(--warning-rgb), 0.1);
    color: var(--warning);
}

.task-badge.priority-low {
    background: rgba(var(--success-rgb), 0.1);
    color: var(--success);
}

.task-details {
    display: flex;
    gap: 20px;
    margin-bottom: 15px;
}

.task-info {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.task-info .icon {
    font-size: 1rem;
}

.task-actions {
    display: flex;
    justify-content: flex-end;
}

.btn-complete {
    background: linear-gradient(135deg, var(--success) 0%, var(--success-dark) 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-complete:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* Все задачи */
.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-header h4 {
    font-size: 1.2rem;
    color: var(--text-primary);
    margin: 0;
}

.task-filters {
    display: flex;
    gap: 10px;
}

.filter-btn {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    background: var(--bg-secondary);
    color: var(--text-secondary);
}

.filter-btn:hover,
.filter-btn.active {
    background: var(--primary);
    color: white;
}

/* Таблица задач */
.tasks-table {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.table-header {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
    padding: 15px 20px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.9rem;
}

.table-body {
    max-height: 400px;
    overflow-y: auto;
}

.table-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-color);
    cursor: pointer;
    transition: all 0.3s ease;
}

.table-row:hover {
    background: var(--bg-hover);
}

.table-row.completed {
    opacity: 0.7;
    background: var(--bg-secondary);
}

.table-row.overdue {
    background: rgba(var(--danger-rgb), 0.05);
}

.table-row.overdue:hover {
    background: rgba(var(--danger-rgb), 0.1);
}

.table-cell {
    display: flex;
    align-items: center;
}

.task-cell {
    display: flex;
    align-items: center;
    gap: 12px;
}

.task-icon {
    font-size: 1.2rem;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-secondary);
    border-radius: 10px;
}

.task-content {
    display: flex;
    flex-direction: column;
}

.task-content strong {
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.task-content small {
    color: var(--text-secondary);
    font-size: 0.85rem;
    opacity: 0.8;
}

/* Бейджи */
.type-badge,
.priority-badge,
.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.type-badge {
    background: rgba(var(--primary-rgb), 0.1);
    color: var(--primary);
}

.type-badge.type-repair {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
}

.type-badge.type-inspection {
    background: rgba(var(--info-rgb), 0.1);
    color: var(--info);
}

.type-badge.type-replacement {
    background: rgba(var(--warning-rgb), 0.1);
    color: var(--warning);
}

.type-badge.type-custom {
    background: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
}

.priority-badge.priority-high {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
}

.priority-badge.priority-medium {
    background: rgba(var(--warning-rgb), 0.1);
    color: var(--warning);
}

.priority-badge.priority-low {
    background: rgba(var(--success-rgb), 0.1);
    color: var(--success);
}

.status-badge.status-pending {
    background: rgba(var(--warning-rgb), 0.1);
    color: var(--warning);
}

.status-badge.status-overdue {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
}

.status-badge.status-completed {
    background: rgba(var(--success-rgb), 0.1);
    color: var(--success);
}

/* Ячейки даты и пробега */
.date-cell,
.mileage-cell,
.no-schedule {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.9rem;
}

.date-cell .icon {
    color: var(--primary);
}

.mileage-cell .icon {
    color: var(--info);
}

.no-schedule {
    color: var(--text-tertiary);
    font-style: italic;
}

/* Пустое состояние */
.empty-state {
    padding: 40px 20px;
    text-align: center;
    color: var(--text-secondary);
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 10px;
    opacity: 0.5;
}

.empty-state p {
    margin: 0;
    font-size: 1rem;
}

/* Статистика */
.tasks-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
}

.stat-item {
    text-align: center;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.stat-value {
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

/* Адаптивность */
@media (max-width: 1200px) {
    .upcoming-tasks {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
    
    .tasks-table {
        overflow-x: auto;
    }
    
    .table-header,
    .table-row {
        min-width: 800px;
    }
}

@media (max-width: 768px) {
    .maintenance-planner {
        padding: 20px;
    }
    
    .planner-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .upcoming-tasks {
        grid-template-columns: 1fr;
    }
    
    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .task-filters {
        width: 100%;
        justify-content: space-between;
    }
    
    .tasks-stats {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .tasks-stats {
        grid-template-columns: 1fr;
    }
}
</style>