<template>
    <div>
        <AdvancedSearch />
        <div class="search-results">
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="6"
                >
                    <Sample :sample="sample" />
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>
import AdvancedSearch from '~/components/AdvancedSearch.vue'
import Sample from '~/components/Sample.vue'

export default {
    components: {
        AdvancedSearch,
        Sample
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
