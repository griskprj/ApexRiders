<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-tachometer-alt"></i> Изменение пробега</h3>
            </div>
            <form @submit.prevent="handleSubmit" class="modal-form">
                <div class="form-row">
                    <BaseInput
                        id="mileage"
                        type="number"
                        :label="`Текущий пробег: ${motorcycle.current_mileage || 0} км`"
                        min="0"
                        :withIcon="true"
                        icon="fa-road"
                        v-model="form.newMileage"
                        required
                    />
                </div>
                <div class="modal-actions">
                    <BaseButton
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
                        Сохранить
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

export default {
    name: 'UpdateMileageModal',

    components: {
        BaseButton,
        BaseInput
    },

    props: {
        motorcycle: {
            type: Object,
            default: null
        },
        isOpen: {
            type: Boolean,
            default: false
        }
    },

    emits: ['close', 'save'],

    data() {
        return {
            isSaving: false,
            form: {
                newMileage: null
            }
        }
    },

    methods: {
        handleClose() {
            this.resetForm();
            this.$emit('close');
        },

        resetForm() {
            this.form = {
                newMileage: null
            };
        },

        async handleSubmit() {
            this.isSaving = true;

            try {
                const token = authService.getToken();

                await axios.put(
                    `/api/motorcycle/${this.motorcycle.id}/mileage`,
                    { mileage: this.form.newMileage },
                    { headers: { 'Authorization': `Bearer ${token}` } }
                );

                this.$emit('save', this.form.newMileage);
                this.handleClose();
            } catch (error) {
                console.error('Ошибка обновления пробега: ', error);
                alert('Ошибка при обновлении пробега');
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
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
}

.modal-actions {
    display: flex;
    justify-content: space-evenly;
    gap: 15px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-actions button {
    width: 100%;
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
    .modal-header {
        flex-direction: column;
    }
    .modal-actions {
        flex-direction: column;
    }
}
</style>