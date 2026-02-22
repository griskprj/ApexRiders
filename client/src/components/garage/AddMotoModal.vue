<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
        <div class="modal-content">
            <div class="modal-header">
                <h3>{{ motorcycleToEdit ? 'Редактировать мотоцикл' : 'Добавить мотоцикл' }}</h3>
                <BaseButton
                    variant="outline"
                    @click="handleClose"
                >
                    <i class="fas fa-times"></i>
                </BaseButton>
            </div>
            
            <form @submit.prevent="handleSubmit" class="modal-form">
                <div class="form-row">
                    <BaseInput
                        id="brand"
                        type="text"
                        label="Марка *"
                        v-model="form.brand"
                        max="25"
                        required
                    />
                    <BaseInput
                        id="model"
                        type="text"
                        label="Модель *"
                        v-model="form.model"
                        max="50"
                        required
                    />
                </div>
                
                <div class="form-row">
                    <BaseInput
                        id="year"
                        type="number"
                        label="Год выпуска"
                        v-model="form.year"
                        min="1900"
                        :max="new Date().getFullYear()"
                    />
                    
                    <BaseInput
                        id="engineVolume"
                        type="number"
                        label="Объем двигателся (cc) *"
                        v-model="form.engine_volume"
                        min="50"
                        max="3000"
                        required
                    />
                </div>
                
                <div class="form-row">
                    <BaseInput
                        id="color"
                        type="text"
                        label="Цвет"
                        v-model="form.color"
                        max="50"
                    />

                    <BaseInput
                        id="licensePlate"
                        type="text"
                        label="Госномер"
                        v-model="form.license_plate"
                        max="10"
                    />

                    <BaseInput
                        id="vin"
                        type="text"
                        label="VIN-номер"
                        v-model="form.vin"
                        max="17"
                    />
                    
                    <BaseInput
                        id="insurance_expriy"
                        type="date"
                        label="Страховка до"
                        v-model="form.insurance_expiry"
                    />
                </div>
                
                <div class="modal-actions">
                    <BaseButton
                        type="button"
                        variant="outline"
                        @click="handleClose"
                        :disabled="isSaving"
                    >
                        Отмена
                    </BaseButton>

                    <BaseButton
                        type="submit"
                        variant="primary"
                        :loading="isSaving"
                    >
                        {{ motorcycleToEdit ? 'Сохранить' : 'Добавить' }}
                    </BaseButton>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { authService } from '../../utils/checkAuth';
import BaseButton from '../ui/BaseButton.vue';
import BaseInput from '../ui/BaseInput.vue';

export default {
    name: 'AddMotoModal',

    components: {
        BaseButton,
        BaseInput
    },

    props: {
        isOpen: {
            type: Boolean,
            required: true
        },
        motorcycleToEdit: {
            type: Object,
            default: null
        }
    },

    emits: ['close', 'save'],

    data() {
        return {
            isSaving: false,
            form: {
                brand: '',
                model: '',
                year: null,
                engine_volume: null,
                color: '',
                license_plate: '',
                vin: '',
                insurance_expiry: ''
            }
        }
    },

    watch: {
        motorcycleToEdit: {
            handler(newValue) {
                if (newValue) {
                    Object.assign(this.form, newValue)
                } else {
                    this.resetForm()
                }
            },
            immediate: true,
            deep: true
        }
    },

    methods: {
        handleClose() {
            this.resetForm()
            this.$emit('close')
        },

        resetForm() {
            this.form = {
                brand: '',
                model: '',
                year: null,
                engine_volume: null,
                color: '',
                license_plate: '',
                vin: '',
                insurance_expiry: ''
            }
        },

        async handleSubmit() {
            this.isSaving = true
            
            try {
                const token = authService.getToken()
                let response
    
                if (this.motorcycleToEdit) {
                    // Редактирование
                    response = await axios.put(`/api/motorcycle/${this.motorcycleToEdit.id}`, this.form, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    })
                } else {
                    // Добавление
                    response = await axios.post('/api/motorcycle', this.form, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    })
                }

                this.$emit('save', response.data?.motorcycle || response.data)
                this.handleClose()
            } catch (error) {
                console.error('Ошибка сохранения', error)
                alert(error.response?.data?.error || 'Ошибка при сохранении')
            } finally {
                this.isSaving = false
            }
        }
    }
}
</script>

<style scoped>
.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    color: var(--text);
    font-weight: 500;
    font-size: 0.95rem;
}

.form-group input {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

.form-actions {
    padding-top: 10px;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.modal-content {
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 25px 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    font-size: 1.4rem;
    color: var(--text);
}

.modal-close {
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.5rem;
    cursor: pointer;
    padding: 5px;
    transition: all 0.3s ease;
}

.modal-close:hover {
    color: var(--text);
}

.modal-form {
    padding: 25px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 480px) {
    .modal-body {
        padding: 15px;
    }
    
    .modal-body h4 {
        font-size: 1.1rem;
    }

    .modal-content {
        margin: 10px;
        padding: 15px;
    }
    
    .modal-form {
        padding: 15px;
    }
}

@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 15px;
    }
}
</style>