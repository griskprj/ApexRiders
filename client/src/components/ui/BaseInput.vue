<template>
    <div class="form-group">
        <label :for="id">{{ label }}</label>
        <input
            :id="id"
            :type="type"
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            :required="required"
            :min="min"
            :max="max"
        />
    </div>
</template>

<script>
export default {
    name: 'BaseInput',
    props: {
        modelValue: [String, Number],
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
        }
    },

    emits: ['update:modelValue']
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
</style>