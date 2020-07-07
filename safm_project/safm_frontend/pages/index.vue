<template>
    <div>
        <v-container>
            <h1>SAFMarket</h1>
            <section>
                <v-text-field
                    v-model="quickSearchInput"
                    label="Tag, tempo, user, ..."
                    outlined
                    hide-details
                    single-line
                    @keypress.enter="quickSearch"
                >
                    <template v-slot:append>
                        <v-icon @click="quickSearch">{{ quickSearchIcon }}</v-icon>
                    </template>
                </v-text-field>
                <v-btn
                    color="primary"
                    text
                    @click="advancedSearch"
                >
                    Advanced Form
                </v-btn>
            </section>
        </v-container>
    </div>
</template>

<script>
export default {
    middleware: 'authenticated',

    data () {
        return {
            quickSearchInput: ''
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
                this.dialog = false
                this.$router.push(`/quick-search/${this.quickSearchInput}`)
                this.quickSearchInput = ''
            }
        },

        advancedSearch () {
            this.dialog = false
            this.$router.push('/advanced-search')
        }
    }
}
</script>
