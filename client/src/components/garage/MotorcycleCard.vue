<template>
    <div class="motorcycle-card">
        <div class="card-header">
            <h3>{{ motorcycle.brand }} {{ motorcycle.model }}</h3>
            <div class="card-actions">
                <button @click="$emit('edit')" class="btn-icon">
                    <i class="fas fa-edit"></i>
                </button>
                <button @click="$emit('delete')" class="btn-icon danger">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
        
        <div class="motorcycle-content">
            <!-- Изображение мотоцикла -->
            <div class="motorcycle-image">
                <img 
                    v-if="motorcycle.image_url" 
                    :src="motorcycle.image_url" 
                    :alt="motorcycle.brand + ' ' + motorcycle.model"
                >
                <div v-else class="image-placeholder">
                    <i class="fas fa-motorcycle"></i>
                </div>
            </div>
            
            <!-- Характеристики -->
            <div class="motorcycle-specs">
                <div class="spec-item">
                    <span class="spec-label">Год:</span>
                    <span class="spec-value">{{ motorcycle.year }}</span>
                </div>
                <div class="spec-item">
                    <span class="spec-label">Объем двигателя:</span>
                    <span class="spec-value">{{ motorcycle.engine_volume }} см³</span>
                </div>
                <div class="spec-item">
                    <span class="spec-label">Цвет:</span>
                    <span class="spec-value">{{ motorcycle.color }}</span>
                </div>
                <div class="spec-item">
                    <span class="spec-label">Пробег:</span>
                    <span class="spec-value">{{ formatNumber(motorcycle.current_mileage) }} км</span>
                </div>
                <div class="spec-item">
                    <span class="spec-label">Номер:</span>
                    <span class="spec-value plate">{{ motorcycle.license_plate }}</span>
                </div>
                <div v-if="motorcycle.vin" class="spec-item">
                    <span class="spec-label">VIN:</span>
                    <span class="spec-value">{{ motorcycle.vin }}</span>
                </div>
            </div>
            
            <!-- Дополнительная информация -->
            <div class="additional-info">
                <div v-if="motorcycle.insurance_expiry" class="info-item">
                    <i class="fas fa-shield-alt"></i>
                    <span>Страховка до: {{ formatDate(motorcycle.insurance_expiry) }}</span>
                </div>
                <div v-if="motorcycle.registration_expiry" class="info-item">
                    <i class="fas fa-file-alt"></i>
                    <span>Регистрация до: {{ formatDate(motorcycle.registration_expiry) }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MotorcycleCard',
    
    props: {
        motorcycle: {
            type: Object,
            required: true
        }
    },
    
    methods: {
        formatNumber(num) {
            return new Intl.NumberFormat('ru-RU').format(num)
        },
        
        formatDate(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString('ru-RU')
        }
    }
}
</script>

<style scoped>
.motorcycle-card {
    background: var(--dark-light);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
}

.card-header h3 {
    margin: 0;
    font-size: 1.5rem;
    color: var(--light);
}

.card-actions {
    display: flex;
    gap: 10px;
}

.motorcycle-content {
    padding: 20px;
}

.motorcycle-image {
    width: 100%;
    height: 250px;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
    background: rgba(0, 0, 0, 0.3);
}

.motorcycle-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.image-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
    color: rgba(255, 255, 255, 0.2);
}

.motorcycle-specs {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}

.spec-item {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
}

.spec-label {
    color: var(--gray);
    font-size: 0.9rem;
}

.spec-value {
    color: var(--light);
    font-weight: 500;
}

.spec-value.plate {
    font-family: monospace;
    background: var(--dark);
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 1px;
}

.additional-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    color: var(--light);
}

.info-item i {
    color: var(--primary);
}

.btn-icon {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--light);
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-icon:hover {
    background: var(--primary);
    transform: translateY(-2px);
}

.btn-icon.danger:hover {
    background: var(--danger);
}

@media (max-width: 768px) {
    .motorcycle-specs {
        grid-template-columns: 1fr;
    }
    
    .motorcycle-image {
        height: 200px;
    }
}
</style>