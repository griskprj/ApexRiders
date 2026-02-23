<template>
    <div class="form-group">
        <label v-if="label">{{ label }}</label>

        <div :class="{ 'with-icon': withIcon }">
            <i v-if="withIcon" class="fas " :class="icon"></i>
            <select 
                :value="selectedId"
                @change="handleChange"
                v-bind="$attrs"
            >
                <option
                    v-for="item in normalizeItems" 
                    :key="item.value" 
                    :value="item.value"
                >
                    {{ item.label }}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BasicSelect',
    inheritAttrs: false,

    props: {
        modelValue: [String, Number],
        label: String,
        items: {
            type: Array,
            required: true,
        },
        withIcon: Boolean,
        icon: String,
    },

    emits: ['update:modelValue'],
    computed: {
        normalizeItems() {
            return this.items.map(item => {
                if (typeof item === 'string') {
                    return {
                        value: item,
                        label: item
                    }
                }
                return {
                    value: item.value ?? item.id,
                    label: item.label ?? item.name ?? String(item.value ?? item.id)
                }
            })
        }
    },

    methods: {
        handleChange(event) {
            this.$emit('update:modelValue', event.target.value)
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

.form-group select {
    width: 100%;
    padding: 14px 15px 14px 45px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: var(--text);
    font-size: 1em;
    transition: all 0.3s ease;
}

.form-group select:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.2);
}

.with-icon {
    position: relative;
}

.with-icon i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    margin-right: 10px;
}
</style>