<template>
    <div>
        <v-dialog
            v-model="dialog"
            max-width="600"
            light
        >
            <template #activator="{ on }">
                <v-btn
                    fab
                    depressed
                    v-on="on"
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
                            label="Search anything"
                            autofocus
                            outlined
                            hide-details
                            single-line
                            @keypress.enter="quickSearch"
                        >
                            <template #append>
                                <v-icon @click="quickSearch">
                                    {{ quickSearchIcon }}
                                </v-icon>
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
                            Advanced Search
                        </v-btn>
                    </v-container>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {

    data() {
        return {
            dialog: false,
            quickSearchInput: ''
        };
    },

    computed: {
        quickSearchIcon() {
            return this.quickSearchInput.length > 0 ? 'mdi-magnify' : '';
        }
    },

    methods: {
        // Performs a Quick Search
        quickSearch() {
            if (this.quickSearchInput.length > 0) {
                // Replaces the commas with dots (commas do not work as expected in Django search)
                this.quickSearchInput = this.quickSearchInput.replace(/,/g, '.');
                this.dialog = false;

                // Goes to the Quick Search results page
                this.$router.push(`/quick-search/${this.quickSearchInput}`);

                // Resets the input
                this.quickSearchInput = '';
            }
        },

        // Goes to the Advanced Search page
        advancedSearch() {
            this.dialog = false;
            this.$router.push('/advanced-search');
        }
    }
};
</script>
