<template>
    <div v-if="isOpen" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Удаление мотоцикла</h3>
                <BaseButton
                    variant="outline"
                    @click="handleClose"
                >
                    <i class="fas fa-times"></i>
                </BaseButton>
            </div>

            <form class="modal-form">
                <h3 class="form-subtitle">Вы уверены, что хотите удалить мотоцикл?</h3>
                <p class="form-description">Отменить это действией невозможно</p>
                <div class="form-row">
                    <BaseButton
                        variant="outline"
                        :disabled="isDeleting"
                        @click="handleClose"
                    >
                        Отмена
                    </BaseButton>
                    <BaseButton
                        variant="primary"
                        :loading="isDeleting"
                        @click="deleteMoto"
                    >
                        Удалить
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

export default {
    name: 'DeleteMotoModal',

    components: {
        BaseButton
    },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        motoToDeleteId: {
            type: Number,
            default: null
        }
    },

    emits: ['close', 'delete'],

    data() {
        return {
            isDeleting: false,
            motorcycleId: null
        }
    },

    watch: {
        motoToDeleteId: {
            handler(newValue) {
                if (newValue) {
                    this.motoId = newValue
                    console.log('Moto ID to delete:', this.motoId)
                } else {
                    this.resetMoto()
                }
            },
            immediate: true,
        }
    },

    methods: {
        handleClose() {
            this.resetMoto()
            this.$emit('close')
        },

        resetMoto() {
            this.motorcycle = {
                id: null
            }
        },

        async deleteMoto() {
            this.isDeleting = true

            try {
                const token = authService.getToken()
                
                await axios.delete(`/api/motorcycle/${this.motoId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })

                alert('Мотоцикл успешно удален!')
                this.$emit('delete')
                this.handleClose()
            } catch (error) {
                console.error('Ошибка удаления мотоцикла:', error)
                this.handleClose()
            } finally {
                this.isDeleting = false
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

.form-subtitle {
    text-align: center;
    color: var(--primary);
    margin-bottom: 10px;
}

.form-description {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: 35px;
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
    flex-direction: column;
    gap: 20px;
    margin-bottom: 20px;
    align-items: stretch;
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