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
                @onClickPlayPause="playPause"
                @onClickRepeat="toggleRepeat"
                @onClickDownload="downloadSample"
            />
        </v-card-text>
    </v-card>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import SampleActions from '~/components/sample/SampleActions.vue'
const fileDownload = process.client ? require('js-file-download') : undefined

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
        },

        downloadSample () {
            this.$axios.get(`/sample_file/${this.id}/1`, {
                responseType: 'blob'
            })
                .then((response) => {
                    let contentDisposition = response.request.getResponseHeader('Content-Disposition')

                    if (contentDisposition) {
                        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
                        let matches = filenameRegex.exec(contentDisposition)

                        if (matches !== null && matches[1]) {
                            let filename = matches[1].replace(/['"]/g, '')
                            fileDownload(response.data, filename)
                        }
                    }
                })
                .catch((error) => {
                    for (let e in error.response.data) {
                        this.$toast.error(`${e}: ${error.response.data[e]}`, {
                            duration: 5000
                        })
                    }
                })
        }
    }
}
</script>
