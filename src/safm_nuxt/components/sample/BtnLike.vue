<template>
    <v-btn
        fab
        large
        class="pink--text"
        :loading="loading"
        @click="click"
    >
        <v-icon>{{ likeIcon }}</v-icon>
    </v-btn>
</template>

<script>
export default {
    props: ['sampleId'],

    data () {
        return {
            liked: false,
            loading: false
        }
    },

    computed: {
        likeIcon () {
            return this.liked ? 'mdi-heart' : 'mdi-heart-outline'
        },
    },

    mounted () {
        if (this.$store.state.auth) {
            this.loadLikeState()
        }
    },

    methods: {
        async loadLikeState () {
            try {
                const response = await this.$axios.$get(`/sample/like/${this.sampleId}`)
                this.liked = response.liked
            } catch (e) {
                this.$nuxt.$emit('snackbar', 'An error occured')
            }
        },

        async click () {
            if (!this.loading) {
                this.loading = true

                if (this.$store.state.auth) {
                    this.liked = !this.liked

                    try {
                        let response = ''
                        if (this.liked) {
                            response = await this.$axios.post(`/sample/like/${this.sampleId}`)
                        } else {
                            response = await this.$axios.delete(`/sample/like/${this.sampleId}`)
                        }

                        this.$nuxt.$emit('snackbar', response.data.detail)
                    } catch (e) {
                        this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data))
                    }
                } else {
                    this.$nuxt.$emit('snackbar', 'You first need to log in.')
                }

                this.loading = false
            }
        }
    }
}
</script>
