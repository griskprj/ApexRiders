<template>
    <button 
        :type="type" 
        class="btn"
        :class="[`btn-${variant}`]"
        :disabled="disabled || loading"
        @click="$emit('click')"
    >
        <span v-if="loading" class="btn-spinner">
            <i class="fas fa-spinner fa-spin"></i>
        </span>

        <span v-else>
            <slot></slot>
        </span>
    </button>
</template>

<script>
/** 
 * Компонент BaseButton
 * @description Стандартный тип button.
 * 
 * @component
 * @version 1.0.0
 * @example
 * 
 * <BaseInput
 *     id="interval_value"
 *     type="number"
 *     label="Интервал (км) *"
 *     min="1"
 *     :withIcon="true"
 *     icon="fa-tachometer"
 *     v-model="taskForm.interval_value"
 *     :required="taskForm.schedule_type === 'mileage'"
 * />
 * 
 * @emits click - Срабатывает после нажатия на кнопку.
 * 
*/
export default {
    name: 'BaseButton',
    props: {
        /** Тип кнопки */
        type: {
            type: String,
            default: 'button' // 'button', 'submit', 'reset'
        },
        /** Тип внешнего вида кнопки */
        variant: {
            type: String,
            default: 'primary' // 'primary', 'outline', 'danger'
        },
        /** Деактивированная кнопка */
        disabled: {
            type: Boolean,
            default: false
        },
        /** Загрузка */
        loading: {
            type: Boolean,
            default: false
        }
    },

    emits: ['click']
}
</script>

<style scoped>
/* Small button */
:deep(.btn-small) {
    padding: 8px 20px;
    font-size: 0.9rem;
    white-space: nowrap;
}
</style>