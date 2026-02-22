<template>
    <div class="form-group">
        <label>{{ label }}</label>
        <select v-model="item_id" v-on:change="chandeHandle" required>
            <option v-for="item in items" :key="item.id" :value="item.id">
                {{ item.brand }} {{ item.model }}
            </option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'BasicSelect',

    props: {
        label: String,
        items: Array
    },

    emits: ['change'],

    data() {
        return {
            item_id: Number
        }
    },
    
    methods: {
        chandeHandle() {
            this.$emit('change', this.item_id)
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

.form-group select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group select:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}
</style>