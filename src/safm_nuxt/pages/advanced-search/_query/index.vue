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
                <h2>No Results</h2>
            </div>
        </section>
    </div>
</template>

<script>
import AdvancedSearch from '~/components/AdvancedSearch.vue'
import SampleList from '~/components/sample/SampleList.vue'

export default {
    components: {
        AdvancedSearch,
        SampleList
    },

    data () {
        return {
            samples: []
        }
    },

    async asyncData ({ $axios, params, error }) {
        try {
            if (params.query && params.query.length > 0) {
                // Advanced Search query based on params
                const samples = await $axios.$get(`/search/advanced?${params.query}`)

                return { samples }
            }
        } catch (e) {
            error({ statusCode: 404, message: 'Page not found' })
        }
    },

    head () {
        return {
            title: 'Advanced Search'
        }
    }
}
</script>
