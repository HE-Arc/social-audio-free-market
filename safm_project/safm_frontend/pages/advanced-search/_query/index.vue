<template>
    <div>
        <AdvancedSearch />
        <SampleList :samples="samples" />
    </div>
</template>

<script>
import AdvancedSearch from '~/components/AdvancedSearch.vue'
import SampleList from '~/components/SampleList.vue'

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

    async asyncData ({ $axios, params }) {
        try {
            if (params.query.length > 0) {
                let samples = await $axios.$get(`/ad_search?${params.query}`)
                
                return { samples }
            }
        } catch (e) {
            return { samples: [] }
        }
    }
}
</script>
