<template>
    <div :id="`waveform-${id}`"></div>
</template>

<script>
if (process.browser) {
    var WaveSurfer = require('wavesurfer.js')
}

export default {
    props: [
        'id',
        'height'
    ],

    data () {
        return {
            wavesurfer: null,
            repeat: false
        }
    },

    mounted () {
        // Inits the wavesurfer element
        this.initWaveSurfer()

        // On Play Pause Click event
        this.$nuxt.$on('samplePlayPause', (sampleId) => {
            if (this.id == sampleId) {
                this.wavesurfer.playPause()
            }
        })

        // On Sample Repeat event
        this.$nuxt.$on('sampleRepeat', (sampleId) => {
            if (this.id == sampleId) {
                this.repeat = !this.repeat
            }
        })

        // On Stop All event
        this.$nuxt.$on('sampleStopAll', () => {
            this.wavesurfer.pause()
        })
    },

    methods: {
        // Inits the wavesurfer element
        initWaveSurfer () {
            // New wavesurfer instance
            this.wavesurfer = WaveSurfer.create({
                container: `#waveform-${this.id}`,
                waveColor: 'violet',
                progressColor: 'purple',
                barWidth: 2,
                barHeight: 1,
                barGap: null,
                height: this.height ? this.height : 128
            })

            // Loads the sample audio file into the wavesurfer instance
            const audioFileUrl = `${this.$axios.defaults.baseURL}/sample/file/${this.id}/0`
            this.wavesurfer.load(audioFileUrl)

            // On wavesurfer play event
            this.wavesurfer.on('play', () => {
                this.$nuxt.$emit('samplePlay', this.id)
            })

            // On wavesurfer pause event
            this.wavesurfer.on('pause', () => {
                this.$nuxt.$emit('samplePause', this.id)
            })

            // On wavesurfer finish event
            this.wavesurfer.on('finish', () => {
                if (this.repeat) {
                    // Replays the audio file if the repeat is enabled
                    this.wavesurfer.play()
                }
            })
        }
    }
}
</script>
