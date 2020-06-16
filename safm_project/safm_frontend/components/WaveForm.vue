<template>
    <div :id="`waveform-${id}`"></div>
</template>

<script>
if (process.browser) {
    var WaveSurfer = require('wavesurfer.js')
}

export default {
    props: [
        'id'
    ],

    data () {
        return {
            wavesurfer: null
        }
    },

    mounted () {
        this.initWaveSurfer()

        // On Stop All event
        this.$nuxt.$on('stopAll', () => {
            this.wavesurfer.pause()
        })
    },

    methods: {
        initWaveSurfer () {
            this.wavesurfer = WaveSurfer.create({
                container: `#waveform-${this.id}`,
                waveColor: 'violet',
                progressColor: 'purple',
                barWidth: 2,
                barHeight: 1,
                barGap: null
            })

            // Loads the sample audio file
            let audioFileUrl = `${this.$axios.defaults.baseURL}/sample_file/${this.id}/0`
            this.wavesurfer.load(audioFileUrl)

            // On play event
            this.wavesurfer.on('play', () => {
                this.$emit('onPlay')
            })

            // On pause event
            this.wavesurfer.on('pause', () => {
                this.$emit('onPause')
            })

            // On finish event
            this.wavesurfer.on('finish', () => {
                this.$emit('onFinish')
            })
        },

        play () {
            this.wavesurfer.play()
        },

        playPause () {
            this.wavesurfer.playPause()
        }
    }
}
</script>
