<template>
    <div class="history-card">
        <div class="card-header">
            <div class="header-title">
                <h2>
                    <i class="fas fa-history"></i>
                    История обслуживания
                </h2>
                <span class="records-count" v-if="history.length > 0">
                    {{ history.length }} {{ pluralize(history.length, ['запись', 'записи', 'записей']) }}
                </span>
            </div>
            <BaseButton
                variant="primary"
                @click="$emit('add-record')"
                class="add-button"
            >
                <i class="fas fa-plus"></i>
                Добавить запись
            </BaseButton>
        </div>

        <div class="card-body">
            <div v-if="history.length > 0" class="history-list">
                <div 
                    v-for="record in displayedRecord" 
                    :key="record.id" 
                    class="history-item"
                    :class="{ 'has-description': record.description }"
                >
                    <!-- Временная линия -->
                    <div class="timeline-indicator">
                        <div class="timeline-dot"></div>
                        <div class="timeline-line"></div>
                    </div>

                    <div class="history-content">
                        <!-- Заголовок и дата -->
                        <div class="history-header">
                            <div class="history-title-wrapper">
                                <h3 class="history-title">{{ record.title }}</h3>
                                <span class="history-badge">
                                    <i class="fas fa-calendar-alt"></i>
                                    {{ formatDate(record.last_maintenance_date) }}
                                </span>
                            </div>
                            
                            <div class="history-actions">
                                <button 
                                    class="btn-icon btn-outline" 
                                    @click="$emit('edit-record', record)"
                                    title="Редактировать запись"
                                >
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button 
                                    class="btn-icon btn-outline" 
                                    @click="confirmDelete(record)"
                                    title="Удалить запись"
                                >
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>

                        <!-- Детали записи -->
                        <div class="history-details">
                            <!-- Описание -->
                            <div v-if="record.description" class="detail-block description">
                                <div class="detail-icon">
                                    <i class="fas fa-align-left"></i>
                                </div>
                                <div class="detail-content">
                                    <span class="detail-label">Описание работ</span>
                                    <p class="detail-text">{{ record.description }}</p>
                                </div>
                            </div>

                            <!-- Запчасти -->
                            <div v-if="record.parts_used && record.parts_used.length !== 0" class="detail-block parts">
                                <div class="detail-icon">
                                    <i class="fas fa-cog"></i>
                                </div>
                                <div class="detail-content">
                                    <span class="detail-label">Использованные запчасти</span>
                                    <div class="parts-list">
                                        <span 
                                            v-for="(part, index) in getPartsArray(record.parts_used)" 
                                            :key="index"
                                            class="part-tag"
                                        >
                                            {{ part }}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <!-- Стоимость -->
                            <div v-if="record.cost" class="detail-block cost">
                                <div class="detail-icon">
                                    <i class="fas fa-ruble-sign"></i>
                                </div>
                                <div class="detail-content">
                                    <span class="detail-label">Стоимость работ</span>
                                    <span class="cost-value">{{ formatCost(record.cost) }} ₽</span>
                                </div>
                            </div>

                            <!-- Дополнительная информация (пробег) -->
                            <div v-if="record.mileage" class="detail-block mileage">
                                <div class="detail-icon">
                                    <i class="fas fa-tachometer-alt"></i>
                                </div>
                                <div class="detail-content">
                                    <span class="detail-label">Пробег при обслуживании</span>
                                    <span class="mileage-value">{{ record.mileage }} км</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Пустое состояние -->
            <div v-else class="empty-state">
                <div class="empty-state-icon">
                    <i class="fas fa-history"></i>
                </div>
                <h3>История обслуживания пуста</h3>
                <p>Добавьте первую запись о техническом обслуживании</p>
                <BaseButton variant="primary" @click="$emit('add-record')">
                    <i class="fas fa-plus"></i>
                    Добавить запись
                </BaseButton>
            </div>

            <!-- Индикатор загрузки (если нужно показать, что есть еще записи) -->
            <div v-if="history.length > limit" class="show-more">
                <BaseButton variant="outline" @click="$emit('show-all')">
                    Показать все записи ({{ history.length }})
                </BaseButton>
            </div>
        </div>
    </div>
</template>

<script>
import BaseButton from '../../ui/BaseButton.vue';

export default {
    name: 'MaintenanceHistory',

    components: {
        BaseButton
    },

    props: {
        history: {
            type: Array,
            required: true,
            default: () => []
        },
        limit: {
            type: Number,
            default: 10
        }
    },

    computed: {
        displayedRecord() {
            return this.limit ? this.history.slice(0, this.limit) : this.history;
        }
    },

    methods: {
        formatDate(dateString) {
            if (!dateString) return 'Не указано';
            const date = new Date(dateString);
            if (isNaN(date.getTime())) return 'Не указано';
            
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        },

        formatCost(cost) {
            if (!cost) return '0';
            return cost.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        },

        getPartsArray(parts) {
            if (!parts) return [];
            if (Array.isArray(parts)) return parts;
            if (typeof parts === 'string') return parts.split(',').map(p => p.trim());
            return [];
        },

        pluralize(count, words) {
            const cases = [2, 0, 1, 1, 1, 2];
            return words[(count % 100 > 4 && count % 100 < 20) ? 2 : cases[Math.min(count % 10, 5)]];
        },

        confirmDelete(record) {
            if (confirm(`Вы уверены, что хотите удалить запись "${record.title}"?`)) {
                this.$emit('delete-record', record);
            }
        }
    }
}
</script>

<style scoped>
.history-card {
    background: rgba(20, 20, 30, 0.95);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Header */
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

.header-title {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
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
    color: #9c27b0;
    font-size: 1.2em;
}

.records-count {
    background: rgba(156, 39, 176, 0.15);
    color: #ce93d8;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 500;
    border: 1px solid rgba(156, 39, 176, 0.3);
}

.add-button {
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-body {
    padding: 24px;
}

/* Timeline стили */
.history-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: relative;
}

.history-item {
    display: flex;
    gap: 20px;
    position: relative;
    transition: all 0.3s ease;
}

.timeline-indicator {
    position: relative;
    width: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.timeline-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: linear-gradient(135deg, #9c27b0, #7b1fa2);
    border: 2px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 15px rgba(156, 39, 176, 0.5);
    z-index: 2;
}

.timeline-line {
    position: absolute;
    top: 20px;
    width: 2px;
    height: calc(100% + 16px);
    background: linear-gradient(180deg, 
        rgba(156, 39, 176, 0.5) 0%, 
        rgba(156, 39, 176, 0.2) 80%,
        transparent 100%
    );
}

.history-item:last-child .timeline-line {
    display: none;
}

/* Контент */
.history-content {
    flex: 1;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
    margin-bottom: 8px;
}

.history-content:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(156, 39, 176, 0.3);
    transform: translateX(5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;
}

.history-title-wrapper {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.history-title {
    margin: 0;
    font-size: 1.15em;
    font-weight: 600;
    color: #fff;
}

.history-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    font-size: 0.85em;
    color: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.history-badge i {
    color: #9c27b0;
    font-size: 0.9em;
}

/* Кнопки действий */
.history-actions {
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
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #fff;
    font-size: 1em;
}

.btn-icon:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}

.btn-icon:first-child:hover {
    background: rgba(33, 150, 243, 0.2);
    border-color: #2196f3;
    color: #2196f3;
}

.btn-icon:last-child:hover {
    background: rgba(244, 67, 54, 0.2);
    border-color: #f44336;
    color: #f44336;
}

/* Детали */
.history-details {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.detail-block {
    display: flex;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(156, 39, 176, 0.15);
    color: #ce93d8;
    font-size: 1.1em;
}

.detail-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.detail-label {
    font-size: 0.75em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: rgba(255, 255, 255, 0.5);
}

.detail-text {
    margin: 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.95em;
    line-height: 1.5;
}

/* Теги запчастей */
.parts-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.part-tag {
    padding: 4px 12px;
    background: rgba(33, 150, 243, 0.15);
    border-radius: 20px;
    font-size: 0.85em;
    color: #90caf9;
    border: 1px solid rgba(33, 150, 243, 0.3);
}

/* Стоимость */
.cost-value {
    font-size: 1.2em;
    font-weight: 700;
    color: #4caf50;
}

.mileage-value {
    font-size: 1.1em;
    font-weight: 600;
    color: #ff9800;
}

/* Специфичные стили для блоков */
.detail-block.description .detail-icon {
    background: rgba(33, 150, 243, 0.15);
    color: #90caf9;
}

.detail-block.parts .detail-icon {
    background: rgba(255, 152, 0, 0.15);
    color: #ffb74d;
}

.detail-block.cost .detail-icon {
    background: rgba(76, 175, 80, 0.15);
    color: #81c784;
}

.detail-block.mileage .detail-icon {
    background: rgba(255, 87, 34, 0.15);
    color: #ff8a65;
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
    background: linear-gradient(135deg, rgba(156, 39, 176, 0.2), rgba(123, 31, 162, 0.2));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5em;
    color: #ce93d8;
    border: 2px solid rgba(156, 39, 176, 0.3);
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

/* Show more */
.show-more {
    margin-top: 20px;
    text-align: center;
}

.show-more button {
    min-width: 200px;
}

/* Адаптивность */
@media (max-width: 768px) {
    .card-header {
        flex-direction: column;
        align-items: stretch;
    }

    .header-title {
        justify-content: space-between;
    }

    .history-header {
        flex-direction: column;
    }

    .history-actions {
        width: 100%;
        justify-content: flex-end;
    }

    .detail-block {
        flex-direction: column;
    }

    .detail-icon {
        width: 100%;
        height: auto;
        padding: 8px;
    }
}

@media (max-width: 480px) {
    .card-body {
        padding: 16px;
    }

    .history-item {
        gap: 12px;
    }

    .history-content {
        padding: 16px;
    }

    .history-title-wrapper {
        flex-direction: column;
        align-items: flex-start;
    }

    .timeline-indicator {
        width: 16px;
    }
}

/* Анимация появления */
.history-item {
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-10px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Кастомный скроллбар */
.history-list::-webkit-scrollbar {
    width: 6px;
}

.history-list::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb {
    background: rgba(156, 39, 176, 0.5);
    border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover {
    background: rgba(156, 39, 176, 0.7);
}
</style>