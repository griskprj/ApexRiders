<template>
    <!-- Модальное окно добавления записи в историю -->
    <div v-if="isOpen" class="modal-overlay" @click="handleClose">
        <div class="modal">
            <input v-model="form.status" value="completed" type="hidden">
            <div class="modal-header">
                <h3><i class="fas fa-history"></i>{{ isEditing ? 'Редактировать запись' : 'Добавить запись в историю' }}</h3>
                <BaseButton
                    variant="outline"
                    @click="handleClose"
                >
                    <div class="fas fa-times"></div>
                </BaseButton>
            </div>
            <form @submit.prevent="handleSubmit" class="modal-form">
                <div class="form-row">
                    <BaseInput
                        id="title"
                        type="text"
                        label="Название работы *"
                        v-model="form.title"
                        max="64"
                        required
                        :withIcon="true"
                        icon="fa-heading"
                    />
                </div>

                <div class="form-row">
                    <BaseTextarea
                        label="Описание"
                        :resize="false"
                        v-model="form.description"
                    />
                </div>
                
                <div class="form-row">
                    <BaseInput
                        id="completed_date"
                        type="date"
                        label="Дата выполнения *"
                        :withIcon="true"
                        icon="fa-calendar"
                        v-model="form.completed_date"
                    />
                </div>

                <div class="form-row">
                    <BaseInput
                        id="current_mileage"
                        type="text"
                        label="Пробег при выполнении *"
                        v-model="form.mileage"
                        min="1"
                        :max="motorcycle.current_mileage"
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
                        v-model="form.cost"
                        max="10000000"
                        :withIcon="true"
                        icon="fa-ruble-sign"
                    />
                </div>

                <div class="form-row">
                    <BasicSelect
                        label="Тип работы"
                        :items="[
                            { value: 'regular', label: 'Регламентное ТО'},
                            { value: 'repair', label: 'Ремонт'},
                            { value: 'upgrade', label: 'Тюнинг/Улучшение'},
                            { value: 'diagnostics', label: 'Диагностика'},
                            { value: 'other', label: 'Другое'}
                        ]"
                        :with-icon="true"
                        icon="fa-tools"
                        v-model="form.maintenance_type"
                    />
                </div>

                <div class="form-row">
                    <BaseTextarea
                        label="Использованные запчасти (через запятую)"
                        :resize="false"
                        v-model="form.parts_used"
                    />
                </div>
                
                <div class="form-row">
                    <BaseTextarea
                        label="Дополнительные заметки"
                        :resize="false"
                        v-model="form.notes"
                    />
                </div>
            </form>

            <div class="modal-footer">
                <BaseButton
                    variant="outline"
                    :disabled="isLoading"
                    @click="handleClose"
                >
                    Отмена
                </BaseButton>
                <BaseButton
                    variant="outline"
                    :disabled="!form.title"
                    :isLoading="isLoading"
                    @click="handleClose"
                >
                    Сохранить в историю
                </BaseButton>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { authService } from '../../../utils/checkAuth';
import BaseButton from '../../ui/BaseButton.vue';
import BaseInput from '../../ui/BaseInput.vue';
import BaseTextarea from '../../ui/BaseTextarea.vue';
import BasicSelect from '../../ui/BasicSelect.vue';

export default {
    name: 'AddHistoryModal',

    components: {
        BaseButton,
        BaseInput,
        BaseTextarea,
        BasicSelect
    },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        isEditing: {
            type: Boolean,
            default: false
        },
        editData: {
            type: Object,
            default: null
        },
        currentMileage: {
            type: Number,
            default: 0
        },
        taskId: {
            type: [Number, String],
            required: true
        },
    },

    emits: ['close', 'create', 'update'],

    data() {
        return {
            isLoading: false,
            form: {
                moto_id: null,
                title: '',
                description: '',
                completed_date: new Date().toISOString().split('T')[0],
                mileage: null,
                cost: null,
                maintenance_type: 'regular',
                parts_used: '',
                notes: '',
                status: 'completed'
            }
        }
    },

    watch: {
        isOpen: {
            handler(newVal) {
                if (this.isEditing && this.editData) {
                    this.populateFormForEdit();
                } else {
                    if (this.taskId) {
                        this.form.moto_id = this.taskId;
                    }
                }
            },
            immediate: true
        },

        editData: {
            handler(newVal) {
                if (this.isOpen && this.isEditing && newVal) {
                    this.populateFormForEdit();
                }
            },
            deep: true
        }
    },

    methods: {
        populateFormForEdit() {
            if (!this.editData) return;

            if (this.editData.completed_date) {
                const date = new Date(this.editData.completed_date);
                if (!isNaN(date.getTime())) {
                    completedDate = date.toISOString().split('T')[0];
                }
            };

            this.form = {
                moto_id: this.editData.moto_id || this.taskId,
                title: this.editData.title,
                description: this.editData.description,
                completed_date: this.editData.completed_date,
                mileage: this.editData.mileage || null,
                cost: this.editData.cost || null,
                maintenance_type: this.editData.maintenance_type || 'regular',
                parts_used: this.editData.parts_used || '',
                notes: this.editData.notes || '',
                status: 'completed'
            };
        },

        handleClose() {
            this.resetForm();
            this.$emit('close');
        },

        resetForm() {
            this.form = {
                moto_id: this.taskId,
                title: '',
                description: '',
                completed_date: null,
                mileage: null,
                cost: null,
                maintenance_type: 'regular',
                parts_used: '',
                notes: '',
                status: 'completed'
            };
        },

        async handleSubmit() {
            this.isLoading = true;

            try {
                const token = authService.getToken();

                const taskId = this.form.taskId || this.taskId;

                if (!taskId) {
                    alert('Задача не выбрана');
                    this.isLoading = false;
                    return;
                };

                const dataToSend = {
                    ...this.form,
                    task_id: taskId
                };

                let response;
                if (this.isEditing && this.editData?.id) {
                    response = await axios.put(
                        `/api/garage/maintenance/${this.editData.id}`,
                        dataToSend,
                        { headers: { 'Authorization': `Bearer ${token}` } }
                    );
                    this.$emit('update', response.data);
                } else {
                    response = await axios.post('/api/garage/maintenance', dataToSend, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    this.$emit('create', response.data);
                }

                this.handleClose();
            } catch (error) {
                console.error('Ошибка сохраниения задачи в историю:', error);
                alert(error.response?.data?.error || 'Ошибка при сохранении задачи');
            } finally {
                this.isLoading = false;
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