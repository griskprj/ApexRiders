<template>
    <div class="form-group">
        <label v-if="label">{{ label }}</label>
        <textarea
            :value="modelValue"
            @input="handleInput"
            :class="{ 'no-resize': !resize }"
            v-bind="$attrs"
            rows="3"
        ></textarea>
    </div>
</template>

<script>
/** 
 * Компонент BaseTextarea
 * @description Стандартный тип textaera.
 * 
 * @component
 * @version 1.0.0
 * @example
 * 
 * <BaseTextarea
 *     label="Заметки"
 *     :resize="false"
 *     v-model="taskForm.notes"
 * />
 * 
 * @emits update:ModelValue - Срабатывает после изменения текста.
 * 
*/


export default {
    name: 'BaseTextarea',
    inheritAttrs: false,

    props: {
        /** Передаваемое значение */
        modelValue: {
            type: String,
            default: ''
        },
        /** Label textaera */
        label: {
            type: String,
            default: ''
        },
        /** Изменение размера */
        resize: {
            type: Boolean,
            default: true
        }
    },

    emits: ['update:modelValue'],
    
    methods: {
        handleInput(event) {
            this.$emit('update:modelValue', event.target.value)
        }
    }
}
</script>

<style scoped>
.no-resize {
    resize: none;
}

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

.form-group textarea {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group textarea:focus {
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
</style>