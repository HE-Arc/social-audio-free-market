<template>
    <div class="d-flex justify-space-between">
        <v-btn
            large
            :color="playPauseColor"
            @click="togglePlayPause"
        >
            <v-icon>{{ playPauseIcon }}</v-icon>
        </v-btn>
        <v-btn
            large
            :color="repeat ? 'accent' : ''"
            @click="toggleRepeat"
        >
            <v-icon>{{ repeatIcon }}</v-icon>
        </v-btn>
        <v-btn
            large
            @click="download"
        >
            <v-icon>mdi-download-outline</v-icon>
        </v-btn>
    </div>
</template>

<script>
const fileDownload = process.client ? require('js-file-download') : undefined

export default {
    props: [
        'sampleId'
    ],

    data () {
        return {
            isPlaying: false,
            repeat: false
        }
    },

    computed: {
        playPauseColor () {
            return this.isPlaying ? 'primary' : ''
        },

        playPauseIcon () {
            return this.isPlaying ? 'mdi-pause' : 'mdi-play'
        },

        repeatIcon () {
            return this.repeat ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
        togglePlayPause () {
            this.isPlaying = !this.isPlaying
            this.$emit('onClickPlayPause')
        },

        toggleRepeat () {
            this.repeat = !this.repeat
            this.$emit('onClickRepeat')
        },

        download() {
            this.$axios.get(`/sample_file/${this.sampleId}/1`, {
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
        },

        setPlaying (isPlaying) {
            this.isPlaying = isPlaying
        }
    }
}
</script>
