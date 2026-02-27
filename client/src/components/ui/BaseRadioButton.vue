<template>
    <div class="radio-group">
        <label class="radio-label">
            <input 
                type="radio"
                :name="name"
                :value="value"
                :checked="modelValue === value" 
                @change="$emit('update:modelValue', value)"
            />
            <span class="radio-custom"></span> 
            {{ label }}
        </label>
    </div>
</template>

<script>
/** 
 * Компонент BaseRadioButton
 * @description Стандартный тип radio.
 * 
 * @component
 * @version 1.0.0
 * @example
 * 
 * <BaseRadioButton
 *     name="schedule_type"
 *     value="mileage"
 *     label="По пробегу"
 *     v-model="taskForm.schedule_type"
 * />
 * 
 * @emits update:ModelValue - Срабатывает после изменения выбора.
 * 
*/

export default {
    name: 'BaseRadioButton',

    props:{
        /** Значение выбора */
        value: {
            type: [String, Number, Boolean],
            required: true
        },
        /** Label кнопки */
        label: {
            type: String,
            default: ''
        },
        /** Значение */
        name: {
            type: String,
            required: true
        },
        /** Передаваемое значение */
        modelValue: {
            type: [String, Number, Boolean],
            default: null
        }
    },

    emits: ['update:modelValue'],
}
</script>

<style scoped>
.radio-group {
  display: flex;
  flex-direction: row !important;
  justify-content: space-around;
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
</style>