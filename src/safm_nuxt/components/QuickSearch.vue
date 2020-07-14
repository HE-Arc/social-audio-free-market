<template>
    <div>
        <v-dialog
            v-model="dialog"
            max-width="600"
            light
        >
            <template v-slot:activator="{ on }">
                <v-btn
                    v-on="on"
                    fab
                    depressed
                >
                    <v-icon>mdi-magnify</v-icon>
                </v-btn>
            </template>
            <v-card>
                <v-card-title
                    class="headline"
                >
                    Quick Search
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-text-field
                            v-model="quickSearchInput"
                            label="Tag, tempo, user, ..."
                            autofocus
                            outlined
                            hide-details
                            single-line
                            @keypress.enter="quickSearch"
                        >
                            <template v-slot:append>
                                <v-icon @click="quickSearch">{{ quickSearchIcon }}</v-icon>
                            </template>
                        </v-text-field>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-container>
                        <v-btn
                            color="accent"
                            text
                            @click="advancedSearch"
                        >
                            Advanced Form
                        </v-btn>
                    </v-container>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {

    data () {
        return {
            dialog: false,
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
