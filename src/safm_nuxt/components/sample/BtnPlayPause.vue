<template>
    <v-btn
        fab
        large
        :color="color"
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
            isPlaying: false
        }
    },

    computed: {
        color () {
            return this.isPlaying ? 'primary' : ''
        },

        icon () {
            return this.isPlaying ? 'mdi-pause' : 'mdi-play'
        }
    },

    mounted () {
        // On Sample Play event
        this.$nuxt.$on('samplePlay', (id) => {
            if (id == this.sampleId) {
                this.isPlaying = true
            }
        })

        // On Sample Pause event
        this.$nuxt.$on('samplePause', (id) => {
            if (id == this.sampleId) {
                this.isPlaying = false
            }
        })
    },

    methods: {
        click () {
            this.isPlaying = !this.isPlaying
            this.$nuxt.$emit('samplePlayPause', this.sampleId)
        }
    }
}
</script>
