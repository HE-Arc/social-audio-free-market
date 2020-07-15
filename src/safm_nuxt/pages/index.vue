<template>
    <div>
        <v-container>
            <h1>SAFMarket</h1>
            <section>
                <v-text-field
                    v-model="quickSearchInput"
                    label="Search anything"
                    outlined
                    @keypress.enter="quickSearch"
                    :append-icon="quickSearchIcon"
                    @click:append="quickSearch"
                ></v-text-field>
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
                <SampleList :samples="lastSamples" />
            </section>
        </v-container>
    </div>
</template>

<script>
import SampleList from '~/components/SampleList.vue'

export default {
    components: {
        SampleList
    },

    data () {
        return {
            quickSearchInput: '',
            lastSamples: []
        }
    },

    computed: {
        quickSearchIcon () {
            return this.quickSearchInput.length > 0 ? 'mdi-magnify' : ''
        }
    },

    async asyncData ({ $axios, params }) {
        try {
            const lastSamples = await $axios.$get('/samples/last')

            return { lastSamples }
        } catch (e) {
            this.$nuxt.$emit('snackbar', 'Problem while downloading last samples')
        }
    },

    head () {
        return {
            title: 'Home'
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
