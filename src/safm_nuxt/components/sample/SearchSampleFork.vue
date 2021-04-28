<template>
    <div>
        <v-text-field
            v-model="searchInput"
            label="Search samples..."
            outlined
            @input="typing"
        />
    </div>
</template>

<script>
export default {
    data() {
        return {
            searchInput: '',
            timeout: null,
            timeoutDuration: 500,
            loading: false
        };
    },

    methods: {
        // Triggers a timeout whenever the user types in order to
        // automatically query a search when it stops
        typing() {
            // Cancels the current timeout
            clearTimeout(this.timeout);

            if (this.searchInput.length > 1) {
                // Triggers a timeout if the input is not empty
                this.timeout = setTimeout(this.search, this.timeoutDuration);
            }
        },

        // Performs a search
        async search() {
            if (!this.loading && this.searchInput.length > 1) {
                this.loading = true;

                try {
                    // Gets the tags based on the input value
                    const results = await this.$axios.$get(`/quick?search=${this.searchInput}`);

                    this.$nuxt.$emit('searchForks', results);
                } catch (e) {
                    this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data));
                }

                this.loading = false;
            }
        }
    }
};
</script>
