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
import SampleList from '~/components/sample/SampleList.vue'

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

    mounted () {
        this.loadLastSamples()
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
        },

        async loadLastSamples () {
            try {
                this.lastSamples = await this.$axios.$get('/samples/last')
            } catch (e) {
                this.$nuxt.$emit('snackbar', 'Could not load last samples.')
            }
        }
    }
}
</script>
