<template>
    <div class="garage-header">
        <!-- Навигация -->
        <div class="header-navigation">
            <router-link to="/garage" class="back-link">
                <i class="fas fa-arrow-left"></i>
                <span>Вернуться к списку</span>
            </router-link>
            <div class="header-actions">
                <button @click="handleUpdateMileage" class="btn-primary">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Обновить пробег</span>
                </button>
            </div>
        </div>

        <!-- Основная информация -->
        <div class="header-content">
            <div class="motorcycle-info">
                <h1>{{ motorcycle.brand }} {{ motorcycle.model }}</h1>
                <div class="motorcycle-subtitle">
                    <span class="year">{{ motorcycle.year }} год</span>
                    <span class="separator">•</span>
                    <span class="engine">{{ motorcycle.engine_volume }} см³</span>
                    <span class="separator">•</span>
                    <span class="mileage">{{ formatNumber(motorcycle.current_mileage) }} км</span>
                </div>
                <div class="license-plate">
                    <i class="fas fa-bolt"></i>
                    <span>{{ motorcycle.license_plate || 'Номер не указан' }}</span>
                </div>
            </div>
            
            <div class="header-stats">
                <div class="stat-item">
                    <div class="stat-value">{{ stats.total_tasks || 0 }}</div>
                    <div class="stat-label">Всего задач</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ stats.overdue || 0 }}</div>
                    <div class="stat-label">Просрочено</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ stats.completion_rate || 0 }}%</div>
                    <div class="stat-label">Выполнено</div>
                </div>
            </div>
        </div>

        <!-- Статусные индикаторы -->
        <div class="status-indicators">
            <div v-if="hasInsuranceExpiring" class="status-item warning">
                <i class="fas fa-exclamation-triangle"></i>
                <span>Страховка скоро истекает</span>
            </div>
            <div v-if="hasRegistrationExpiring" class="status-item warning">
                <i class="fas fa-exclamation-triangle"></i>
                <span>Регистрация скоро истекает</span>
            </div>
            <div v-if="hasOverdueTasks" class="status-item danger">
                <i class="fas fa-exclamation-circle"></i>
                <span>Есть просроченные задачи ТО</span>
            </div>
        </div>
    </div>
</template>

<script>
import { computed } from 'vue'

export default {
    name: 'GarageHeader',
    
    props: {
        motorcycle: {
            type: Object,
            required: true,
            default: () => ({
                brand: '',
                model: '',
                year: '',
                engine_volume: '',
                current_mileage: 0,
                license_plate: '',
                insurance_expiry: null,
                registration_expiry: null
            })
        },
        stats: {
            type: Object,
            default: () => ({
                total_tasks: 0,
                overdue: 0,
                completion_rate: 0
            })
        }
    },
    
    emits: ['update-mileage'],
    
    setup(props, { emit }) {
        // Форматирование чисел
        const formatNumber = (num) => {
            return new Intl.NumberFormat('ru-RU').format(num)
        }

        // Проверка на истечение страховки (менее 30 дней)
        const hasInsuranceExpiring = computed(() => {
            if (!props.motorcycle.insurance_expiry) return false
            const expiryDate = new Date(props.motorcycle.insurance_expiry)
            const today = new Date()
            const daysDiff = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
            return daysDiff <= 30 && daysDiff > 0
        })

        // Проверка на истечение регистрации (менее 30 дней)
        const hasRegistrationExpiring = computed(() => {
            if (!props.motorcycle.registration_expiry) return false
            const expiryDate = new Date(props.motorcycle.registration_expiry)
            const today = new Date()
            const daysDiff = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
            return daysDiff <= 30 && daysDiff > 0
        })

        // Проверка на просроченные задачи
        const hasOverdueTasks = computed(() => {
            return props.stats.overdue > 0
        })

        // Обработчик обновления пробега
        const handleUpdateMileage = () => {
            emit('update-mileage')
        }

        return {
            formatNumber,
            hasInsuranceExpiring,
            hasRegistrationExpiring,
            hasOverdueTasks,
            handleUpdateMileage
        }
    }
}
</script>

<style scoped>
.garage-header {
    background: linear-gradient(135deg, rgba(30, 30, 40, 0.9) 0%, rgba(20, 20, 30, 0.95) 100%);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 25px;
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
    border-radius: 20px 20px 0 0;
}

.header-navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.back-link {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--gray);
    text-decoration: none;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.back-link:hover {
    color: var(--light);
}

.back-link i {
    font-size: 0.9rem;
}

.header-actions {
    display: flex;
    gap: 15px;
}

.btn-primary {
    background: var(--primary);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(var(--primary-rgb), 0.3);
}

.btn-primary i {
    font-size: 0.9rem;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.motorcycle-info h1 {
    margin: 0 0 10px 0;
    font-size: 2.2rem;
    color: var(--light);
    font-weight: 600;
}

.motorcycle-subtitle {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    color: var(--gray);
    font-size: 1.1rem;
}

.separator {
    opacity: 0.5;
}

.license-plate {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(var(--accent-rgb), 0.1);
    padding: 6px 12px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 1rem;
    color: var(--light);
    border: 1px solid rgba(var(--accent-rgb), 0.2);
}

.license-plate i {
    color: var(--accent);
}

.header-stats {
    display: flex;
    gap: 30px;
}

.stat-item {
    text-align: center;
    padding: 15px 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    min-width: 100px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

.stat-item:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-3px);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--light);
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-indicators {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

.status-item.warning {
    background: rgba(var(--warning-rgb), 0.1);
    color: var(--warning);
    border: 1px solid rgba(var(--warning-rgb), 0.2);
}

.status-item.danger {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
    border: 1px solid rgba(var(--danger-rgb), 0.2);
}

.status-item i {
    font-size: 0.8rem;
}

/* Адаптивность */
@media (max-width: 992px) {
    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 25px;
    }
    
    .header-stats {
        width: 100%;
        justify-content: space-between;
    }
    
    .stat-item {
        flex: 1;
        min-width: auto;
    }
}

@media (max-width: 768px) {
    .garage-header {
        padding: 20px;
    }
    
    .motorcycle-info h1 {
        font-size: 1.8rem;
    }
    
    .motorcycle-subtitle {
        flex-wrap: wrap;
        font-size: 1rem;
    }
    
    .header-stats {
        gap: 15px;
    }
    
    .stat-item {
        padding: 12px 15px;
    }
    
    .stat-value {
        font-size: 1.6rem;
    }
}

@media (max-width: 576px) {
    .header-navigation {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .header-actions {
        width: 100%;
    }
    
    .btn-primary {
        flex: 1;
        justify-content: center;
    }
    
    .header-stats {
        flex-direction: column;
    }
}
</style>