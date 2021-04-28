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
const fileDownload = process.client ? require('js-file-download') : undefined;

export default {
    props: ['sampleId'],

    data() {
        return {
            loading: false
        };
    },

    methods: {
        // On button click
        async click() {
            if (!this.loading) {
                this.loading = true;

                try {
                    // Gets the sample audio file
                    const response = await this.$axios.get(`/sample/file/${this.sampleId}/1`, { responseType: 'blob' });

                    // Prepares the audio file for download
                    const contentDisposition = response.request.getResponseHeader('Content-Disposition');
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(contentDisposition);

                    if (matches !== null && matches[1]) {
                        const filename = matches[1].replace(/['"]/g, '');
                        // Triggers the download dialog
                        fileDownload(response.data, filename);
                    }
                } catch (e) {
                    this.$nuxt.$emit('snackbar', 'Problem while downloading the sample.');
                }

                this.loading = false;
            }
        }
    }
};
</script>
