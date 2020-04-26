<template>
    <main>
        <v-container>
            <QuickSearch :baseQuickSearchInput="baseQuickSearchInput"/>
        </v-container>

        <v-container>
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="6"
                >
                    <Sample :sample="sample" />
                </v-col>
            </v-row>
        </v-container>
    </main>
</template>

<script>
import QuickSearch from '~/components/QuickSearch.vue'
import Sample from '~/components/Sample.vue'

export default {
    components: {
        QuickSearch,
        Sample
    },

    data () {
        return {
            baseQuickSearchInput: '',
            samples: []
        }
    },

    async asyncData ({ $axios, params }) {
        try {
            if (params.query.length > 0) {
                let baseQuickSearchInput = params.query
                let samples = await $axios.$get(`/quick?search=${params.query}`)
                
                return { baseQuickSearchInput, samples }
            }
        } catch (e) {
            return { baseQuickSearchInput: '', samples: [] }
        }
    }
}
</script>
