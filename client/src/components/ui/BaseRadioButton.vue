<template>
    <label>Тип расписания</label>
    <div class="radio-group">
        <label class="radio-label">
            <input type="radio" value="mileage" v-model="optionCl"/>
            <span class="radio-custom"></span> {{ label }}
        </label>
    </div>
</template>

<script>
export default {
    name: 'BaseRadioButton',

    props:{
        option: String,
        label: String
    },

    emits: ['change'],

    data() {
        return {
            optionCl: String
        }
    },

    methods: {
        handleChange (option) {
            this.$emit('change', option)
        }
    }
}
</script>