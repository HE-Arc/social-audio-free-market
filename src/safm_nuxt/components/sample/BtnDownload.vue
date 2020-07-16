<template>
    <v-btn
        fab
        large
        :loading="loading"
        @click="click"
    >
        <v-icon>mdi-download-outline</v-icon>
    </v-btn>
</template>

<script>
const fileDownload = process.client ? require('js-file-download') : undefined

export default {
    props: ['sampleId'],

    data () {
        return {
            loading: false
        }
    },

    methods: {
        async click () {
            if (!this.loading) {
                this.loading = true

                try {
                    const response = await this.$axios.get(`/sample/file/${this.sampleId}/1`, { responseType: 'blob' })
                    
                    const contentDisposition = response.request.getResponseHeader('Content-Disposition')
                    let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
                    let matches = filenameRegex.exec(contentDisposition)

                    if (matches !== null && matches[1]) {
                        let filename = matches[1].replace(/['"]/g, '')
                        fileDownload(response.data, filename)
                    }
                } catch (e) {
                    this.$nuxt.$emit('snackbar', 'Problem while downloading the sample')
                }

                this.loading = false
            }
        }
    }
}
</script>
