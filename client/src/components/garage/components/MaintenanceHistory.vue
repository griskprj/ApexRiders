<template>
    <!-- История обслуживания -->
    <div class="history-card">
        <div class="card-header">
            <h2><i class="fas fa-history"></i> История обслуживания</h2>
            <BaseButton
                variant="outline"
                @click="$emit('add-record')"
            >
                Добавить запись
            </BaseButton>
        </div>
        <div class="card-body">
            <div v-if="history.length > 0" class="history-list">
                <div v-for="record in displayedRecord" :key="record.id" class="history-item">
                    <div class="history-icon">
                        <div class="history-title">{{ record.title }}</div>
                        <div class="history-date">
                            {{ formatDate(record.last_maintenance_date) }}
                        </div>
                    </div>
                    <div class="history-content">
                        <div class="history-details">
                            <span v-if="record.description" class="history-description">
                                <i class="fas fa-align-left"></i> {{ record.description }}
                            </span>
                            <div v-if="record.cost" class="history-cost">
                                <i class="fas fa-ruble-sign"></i> {{ record.cost }} руб.
                            </div>
                            <div v-if="record.parts_used.length !== 0" class="history-parts">
                                <i class="fas fa-cog"></i> {{ record.parts_used }}
                            </div>
                        </div>
                        <div class="history-actions">
                            <BaseButton
                                variant="outline"
                                @click="$emit('edit-record', record)"
                            >
                                <i class="fas fa-edit"></i>
                            </BaseButton>

                            <BaseButton
                                variant="outline"
                                @click="$emit('delete-record', record)"
                            >
                                <i class="fas fa-trash"></i>
                            </BaseButton>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="empty-state">
                <i class="fas fa-history"></i>
                <p>История обслуживания пуста</p>
            </div>
        </div>
    </div>
</template>

<script>
import BaseButton from '../../ui/BaseButton.vue'; /** Компонент кнопки */

export default {
    name: 'MaintenanceHistory',

    components: {
        BaseButton
    },

    props: {
        /** Список записей обслуживания */
        history: {
            type: Array,
            required: true,
            default: () => []
        },
        /** Лимит отображения записей */
        limit: {
            type: Number,
            default: 20
        }
    },
    computed: {
        displayedRecord() {
            return this.limit ? this.history.slice(0, this.limit) : this.history
        }
    },
    methods: {
        formatDate(dateString) {
            if (!dateString) return 'Не указано'
            const date = new Date(dateString)
            if (isNaN(date.getTime())) return 'Не указано'
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

.history-card {
    background: rgba(10, 10, 15, 0.7);
    backdrop-filter: blur(20px);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.history-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.history-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.history-item:hover {
    background: rgba(var(--accent-rgb), 0.1);
    border-color: var(--accent);
}

.history-icon {
    width: 100%;
    min-height: 36px;
    border-radius: 8px;
    background: linear-gradient(135deg, #6f42c1 0%, #6610f2 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    flex-wrap: wrap;
    gap: 10px;
}

.history-title {
    font-weight: 600;
    color: var(--text);
    font-size: 1.05em;
    margin-top: 8px;
}

.history-content {
    display: flex;
    flex-direction: column;
}

.history-date {
    font-size: 0.85em;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: space-around;
    margin-bottom: 8px;
    gap: 5px;
}

.history-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    margin-bottom: 16px;
}

.history-description {
    color: var(--text-secondary);
    font-size: 0.95em;
    line-height: 1.4;
}

.history-cost {
    color: #28a745;
    font-weight: 600;
    font-size: 0.9em;
    display: flex;
    align-items: center;
    gap: 5px;
}

.history-parts {
    color: var(--text-secondary);
    font-size: 0.9em;
    display: flex;
    align-items: center;
    gap: 5px;
    margin-bottom: 10px;
}

.history-actions {
    display: flex;
    justify-content: space-evenly;
    gap: 8px;
}

.history-actions button {
    width: 100%;
}

.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-secondary);
}

.empty-state i {
    font-size: 3em;
    margin-bottom: 15px;
    color: var(--text-secondary);
    opacity: 0.5;
}

.empty-state p {
    margin: 0;
    font-size: 1.1em;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.task-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
    gap: 10px;
}
</style>