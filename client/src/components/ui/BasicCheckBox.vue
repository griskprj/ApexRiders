<template>
    <div class="form-group">
        <label v-if="label">
            <i v-if="withIcon" class="fas" :class="icon"></i>
            {{ label }}
        </label>
        
        <label class="checkbox-label">
            <input 
                type="checkbox"
                :checked="modelValue" 
                @change="handleChange"
            >
            <span class="checkbox-custom"></span>
            {{ text }}
        </label>
    </div>
</template>

<script>
/** 
 * Компонент BasicCheckBox
 * @description Стандартный тип checkbox.
 * 
 * @component
 * @version 1.0.0
 * @example
 * 
 * <BasicCheckBox
 *     label="Повторяющаяся задача"
 *     text="Это повторяющаяся задача?"
 *     v-model="taskForm.is_recurring"
 * /> 
 * 
 * @emits update:ModelValue - Срабатывает после изменения выбора.
 * 
*/

export default {
    name: 'BasicCheckBox',

    props: {
        /** Передаваемое значение */
        modelValue: {
            type: Boolean,
            default: false
        },
        /** Label чек-бокса */
        label: {
            type: String,
            default: ''
        },
        /** Текст чек-бокса */
        text: {
            type: String,
            default: ''
        },
        /** Есть иконка */
        withIcon: {
            type: Boolean,
            default: false
        },
        /** Иконка */
        icon: {
            type: String,
            default: ''
        },
    },

    emits: ['update:modelValue'],

    methods: {
        handleChange(event) {
            this.$emit('update:modelValue', event.target.checked)
        }
    },
}
</script>

<style scoped>
.form-group {
   margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
}

.checkbox-group {
    margin-top: 10px;
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
</style>