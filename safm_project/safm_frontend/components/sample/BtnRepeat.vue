<template>
    <v-btn
        large
        :color="repeat ? 'accent' : ''"
        @click="click"
    >
        <v-icon>{{ icon }}</v-icon>
    </v-btn>
</template>

<script>
export default {
    props: ['sampleId'],

    data () {
        return {
            repeat: false
        }
    },

    computed: {
        icon () {
            return this.repeat ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
        click () {
            this.repeat = !this.repeat
            this.$nuxt.$emit('sampleRepeat', this.sampleId)
        }
    }
}
</script>
