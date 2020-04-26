<template>
    <div id="quick-search">
        <v-text-field
            v-model="quickSearchInput"
            label="Quick Search"
            outlined
            hide-details
            single-line
            @keypress.enter="quickSearch"
        >
            <template v-slot:append>
                <v-icon @click="quickSearch">{{ quickSearchIcon }}</v-icon>
            </template>
        </v-text-field>
    </div>
</template>

<script>
export default {
    props: ['baseQuickSearchInput'],

    data () {
        return {
            quickSearchInput: this.baseQuickSearchInput
        }
    },

    computed: {
        quickSearchIcon () {
            return this.quickSearchInput.length > 0 ? 'mdi-magnify' : ''
        }
    },
    
    methods: {
        quickSearch () {
            if (this.quickSearchInput.length > 0) {
                this.$router.push(`/quick-search/${this.quickSearchInput}`)
            }
        }
    }
}
</script>
