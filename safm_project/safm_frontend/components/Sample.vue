<template>
    <v-card class="sample card">
        <v-card-title>{{ sample.name }}</v-card-title>
        <v-card-text>
            <v-btn
                text
                small
                :to="`/profiles/${sample.user.id}`"
            >
                {{ sample.user.username }}
            </v-btn>
        </v-card-text>
        <v-card-text>
            <v-row align="center">
                <v-col cols="4">
                    <v-icon>mdi-metronome</v-icon>
                    {{ sample.tempo }}
                </v-col>
                <v-col cols="4">
                    <v-icon>mdi-music-circle-outline</v-icon>
                    {{ sample.tone + sample.mode }}
                </v-col>
                <v-col cols="4">
                    <v-icon>mdi-timer-outline</v-icon>
                    {{ sample.duration + 's' }}
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
                outlined
            >
                {{ tag.name }}
            </v-chip>
        </v-card-text>
        <v-card-actions>
            <v-row align="center">
                <v-col cols="4">
                    <v-btn
                        @click="playPauseSample"
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
        <audio :id="`audio-${sample.id}`">
            <source :src="`${$axios.defaults.baseURL}/sample_file/${sample.id}`" />
            Your browser does not support the audio element.
        </audio>
    </v-card>
</template>

<script>
export default {
    props: ['sample'],

    data () {
        return {
            playing: false
        }
    },

    computed: {
        playPauseIcon () {
            return this.playing ? 'mdi-pause' : 'mdi-play'
        }
    },

    methods: {
        playPauseSample () {
            let audio = document.getElementById('audio-' + this.sample.id)

            if (audio.paused) {
                audio.play()
                this.playing = true
            } else {
                audio.pause()
                this.playing = false
            }
        }
    }
}
</script>
