<template>
    <v-card class="sample card">
        <v-card-title class="headline">{{ name }}</v-card-title>
        <div :id="`waveform-${id}`"></div>
        <v-card-text>
            <v-row align="center">
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${tempo}`"
                    >
                        <v-icon class="mx-2">mdi-metronome</v-icon>
                        {{ tempo }}
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${_key + mode}`"
                    >
                        <v-icon class="mx-2">mdi-music-circle-outline</v-icon>
                        {{ _key + mode }}
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${duration}`"
                    >
                        <v-icon class="mx-2">mdi-timer-outline</v-icon>
                        {{ duration + 's' }}
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-text>
            <v-chip
                v-for="tag in tags"
                :key="tag.id"
                class="tag ma-1"
                label
                small
                :to="`/quick-search/${tag.name}`"
            >
                {{ tag.name }}
            </v-chip>
        </v-card-text>
        <v-card-text>
            By
            <v-btn
                text
                small
                :to="`/profiles/${username}`"
                class="pa-0"
            >
                {{ username }}
            </v-btn>
        </v-card-text>
        <v-card-actions>
            <v-row align="center">
                <v-col cols="4" align="center">
                    <v-btn
                        @click="playPause"
                        fab
                        large
                        class="sample-playpause"
                    >
                        <v-icon>{{ playPauseIcon }}</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4" align="center">
                    <v-btn
                        :href="`${$axios.defaults.baseURL}/sample_file/${id}`"
                        fab
                        large
                        class="sample-download"
                    >
                        <v-icon>mdi-download-outline</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4" align="center">
                    <v-btn
                        :to="`/samples/${id}`"
                        fab
                        large
                        class="sample-detail"
                    >
                        <v-icon>mdi-eye-outline</v-icon>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-actions>
    </v-card>
</template>

<script>
if (process.browser) {
    var WaveSurfer = require('wavesurfer.js')
}

export default {
    props: [
        'id',
        'name',
        'tempo',
        '_key',
        '_mode',
        'duration',
        'tags',
        'username'
    ],

    data () {
        return {
            wavesurfer: null
        }
    },

    computed: {
        mode () {
            return this._mode == 'min' ? 'm' : this._mode == 'maj' ? 'M' : ''
        },

        playPauseIcon () {
            if (this.wavesurfer) {
                return this.wavesurfer.isPlaying() ? 'mdi-pause' : 'mdi-play'
            }
        }
    },

    mounted () {
        this.initWaveSurfer()
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
            let audioFileUrl = `${this.$axios.defaults.baseURL}/sample_file/${this.id}`
            this.wavesurfer.load(audioFileUrl)

            // Repeats the audio file if the repeatSample property is true
            this.wavesurfer.on('finish', () => {
                if (this.$store.state.repeatSample) {
                    this.wavesurfer.play()
                }
            })
        },

        playPause () {
            this.wavesurfer.playPause()
        }
    }
}
</script>
