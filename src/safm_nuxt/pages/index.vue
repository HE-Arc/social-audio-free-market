<template>
    <div>
        <v-container>
            <h1>SAFMarket</h1>
            <section>
                <v-text-field
                    v-model="quickSearchInput"
                    label="Search anything"
                    outlined
                    :append-icon="quickSearchIcon"
                    @keypress.enter="quickSearch"
                    @click:append="quickSearch"
                />
                <div class="text-center">
                    <v-btn
                        color="primary"
                        text
                        @click="advancedSearch"
                    >
                        Advanced Search
                    </v-btn>
                </div>
            </section>
            <section>
                <h2>Last Samples</h2>
                <div v-if="lastSamples.length > 0">
                    <SampleList :samples="lastSamples" />
                </div>
                <div v-else>
                    <p>Could not load latest samples</p>
                </div>
            </section>
        </v-container>
    </div>
</template>

<script>
import SampleList from '~/components/sample/SampleList.vue';

export default {
    components: {
        SampleList
    },

    async asyncData({ $axios }) {
        try {
            const lastSamples = await $axios.$get('/samples/last');

            return { lastSamples };
        } catch (e) {
            return { lastSamples: [] };
        }
    },

    data() {
        return {
            quickSearchInput: '',
            lastSamples: []
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
                this.dialog = false;
                this.$router.push(`/quick-search/${this.quickSearchInput}`);
                this.quickSearchInput = '';
            }
        },

        // Goes to the Advanced Search page
        advancedSearch() {
            this.dialog = false;
            this.$router.push('/advanced-search');
        }
    },

    head() {
        return {
            title: 'Home'
        };
    }
};
</script>
