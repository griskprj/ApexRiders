<template>
    <div class="form-group" :class="withIcon ? 'input-with-icon' : ''">
        <label :for="id">{{ label }}</label>
        
        <div v-if="withIcon" class="input-with-icon">
            <i class="fas " :class="icon"></i>
            <input
                :id="id"
                :type="type"
                :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)"
                :required="required"
                :min="min"
                :max="max"
                class="form-input"
            />
        </div>
        <div v-if="!withIcon">
            <input  
                :id="id"
                :type="type"
                :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)"
                :required="required"
                :min="min"
                :max="max"
                class="form-input"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'BaseInput',
    props: {
        modelValue: [String, Number, Boolean],
        type: {
            type: String,
            default: 'text'
        },
        label: {
            type: String,
            required: true
        },
        id: {
            type: String,
            required: true
        },
        required: {
            type: Boolean,
            default: false
        },
        min: {
            type: Number,
            default: null
        },
        max: {
            type: Number,
            default: null
        },
        withIcon: {
            type: Boolean,
            default: false
        },
        icon: {
            type: String,
            default: ''
        }
    },

    emits: ['update:modelValue'],

    computed: {
        value: {
            get() { return modelValue },
            set(value) { this.$emit('update:modelValue', value) }
        }
    }
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

.input-with-icon {
    position: relative;
}

.input-with-icon i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    margin-right: 10px;
}

.form-input {
    width: 100%;
    padding: 14px 15px 14px 45px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: var(--text);
    font-size: 1em;
    transition: all 0.3s ease;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.2);
}
</style>