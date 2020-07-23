<template>
    <v-btn
        fab
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
        // On button click
        click () {
            // Toggles repeat
            this.repeat = !this.repeat
            this.$nuxt.$emit('sampleRepeat', this.sampleId)
        }
    }
}
</script>
