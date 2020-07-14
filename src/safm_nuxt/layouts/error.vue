<template>
    <v-app dark>
        <v-container>
            <h1>Error</h1>
            <p align="center">{{ error.message }}</p>
        </v-container>
    </v-app>
</template>

<script>
export default {
    layout: 'empty',

    props: {
        error: {
            type: Object,
            default: null
        }
    },

    computed: {
        codeStatusMessage () {
            switch (this.error.statusCode) {
            case 401: return 'Unauthorised'
            case 404: return 'Not Found'
            default: return 'An error occured'
            }
        }
    },

    head () {
        return {
            title: this.codeStatusMessage
        }
    }
}
</script>
