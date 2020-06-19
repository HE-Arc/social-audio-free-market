<template>
    <div class="d-flex justify-space-between">
        <BtnPlayPause :sampleId="sampleId" />
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
import BtnPlayPause from '~/components/sample/BtnPlayPause'
const fileDownload = process.client ? require('js-file-download') : undefined

export default {
    components: {
        BtnPlayPause
    },

    props: [
        'sampleId'
    ],

    data () {
        return {
            repeat: false
        }
    },

    computed: {
        repeatIcon () {
            return this.repeat ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
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
        }
    }
}
</script>
