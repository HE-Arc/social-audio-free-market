<template>
    <v-card class="sample card">
        <v-card-title class="headline">
            <nuxt-link :to="`/samples/${id}`">{{ name }}</nuxt-link>
        </v-card-title>
        <WaveForm
            ref="waveform"
            :id="id"
            @onPlay="onPlay"
            @onPause="onPause"
            @onFinish="onFinish"
        />
        <v-card-text>
            <v-row align="center">
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${tempo}`"
                    >
                        <v-icon>mdi-metronome</v-icon>
                        {{ tempo }}
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${duration}`"
                    >
                        <v-icon>mdi-timer-outline</v-icon>
                        {{ duration + 's' }}
                    </v-btn>
                </v-col>
                <v-col cols="4" v-if="_key || mode">
                    <v-btn
                        text
                        small
                        :to="`/quick-search/${_key + mode}`"
                    >
                        <v-icon>mdi-music-circle-outline</v-icon>
                        {{ _key + mode }}
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-text>
            <v-chip
                v-for="tag in tags"
                :key="tag.id"
                class="tag mx-1"
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
                        fab
                        large
                        :color="playPauseColor"
                        @click="playPause"
                    >
                        <v-icon>{{ playPauseIcon }}</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4" align="center">
                    <v-btn
                        fab
                        large
                        :color="repeatSample ? 'accent' : ''"
                        @click="repeatSample = !repeatSample"
                    >
                        <v-icon>{{ repeatSampleIcon }}</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4" align="center">
                    <v-btn
                        :href="`${$axios.defaults.baseURL}/sample_file/${id}`"
                        fab
                        large
                    >
                        <v-icon>mdi-download-outline</v-icon>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-actions>
    </v-card>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'

export default {
    components: {
        WaveForm
    },

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
            isPlaying: false,
            repeatSample: false
        }
    },

    computed: {
        mode () {
            return this._mode == 'min' ? 'm' : this._mode == 'maj' ? 'M' : ''
        },

        playPauseIcon () {
            return this.isPlaying ? 'mdi-pause' : 'mdi-play'
        },

        playPauseColor () {
            return this.isPlaying ? 'primary' : ''
        },

        repeatSampleIcon () {
            return this.repeatSample ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
        playPause () {
            this.$refs.waveform.playPause()
        },

        onPlay () {
            this.isPlaying = true
            this.$nuxt.$emit('samplePlay')
        },

        onPause () {
            this.isPlaying = false
            this.$nuxt.$emit('sampleStop')
        },

        onFinish () {
            if (this.repeatSample) {
                this.$refs.waveform.play()
            } else {
                this.isPlaying = false
                this.$nuxt.$emit('sampleStop')
            }
        }
    }
}
</script>
