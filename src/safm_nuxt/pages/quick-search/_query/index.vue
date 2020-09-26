<template>
    <div>
        <h1>Search Results</h1>
        <div v-if="samples.length > 0">
            <SampleList :samples="samples" />
        </div>
        <div v-else>
            <h2>No Results</h2>
        </div>
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
            samples: []
        }
    },

    async asyncData ({ $axios, params, error }) {
        try {
            if (params.query.length > 0) {
                // Quick Search query based on parameter
                const samples = await $axios.$get(`/search/quick?search=${params.query}`)
                
                return { samples }
            }
        } catch (e) {
            error({ statusCode: 404, message: 'Page not found' })
        }
    },

    head () {
        return {
            title: 'Quick Search'
        }
    },
}
</script>
