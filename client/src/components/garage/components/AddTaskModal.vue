<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
        <div class="modal-content">
            <div class="modal-header">
                <input v-model="formData.status" value="completed" type="hidden">
                <h3>{{ modalTitle }}</h3>
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
                    v-if="showMotorcycleSelect"
                    label="Мотоцикл *"
                    :items="motoForSelect"
                    withIcon="true"
                    icon="fa-motorcycle"
                    v-model="formData.motorcycle_id"
                />

                    <div v-else class="selected-motorcycle-info">
                        <div class="form-group">
                            <label>Мотоцикл</label>
                            <div class="motorcycle-badge">
                                <i class="fas fa-motorcycle"></i>
                                {{ motorcycleName }}
                            </div>
                        </div>
                    </div>  
                </div>

                <div class="form-row">
                    <BaseInput
                        id="title"
                        type="text"
                        label="Название *"
                        v-model="formData.title"
                        max="128"
                        :withIcon="true"
                        icon="fa-align-left"
                        required
                    />
                </div>

                <div class="form-row">
                    <BaseTextarea
                        label="Описание"
                        :resize="false"
                        v-model="formData.description"
                    />
                </div>

                <template v-if="mode === 'task'">
                    <div class="form-row">
                        <BaseInput
                            id="last_maintenance_date"
                            type="date"
                            label="Дата последнего ТО"
                            :withIcon="true"
                            icon="fa-calendar"
                            v-model="formData.last_maintenance_date"
                        />
                    </div>

                    <div class="form-row">
                        <BaseInput
                            id="last_maintenance_mileage"
                            type="number"
                            label="Пробег на последнем ТО"
                            min="0"
                            :withIcon="true"
                            icon="fa-road"
                            v-model="formData.last_maintenance_mileage"
                        />
                    </div>

                    <div class="form-row radio">
                        <label>Тип расписания *</label>
                        <div class="radio-group">
                            <BaseRadioButton
                                name="schedule_type"
                                value="mileage"
                                label="По пробегу"
                                v-model="formData.schedule_type"
                            />
                            <BaseRadioButton
                                name="schedule_type"
                                value="time"
                                label="По времени"
                                v-model="formData.schedule_type"
                            />
                        </div>
                    </div>

                    <div v-if="formData.schedule_type === 'mileage'" class="form-row">
                        <BaseInput
                            id="interval_value"
                            type="number"
                            label="Интервал (км) *"
                            min="1"
                            :withIcon="true"
                            icon="fa-tachometer"
                            v-model="formData.interval_value"
                            :required="formData.schedule_type === 'mileage'"
                        />
                    </div>
                    
                    <div v-if="formData.schedule_type === 'time'">
                        <div class="form-row">
                            <BaseInput
                                id="interval_value"
                                type="number"
                                label="Интервал *"
                                min="1"
                                :withIcon="true"
                                icon="fa-clock"
                                v-model="formData.interval_value"
                                :required="formData.schedule_type === 'time'"
                            />
                        </div>

                        <div class="form-row">
                            <BasicSelect
                                label="Единица измерения"
                                :items="[
                                    { value: 'months', label: 'Месяцы' },
                                    { value: 'days', label: 'Дни' }
                                ]"
                                :withIcon="true"
                                icon="fa-calendar"
                                v-model="formData.interval_unit"
                            />
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <BasicSelect
                            label="Приоритет"
                            :items="[
                                { value: 'low', label: 'Низкий' },
                                { value: 'medium', label: 'Средний' },
                                { value: 'high', label: 'Высокий' }
                            ]"
                            :withIcon="true"
                            icon="fa-exclamation-triangle"
                            v-model="formData.priority"
                        />
                    </div>
                    
                    <div class="form-row">
                        <BasicCheckBox
                            label="Повторяющаяся задача"
                            text="Это повторяющаяся задача?"
                            v-model="formData.is_recurring"
                        />
                    </div>
                </template>

                <template v-if="mode === 'history'">
                    <div class="form-row">
                        <BaseInput
                            id="completed_date"
                            type="date"
                            label="Дата выполнения *"
                            :withIcon="true"
                            icon="fa-calendar"
                            v-model="formData.completed_date"
                        />
                    </div>

                    <div class="form-row">
                        <BaseInput
                            id="mileage"
                            type="text"
                            label="Пробег при выполнении *"
                            v-model="formData.mileage"
                            min="1"
                            :max="motorcycleMileage"
                            required
                            :withIcon="true"
                            icon="fa-tachometer-alt"
                        />
                    </div>

                    <div class="form-row">
                        <BaseInput
                            id="cost"
                            type="number"
                            label="Стоимость (руб.)"
                            min="0"
                            step="0.01"
                            :withIcon="true"
                            icon="fa-ruble-sign"
                            v-model="formData.cost"
                        />
                    </div>

                    <div class="form-row">
                        <BaseTextarea
                            label="Использованные запчасти"
                            :resize="false"
                            v-model="formData.parts_used"
                        />
                    </div>
                </template>

                <div class="form-row">
                    <BaseTextarea
                        label="Заметки"
                        :resize="false"
                        v-model="formData.notes"
                    />
                </div>

                
                
                <div class="modal-footer">
                    <BaseButton
                        variant="outline"
                        :disabled="isSaving"
                        @click="handleClose"
                    >
                        Отмена
                    </BaseButton>

                    <BaseButton
                        variant="primary"
                        :loading="isSaving"
                        @click="handleSubmit"
                    >
                        {{ isEditing ? 'Обновить' : 'Сохранить' }}
                    </BaseButton>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { authService } from '../../../utils/checkAuth';
import BaseButton from '../../ui/BaseButton.vue';
import BaseInput from '../../ui/BaseInput.vue';
import BasicSelect from '../../ui/BasicSelect.vue';
import BaseTextarea from '../../ui/BaseTextarea.vue';
import BaseRadioButton from '../../ui/BaseRadioButton.vue';
import BasicCheckBox from '../../ui/BasicCheckBox.vue';

export default {
    name: 'AddTaskModal',

    components: {
        BaseButton,
        BaseInput,
        BasicSelect,
        BaseTextarea,
        BaseRadioButton,
        BasicCheckBox
    },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        mode: {
            type: String,
            validator: (value) => ['task', 'history'].includes(value),
            default: 'task'
        },
        motorcycles: {
            type: Array,
            default: () => []
        },
        motorcycleId: {
            type: [Number, String],
            default: null
        },
        motorcycleName: {
            type: String,
            default: ''
        },
        motorcycleMileage: {
            type: Number,
            default: null
        },
        isEditing: {
            type: Boolean,
            default: false
        },
        editData: {
            type: Object,
            default: null
        }
    },

    emits: ['close', 'save'],

    data() {
        return {
            isSaving: false,
            formData: this.getDefaultForm()
        }
    },

    computed: {
        modalTitle() {
            if (this.mode === 'task') {
                return this.isEditing ? 'Редактирование ТО' : 'Новая задача ТО';
            }
        },

        showMotorcycleSelect() {
            return this.motorcycles.length > 0 && !this.motorcycleId
        },

        motoForSelect() {
            return this.motorcycles.map(moto => ({
                value: moto.id,
                label: `${moto.brand} ${moto.model}`
            }))
        },

        apiEndpoints() {
            if (this.mode === 'task') {
                return this.isEditing ?
                    `/api/garage/maintenance/${this.editData.id}` :
                    '/api/garage/maintenance';
            } else {
                return this.isEditing ?
                    `/api/garage/maintenance/${this.editData.id}` :
                    '/api/garage/maintenance';
            }
        }
    },

    watch: {
        isOpen: {
            handler(newVal) {
                if (newVal) {
                    if (this.isEditing && this.editData) {
                        this.populateFormForEdit();
                    } else {
                        this.resetForm();
                        if (this.motorcycleId) {
                            this.formData.motorcycle_id = this.motorcycleId;
                        }
                    }
                }
            },
            immediate: true
        },

        mode() {
            if (this.isOpen) {
                this.resetForm();
            }
        }
    },

    methods: {
        getDefaultForm() {
            const baseForm = {
                motorcycle_id: null,
                title: '',
                description: '',
                notes: ''
            };

            if (this.mode === 'task') {
                return {
                    ...baseForm,
                    last_maintenance_date: null,
                    last_maintenance_mileage: null,
                    schedule_type: 'mileage',
                    interval_value: null,
                    interval_unit: 'months',
                    priority: 'medium',
                    is_recurring: true
                };
            } else {
                return {
                    ...baseForm,
                    completed_date: new Date().toISOString().split('T')[0],
                    mileage: null,
                    cost: null,
                    parts_used: '',
                    status: 'completed'
                };
            }
        },

        populateFormForEdit() {
            if (!this.editData) return;

            const baseData = {
                motorcycle_id: this.editData.motorcycle_id || this.motorcycleId,
                title: this.editData.title || '',
                description: this.editData.description || '',
                notes: this.editData.notes || ''
            };

            if (this.mode === 'task') {
                let lastMaintenanceDate = ''
                if (this.editData.last_maintenance_date) {
                    const date = new Date(this.editData.last_maintenance_date)
                    if (!isNaN(date.getTime())) {
                        lastMaintenanceDate = date.toISOString().split('T')[0]
                    }
                }

                this.formData = {
                    ...baseData,
                    last_maintenance_date: lastMaintenanceDate,
                    last_maintenance_mileage: this.editData.last_maintenance_mileage || null,
                    schedule_type: this.editData.schedule_type || 'mileage',
                    interval_value: this.editData.interval_value || null,
                    interval_unit: this.editData.interval_unit || 'months',
                    priority: this.editData.priority || 'medium',
                    is_recurring: this.editData.is_recurring !== undefined ? this.editData.is_recurring : true
                };
            } else {
                let completedDate = ''
                if (this.editData.completed_date) {
                    const date = new Date(this.editData.completed_date)
                    if (!isNaN(date.getTime())) {
                        completedDate = date.toISOString().split('T')[0]
                    }
                }

                this.formData = {
                    ...baseData,
                    completed_date: completedDate,
                    mileage: this.editData.mileage || null,
                    cost: this.editData.cost || null,
                    parts_used: this.editData.parts_used || '',
                    status: 'completed'
                };
            }
        },

        resetForm() {
            this.formData = this.getDefaultForm();
            if (this.motorcycleId) {
                this.formData.motorcycle_id = this.motorcycleId;
            }
        },

        handleClose() {
            this.resetForm()
            this.$emit('close')
        },

        async handleSubmit() {
            this.isSaving = true;

            try {
                const token = authService.getToken();
                const motorcycleId = this.formData.motorcycle_id || this.motorcycleId;
                
                if (!motorcycleId) {
                    alert('Не выбран мотоцикл');
                    this.isSaving = false;
                    return;
                }

                let dataToSend = {
                    ...this.formData,
                    motorcycle_id: motorcycleId,
                };

                if (this.mode === 'task') {
                    dataToSend = {
                        ...dataToSend,
                        last_maintenance_mileage: dataToSend.last_maintenance_mileage ? 
                            Number(dataToSend.last_maintenance_mileage) : null,
                        interval_value: dataToSend.interval_value ? 
                            Number(dataToSend.interval_value) : null
                    };
                } else {
                    dataToSend = {
                        ...dataToSend,
                        mileage: dataToSend.mileage ? Number(dataToSend.mileage) : null,
                        cost: dataToSend.cost ? Number(dataToSend.cost) : null
                    };
                }

                const response = await axios({
                    method: this.isEditing ? 'put' : 'post',
                    url: this.apiEndpoints,
                    data: dataToSend,
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                this.$emit('save', {
                    data: response.data,
                    mode: this.mode,
                    isEditing: this.isEditing
                });
                
                this.handleClose();
            } catch (error) {
                console.error('Ошибка сохранения задачи:', error);
                alert(error.response?.data?.error || 'Ошибка при сохранении задачи');
            } finally {
                this.isSaving = false;
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
    display: block;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 10px;
    gap: 8px;
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

.form-row label {
    display: block;
    font-weight: 500;
    color: var(--text);
    gap: 8px;
}

.form-row.radio {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
    font-weight: 500;
    color: var(--text);
    gap: 8px;
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

.modal-footer {
    padding: 20px 25px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
}

.form-row {
    display: flex;
    flex-direction: column;
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

.radio-group {
  display: flex;
  flex-direction: row !important;
  justify-content: space-around;
  gap: 20px;
  margin-top: 10px;
}

.motorcycle-badge {
    position: relative;
}

.motorcycle-badge label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
}

.motorcycle-badge i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    margin-right: 10px;
}

.motorcycle-badge {
    width: 100%;
    padding: 14px 15px 14px 45px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: var(--text);
    font-size: 1em;
    transition: all 0.3s ease;
}

.motorcycle-badge:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.2);
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