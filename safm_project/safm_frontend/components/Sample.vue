<template>
    <v-card class="sample card">
        <v-card-title>{{ sample.name }}</v-card-title>
        <v-card-text>
            <v-btn
                text
                small
                :to="`/profiles/${sample.user.username}`"
            >
                {{ sample.user.username }}
            </v-btn>
        </v-card-text>
        <div :id="`waveform-${sample.id}`"></div>
        <v-card-text>
            <v-row align="center">
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${sample.tempo}`"
                    >
                        <v-icon>mdi-metronome</v-icon>
                        {{ sample.tempo }}
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${sample.key + sample.mode}`"
                    >
                        <v-icon>mdi-music-circle-outline</v-icon>
                        {{ sample.key + sample.mode }}
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${sample.duration}`"
                    >
                        <v-icon>mdi-timer-outline</v-icon>
                        {{ sample.duration + 's' }}
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-text>
            <v-chip
                v-for="tag in sample.tags"
                :key="tag.id"
                class="tag ma-1"
                label
                small
                :to="`/quick-search/${tag.name}`"
            >
                {{ tag.name }}
            </v-chip>
        </v-card-text>
        <v-card-actions>
            <v-row align="center">
                <v-col cols="4">
                    <v-btn
                        @click="playPause"
                        block>
                        <v-icon>{{ playPauseIcon }}</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        :href="`${$axios.defaults.baseURL}/sample_file/${sample.id}`"
                        block>
                        <v-icon>mdi-download-outline</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        :to="`/samples/${sample.id}`"
                        block>
                        <v-icon>mdi-eye-outline</v-icon>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-actions>
    </v-card>
</template>

<script>
export default {
    props: ['sample'],

    data () {
        return {
            wavesurfer: null
        }
    },

    computed: {
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
                container: `#waveform-${this.sample.id}`,
                waveColor: 'violet',
                progressColor: 'purple',
                barWidth: 2,
                barHeight: 1,
                barGap: null
            })

            let audioFileUrl = `${this.$axios.defaults.baseURL}/sample_file/${this.sample.id}`
            this.wavesurfer.load(audioFileUrl)
        },

        playPause () {
            this.wavesurfer.playPause()
        }
    }
}
</script>
