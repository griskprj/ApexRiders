<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="closeTaskModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Новая задача ТО</h3>
                <BaseButton
                    variant="outline"
                    @click="handleClose"
                >
                    <i class="fas fa-times"></i>
                </BaseButton>
            </div>
            
            <form @submit.prevent="handleSubmit" class="modal-form">
                <div class="form-row">
                    <BasicSelect
                        label="Мотоцикл"
                        :items="motorcycles"
                        @changeOption="handleOptionHandler"
                    />
                    
                    <BaseInput
                        id="title"
                        type="text"
                        label="Название задачи *"
                        v-model="form.title"
                        max="128"
                        required
                    />
                </div>

                <div class="form-row">
                    <BaseTextarea
                        label="Описание задачи"
                        resize="none"
                        @change="handleDescChange"
                    />
                    <BaseTextarea
                        label="Заметки"
                        resize="none"
                        @change="handleNoteChange"
                    />
                </div>

                <div class="form-row">
                    <BaseInput
                        id="last_maintenance_date"
                        type="date"
                        label="Дата последнего ТО"
                        v-model="form.last_maintenance_date"
                    />

                    <BaseInput
                        id="last_maintenance_mileage"
                        type="number"
                        label="Пробег при последнем ТО"
                        v-model="form.last_maintenance_mileage"
                    />
                </div>

                <div class="form-row">
                    <BaseRadioButton
                        label="По пробегу"
                        option="mileage"
                        @change="handleRadioChange"
                    />
                    <BaseRadioButton
                        label="По времени"
                        option="time"
                        @change="handleRadioChange"
                    />
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
import BasicSelect from '../ui/BasicSelect.vue';
import BaseTextarea from '../ui/BaseTextarea.vue';
import BaseRadioButton from '../ui/BaseRadioButton.vue';

export default {
    name: 'AddTaskModal',

    components: {
        BaseButton,
        BaseInput,
        BasicSelect,
        BaseTextarea,
        BaseRadioButton
    },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        motorcycles: {
            type: Array,
            default: null
        }
    },

    emits: ['close', 'create'],

    data() {
        return {
            isCreating: false,
            form: {
                motorcycle_id: null,
                title: '',
                description: '',
                last_maintenance_date: null,
                last_maintenance_mileage: null,
                schedule_type: 'mileage',
                interval_value: null,
                interval_unit: '',
                priority: '',
                notes: '',
                is_recurring: true
            }
        }
    },

    methods: {
        handleClose() {
            this.resetForm()
            this.$emit('close')
        },

        handleOptionHandler(item_id) {
            this.form.motorcycle_id = item_id
        },

        handleDescChange(content) {
            this.form.description = content
        },

        handleNoteChange(content) {
            this.form.notes = content
        },

        handleRadioChange(option) {
            this.form.schedule_type = option
        },

        resetForm() {
            this.form = {
                motorcycle_id: null,
                title: '',
                description: '',
                last_maintenance_date: null,
                last_maintenance_mileage: null,
                schedule_type: '',
                interval_value: null,
                interval_unit: '',
                priority: '',
                notes: '',
                is_recurring: true
            }
        },

        async handleSubmit() {
            this.isCreating = true

            try {
                const token = authService.getToken()

                const dataToSend = {
                    ...this.form,
                    last_maintenance_mileage: this.form.last_maintenance_mileage ? 
                        Number(this.form.last_maintenance_mileage) : null,
                    interval_value: this.form.interval_value ? 
                        Number(this.form.interval_value) : null
                }

                const response = await axios.post('/api/garage/maintenance', dataToSend, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })

                this.$emit('create', response.data.motorcycle || response.data)
                this.handleClose()
            } catch (error) {
                console.error('Ошибка создания мотоцикла', error)
                alert(error.response.data.error || 'Ошибка при создании мотоцикла')
            } finally {
                this.isCreating = false
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

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: var(--text);
}

.checkbox-label input[type="checkbox"] {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--text-secondary);
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
  transition: all 0.3s ease;
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom {
  border-color: var(--primary);
  background: var(--primary);
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 14px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.radio-group {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: var(--text);
}

.radio-label input[type="radio"] {
  display: none;
}

.radio-custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--text-secondary);
  border-radius: 50%;
  margin-right: 10px;
  position: relative;
  transition: all 0.3s ease;
}

.radio-label input[type="radio"]:checked + .radio-custom {
  border-color: var(--primary);
}

.radio-label input[type="radio"]:checked + .radio-custom::after {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--primary);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
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