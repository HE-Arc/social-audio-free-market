<template>
    <div>
        <h1>Advanced Search</h1>
        <AdvancedSearch />
        <section>
            <div v-if="samples.length > 0">
                <h2>Search results</h2>
                <SampleList :samples="samples" />
            </div>
            <div v-else>
                <ErrorDisplay title="No Results" />
            </div>
        </section>
    </div>
</template>

<script>
import AdvancedSearch from '~/components/AdvancedSearch.vue'
import SampleList from '~/components/SampleList.vue'
import ErrorDisplay from '~/components/ErrorDisplay.vue'

export default {
    components: {
        AdvancedSearch,
        SampleList,
        ErrorDisplay
    },

    data () {
        return {
            samples: []
        }
    },

    async asyncData ({ $axios, params }) {
        try {
            if (params.query.length > 0) {
                let samples = await $axios.$get(`/ad_search?${params.query}`)
                
                return { samples }
            }
        } catch (error) {
            return { samples: [] }
        }
    }
}
</script>
