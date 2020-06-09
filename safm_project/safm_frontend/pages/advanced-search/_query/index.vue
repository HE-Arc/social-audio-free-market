<template>
    <div>
        <h2 class="page-title">Advanced Search</h2>
        <AdvancedSearch />
        <section>
            <h3 class="section-title">Search results</h3>
            <SampleList :samples="samples" />
        </section>
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
