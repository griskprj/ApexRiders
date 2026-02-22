<template>
    <div class="form-group">
        <label>{{ label }}</label>
        <textarea 
            class="form-input"
            :class="resize ? 'no-resize' : ''" 
            v-model="content" 
            rows="3"
            v-on:change="handleChange"
        ></textarea>
    </div>
</template>

<script>
export default {
    name: 'BaseTextarea',

    props: {
        label: String,
        resize: Boolean
    },

    data() {
        content: String
    },

    emits: ['change'],

    methods: {
        handleChange(content) {
            this.$emit('change', content)
        }
    }
}
</script>

<style scoped>
.no-resize {
    resize: none;
}
</style>