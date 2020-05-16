<template>
    <div>
        <v-dialog
            v-model="dialog"
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
                            label="Tag, tone, tempo, username, ..."
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
        }
    }
}
</script>
