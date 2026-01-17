<template>
    <div class="maintenance-stats">
        <!-- Заголовок с обновлением статистики -->
        <div class="stats-header">
            <h3>Статистика ТО</h3>
            <button 
                class="btn-refresh" 
                @click="$emit('refresh')"
                :disabled="isLoading"
                :title="lastUpdated ? `Обновлено: ${formatTime(lastUpdated)}` : 'Обновить'"
            >
                <i class="fas fa-refresh refresh-icon" :class="{ spinning: isLoading }"></i>
                {{ isLoading ? 'Обновление...' : 'Обновить' }}
            </button>
        </div>
        
        <!-- Основные метрики -->
        <div class="stats-grid">
            <div class="stat-card" :class="{ highlight: stats.overdue > 0 }">
                <div class="stat-icon overdue">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-value">{{ stats.overdue || 0 }}</div>
                    <div class="stat-label">Просрочено</div>
                    <div v-if="stats.overdue > 0" class="stat-warning">
                        Требуется срочное внимание
                    </div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon pending">
                    <i class="fas fa-hourglass"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-value">{{ stats.pending || 0 }}</div>
                    <div class="stat-label">Ожидают</div>
                    <div v-if="stats.next_due_date" class="stat-hint">
                        Следующее: {{ formatDate(stats.next_due_date) }}
                    </div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon completed">
                    <i class="fas fa-check"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-value">{{ stats.completed || 0 }}</div>
                    <div class="stat-label">Завершено</div>
                    <div v-if="stats.completion_rate > 0" class="stat-progress">
                        <div class="progress-bar">
                            <div 
                                class="progress-fill" 
                                :style="{ width: `${stats.completion_rate}%` }"
                            ></div>
                        </div>
                        <span class="progress-text">{{ stats.completion_rate }}%</span>
                    </div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon total">
                    <i class="fas fa-bar-chart"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-value">{{ stats.total_tasks || 0 }}</div>
                    <div class="stat-label">Всего задач</div>
                    <div class="stat-distribution">
                        <div class="dist-item">
                            <span class="dist-dot overdue-dot"></span>
                            <span class="dist-text">Просрочено: {{ stats.overdue || 0 }}</span>
                        </div>
                        <div class="dist-item">
                            <span class="dist-dot pending-dot"></span>
                            <span class="dist-text">Ожидают: {{ stats.pending || 0 }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Дополнительная информация -->
        <div class="stats-details">
            <div class="details-section">
                <h4>Общая информация</h4>
                <div class="details-grid">
                    <div class="detail-item">
                        <span class="detail-label">Средняя стоимость:</span>
                        <span class="detail-value">
                            {{ formatCurrency(stats.average_cost) }}
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Общие затраты:</span>
                        <span class="detail-value">
                            {{ formatCurrency(stats.total_cost) }}
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Последнее ТО:</span>
                        <span class="detail-value">
                            {{ stats.last_maintenance ? formatDate(stats.last_maintenance) : '—' }}
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Следующее ТО:</span>
                        <span class="detail-value">
                            {{ stats.next_maintenance ? formatDate(stats.next_maintenance) : '—' }}
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Мини-график активности -->
            <div class="details-section">
                <h4>Активность (30 дней)</h4>
                <div class="activity-chart">
                    <div 
                        v-for="(day, index) in activityData" 
                        :key="index" 
                        class="activity-bar"
                        :style="{ height: `${getActivityHeight(day.count)}%` }"
                        :class="{ active: day.count > 0 }"
                        :title="`${day.date}: ${day.count} задач`"
                    >
                        <div class="bar-tooltip">
                            {{ day.date }}: {{ day.count }}
                        </div>
                    </div>
                </div>
                <div class="activity-legend">
                    <div class="legend-item">
                        <span class="legend-dot completed-dot"></span>
                        <span>Завершенные задачи</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Быстрые действия для просроченных задач -->
        <div v-if="stats.overdue > 0" class="urgent-actions">
            <div class="urgent-header">
                <i class="fas fa-exclamation urgent-icon"></i>
                <h4>Требуется внимание!</h4>
            </div>
            <p class="urgent-message">
                У вас {{ stats.overdue }} просроченных задач ТО.
                Рекомендуем выполнить их как можно скорее.
            </p>
            <div class="action-buttons">
                <button class="btn-action primary" @click="$emit('view-overdue')">
                    Показать просроченные
                </button>
                <button class="btn-action secondary" @click="$emit('schedule-all')">
                    Запланировать все
                </button>
            </div>
        </div>
        
        <!-- Подсказки и рекомендации -->
        <div v-else class="tips-section">
            <div class="tips-header">
                <i class="fas fa-lightbulb tips-icon"></i>
                <h4>Подсказки</h4>
            </div>
            <div class="tips-list">
                <div class="tip-item">
                    <i class="fas fa-calendar tip-icon"></i>
                    <div class="tip-content">
                        <strong>Планируйте заранее</strong>
                        <p>Создавайте задачи ТО за 2-3 недели до срока</p>
                    </div>
                </div>
                <div class="tip-item">
                    <i class="fas fa-credit-card tip-icon"></i>
                    <div class="tip-content">
                        <strong>Бюджет</strong>
                        <p>Учитывайте стоимость запчастей при планировании</p>
                    </div>
                </div>
                <div class="tip-item">
                    <i class="fas fa-wrench tip-icon"></i>
                    <div class="tip-content">
                        <strong>Регулярность</strong>
                        <p>Регулярное ТО продлевает срок службы мотоцикла</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
    name: 'MaintenanceStats',
    
    props: {
        stats: {
            type: Object,
            default: () => ({
                total_tasks: 0,
                completed: 0,
                pending: 0,
                overdue: 0,
                completion_rate: 0,
                average_cost: 0,
                total_cost: 0,
                last_maintenance: null,
                next_maintenance: null,
                next_due_date: null
            })
        },
        isLoading: {
            type: Boolean,
            default: false
        }
    },
    
    emits: ['refresh', 'view-overdue', 'schedule-all'],
    
    setup(props) {
        const lastUpdated = ref(new Date())
        
        // Генерация тестовых данных для графика активности
        const activityData = computed(() => {
            const data = []
            const today = new Date()
            
            for (let i = 29; i >= 0; i--) {
                const date = new Date(today)
                date.setDate(date.getDate() - i)
                
                // Случайное количество задач для демонстрации
                const count = Math.floor(Math.random() * 5)
                
                data.push({
                    date: date.toLocaleDateString('ru-RU', { 
                        day: '2-digit', 
                        month: 'short' 
                    }),
                    count: count
                })
            }
            
            return data
        })
        
        // Методы форматирования
        const formatDate = (dateString) => {
            if (!dateString) return '—'
            const date = new Date(dateString)
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: 'short'
            })
        }
        
        const formatTime = (date) => {
            return date.toLocaleTimeString('ru-RU', {
                hour: '2-digit',
                minute: '2-digit'
            })
        }
        
        const formatCurrency = (amount) => {
            if (!amount || amount === 0) return '—'
            return new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(amount)
        }
        
        const getActivityHeight = (count) => {
            const maxCount = Math.max(...activityData.value.map(d => d.count))
            if (maxCount === 0) return 0
            return (count / maxCount) * 100
        }
        
        // Обновление времени последнего обновления
        const refreshStats = () => {
            lastUpdated.value = new Date()
        }
        
        // Автоматическое обновление каждую минуту
        onMounted(() => {
            setInterval(() => {
                // Обновляем время, но не данные
                lastUpdated.value = new Date()
            }, 60000) // 1 минута
        })
        
        return {
            lastUpdated,
            activityData,
            formatDate,
            formatTime,
            formatCurrency,
            getActivityHeight,
            refreshStats
        }
    }
}
</script>

<style scoped>
.maintenance-stats {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Заголовок */
.stats-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.stats-header h3 {
    font-size: 1.5rem;
    color: var(--text-primary);
    margin: 0;
}

.btn-refresh {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
}

.btn-refresh:hover:not(:disabled) {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.btn-refresh:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.refresh-icon {
    font-size: 1rem;
    transition: transform 0.3s ease;
}

.refresh-icon.spinning {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Основные метрики */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}

@media (max-width: 1200px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}

.stat-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    border-left: 4px solid transparent;
    text-align: center;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.stat-card.highlight {
    border-left-color: var(--danger);
    background: linear-gradient(135deg, rgba(var(--danger-rgb), 0.05) 0%, rgba(var(--danger-rgb), 0.02) 100%);
}

@media (max-width: 1200px) {
    .stat-card {
        flex-direction: row;
    }
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.stat-icon.overdue {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
}

.stat-icon.pending {
    background: rgba(var(--warning-rgb), 0.1);
    color: var(--warning);
}

.stat-icon.completed {
    background: rgba(var(--success-rgb), 0.1);
    color: var(--success);
}

.stat-icon.total {
    background: rgba(var(--primary-rgb), 0.1);
    color: var(--primary);
}

.stat-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.stat-warning {
    font-size: 0.8rem;
    color: var(--danger);
    background: rgba(var(--danger-rgb), 0.1);
    padding: 4px 8px;
    border-radius: 6px;
    display: inline-block;
}

.stat-hint {
    font-size: 0.8rem;
    color: var(--text-tertiary);
}

/* Прогресс бар */
.stat-progress {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
}

.progress-bar {
    flex: 1;
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--success) 0%, var(--success-light) 100%);
    border-radius: 4px;
    transition: width 0.5s ease;
}

.progress-text {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--success);
    min-width: 40px;
}

/* Распределение задач */
.stat-distribution {
    margin-top: 10px;
}

.dist-item {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
}

.dist-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.overdue-dot {
    background: var(--danger);
}

.pending-dot {
    background: var(--warning);
}

.dist-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

/* Дополнительная информация */
.stats-details {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 30px;
}

@media (max-width: 992px) {
    .stats-details {
        grid-template-columns: 1fr;
    }
}

.details-section h4 {
    font-size: 1.1rem;
    color: var(--text-primary);
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.detail-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.detail-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.detail-value {
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-primary);
}

/* График активности */
.activity-chart {
    display: flex;
    align-items: flex-end;
    height: 100px;
    gap: 4px;
    margin-bottom: 15px;
    padding: 15px;
    background: var(--bg-secondary);
    border-radius: 10px;
}

.activity-bar {
    flex: 1;
    background: rgba(var(--success-rgb), 0.3);
    border-radius: 4px 4px 0 0;
    position: relative;
    transition: height 0.3s ease;
    min-height: 4px;
}

.activity-bar.active {
    background: var(--success);
}

.activity-bar:hover {
    opacity: 0.8;
}

.bar-tooltip {
    position: absolute;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--text-primary);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.activity-bar:hover .bar-tooltip {
    opacity: 1;
}

.activity-legend {
    display: flex;
    justify-content: center;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.completed-dot {
    background: var(--success);
}

/* Срочные действия */
.urgent-actions {
    background: linear-gradient(135deg, rgba(var(--danger-rgb), 0.1) 0%, rgba(var(--danger-rgb), 0.05) 100%);
    border: 1px solid rgba(var(--danger-rgb), 0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.urgent-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.urgent-icon {
    font-size: 1.5rem;
}

.urgent-header h4 {
    font-size: 1.2rem;
    color: var(--danger);
    margin: 0;
}

.urgent-message {
    color: var(--text-secondary);
    margin-bottom: 15px;
    font-size: 0.95rem;
}

.action-buttons {
    display: flex;
    gap: 10px;
}

.btn-action {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}

.btn-action.primary {
    background: var(--danger);
    color: white;
}

.btn-action.primary:hover {
    background: var(--danger-dark);
    transform: translateY(-2px);
}

.btn-action.secondary {
    background: white;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-action.secondary:hover {
    background: var(--bg-secondary);
    transform: translateY(-2px);
}

/* Подсказки */
.tips-section {
    background: linear-gradient(135deg, rgba(var(--primary-rgb), 0.05) 0%, rgba(var(--primary-rgb), 0.02) 100%);
    border: 1px solid rgba(var(--primary-rgb), 0.1);
    border-radius: 12px;
    padding: 20px;
}

.tips-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.tips-icon {
    font-size: 1.5rem;
}

.tips-header h4 {
    font-size: 1.2rem;
    color: var(--primary);
    margin: 0;
}

.tips-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.tip-icon {
    font-size: 1.2rem;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.tip-content {
    flex: 1;
}

.tip-content strong {
    display: block;
    font-size: 0.95rem;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.tip-content p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin: 0;
}
</style>