<template>
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
                <button class="btn btn-small btn-outline" @click="$emit('update-mileage')">
                    <i class="fas fa-edit"></i> Обновить
                </button>
            </div>
            <div class="action-buttons">
                <button class="btn btn-primary" @click="$emit('edit-moto')">
                    <i class="fas fa-edit"></i> Редактировать
                </button>
                <button class="btn btn-danger" @click="$emit('delete-moto')">
                    <i class="fas fa-trash"></i> Удалить
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MotoInfo',

    props: {
        motorcycle: {
            type: Object,
            default: null
        }
    },
}
</script>

<style scoped>

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

.btn-danger {
    background: linear-gradient(135deg, var(--danger) 0%, var(--very-danger) 100%);
    color: white;
    border: 1px solid var(--danger);
}

.btn-danger:hover {
    background: linear-gradient(135deg, #ff5e6d 0%, var(--danger) 100%);
    box-shadow: 0 0 20px rgba(255, 71, 87, 0.5);
}
</style>