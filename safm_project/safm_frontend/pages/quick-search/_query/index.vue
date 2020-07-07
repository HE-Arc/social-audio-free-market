<template>
    <div>
        <h1>Search Results</h1>
        <div v-if="samples.length > 0">
            <SampleList :samples="samples" />
        </div>
        <div v-else>
            <ErrorDisplay title="No Results" />
        </div>
    </div>
</template>

<script>
import SampleList from '~/components/SampleList.vue'
import ErrorDisplay from '~/components/ErrorDisplay.vue'

export default {
    components: {
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
                let samples = await $axios.$get(`/quick?search=${params.query}`)
                
                return { samples }
            }
        } catch (e) {
            return { samples: [] }
        }
    }
}
</script>
