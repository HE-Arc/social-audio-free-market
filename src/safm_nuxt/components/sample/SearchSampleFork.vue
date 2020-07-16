<template>
    <div>
        <v-text-field
            v-model="searchInput"
            label="Search samples..."
            outlined
            @input="typing"
        ></v-text-field>
    </div>
</template>

<script>
export default {
    data () {
        return {
            searchInput: '',
            timeout: null,
            loading: false
        }
    },

    methods: {
        typing () {
            clearTimeout(this.timeout)

            if (this.searchInput.length > 1) {
                this.timeout = setTimeout(this.search, 500)
            }
        },

        async search () {
            if (!this.loading && this.searchInput.length > 1) {
                this.loading = true

                try {
                    const results = await this.$axios.$get(`/quick?search=${this.searchInput}`)

                    this.$nuxt.$emit('searchForks', results)
                } catch (e) {
                    this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data))
                }

                this.loading = false
            }
        }
    }
}
</script>
