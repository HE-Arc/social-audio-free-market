<template>
    <div>
        <v-row>
            <v-col
                cols="8"
            >
                <div :id="`waveform-${sample.id}`"></div>
            </v-col>
            <v-col
                cols="4"
            >
                <div>HELLO</div>
            </v-col>
        </v-row>
        <Comments :comments="comments" />
    </div>
</template>

<script>
if (process.browser) {
    var WaveSurfer = require('wavesurfer.js')
}
import Comments from '~/components/Comments.vue'

export default {
    components: {
        Comments
    },

    data () {
        return {
            wavesurfer: null,
            sample: [],
            comments: []
        }
    },

    mounted () {
        this.initWaveSurfer()
    },

    async asyncData({ $axios, params }) {
        try {
            let sample = await $axios.$get(`/sample/${params.id}`)

            // THIS IS TEMPORARY ; WILL BE DEVELOPED LATER
            let comments = [
                {
                    id: 1,
                    username: 'Len Faki',
                    text: 'Aliquip laborum dolor ex ut ut qui ipsum. Ullamco tempor deserunt incididunt veniam. Pariatur veniam ad tempor sit. Ipsum dolore pariatur aliqua veniam eu est.',
                    datetime: '26.04.2020 14:30'
                },
                {
                    id: 2,
                    username: 'Solomun',
                    text: 'Amet dolor laboris ea ad mollit elit nulla aliquip. Occaecat consectetur commodo culpa excepteur consectetur occaecat. Ullamco culpa occaecat cillum ipsum deserunt culpa reprehenderit. Occaecat pariatur et reprehenderit eu labore nisi non consequat ipsum nisi tempor ullamco fugiat Lorem. Ut Lorem qui id eu velit id ut fugiat sit cupidatat. Sunt voluptate ex voluptate cillum proident magna.',
                    datetime: '26.04.2020 14:43'
                }
            ]
            return { sample, comments }
        } catch (e) {
            return { sample: [], comments: [] }
        }
    },

    methods: {
        initWaveSurfer () {
            this.wavesurfer = WaveSurfer.create({
                container: `#waveform-${this.sample.id}`,
                waveColor: 'violet',
                progressColor: 'purple',
                barWidth: 2,
                barHeight: 1,
                barGap: null
            })

            // Loads the sample audio file
            let audioFileUrl = `${this.$axios.defaults.baseURL}/sample_file/${this.sample.id}`
            this.wavesurfer.load(audioFileUrl)

            // Repeats the audio file if the repeatSample property is true
            this.wavesurfer.on('finish', () => {
                if (this.$store.state.repeatSample) {
                    this.wavesurfer.play()
                }
            })
        }
    }
}
</script>
