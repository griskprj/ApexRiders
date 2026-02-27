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
export default {
    name: 'BaseButton',
    props: {
        type: {
            type: String,
            default: 'button' // 'button', 'submit', 'reset'
        },
        variant: {
            type: String,
            default: 'primary' // 'primary', 'outline', 'danger'
        },
        disabled: {
            type: Boolean,
            default: false
        },
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