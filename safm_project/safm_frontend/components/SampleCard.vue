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
            <div class="d-flex justify-space-around">
                <v-btn
                    text
                    small
                    :to="`/quick-search/${tempo}`"
                >
                    <v-icon>mdi-metronome</v-icon>
                    <span class="mx-1">{{ tempo }}</span>
                </v-btn>
                <v-btn
                    text
                    small
                    :to="`/quick-search/${duration}`"
                >
                    <v-icon>mdi-timer-outline</v-icon>
                    <span class="mx-1">{{ duration + 's' }}</span>
                </v-btn>
                <v-btn
                    text
                    small
                    :to="`/quick-search/${keyMode}`"
                >
                    <v-icon>mdi-music-circle-outline</v-icon>
                    <span class="mx-1">{{ keyMode }}</span>
                </v-btn>
            </div>
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
        <v-card-text>
            <SampleActions
                ref="sampleActions"
                :sampleId="id"
                @onClickPlayPause="playPause"
                @onClickRepeat="toggleRepeat"
            />
        </v-card-text>
    </v-card>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import SampleActions from '~/components/sample/SampleActions.vue'

export default {
    components: {
        WaveForm,
        SampleActions
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
            repeatSample: false
        }
    },

    computed: {
        keyMode () {
            if (this._key || this._mode) {
                return this._key + (this._mode == 'min' ? 'm' : this._mode == 'maj' ? 'M' : '')
            }

            return '-'
        }
    },

    methods: {
        playPause () {
            this.$refs.waveform.playPause()
        },

        toggleRepeat () {
            this.repeatSample = !this.repeatSample
        },

        onPlay () {
            this.$refs.sampleActions.setPlaying(true)
            this.$nuxt.$emit('samplePlay')
        },

        onPause () {
            this.$refs.sampleActions.setPlaying(false)
            this.$nuxt.$emit('sampleStop')
        },

        onFinish () {
            if (this.repeatSample) {
                this.$refs.waveform.play()
            } else {
                this.$refs.sampleActions.setPlaying(false)
                this.$nuxt.$emit('sampleStop')
            }
        }
    }
}
</script>
