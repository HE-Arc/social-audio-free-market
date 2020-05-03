<template>
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
</template>

<script>
import Sample from '~/components/Sample.vue'

export default {
    components: {
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
                let samples = await $axios.$get(`/quick?search=${params.query}`)
                
                return { samples }
            }
        } catch (e) {
            return { samples: [] }
        }
    }
}
</script>
