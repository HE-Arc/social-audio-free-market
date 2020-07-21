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
            isPlaying: false,
            repeat: false
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
            if (id == this.sampleId && !this.repeat) {
                this.isPlaying = false
            }
        })

        // On Sample Repeat event
        this.$nuxt.$on('sampleRepeat', (sampleId) => {
            if (this.sampleId == sampleId) {
                this.repeat = !this.repeat
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
