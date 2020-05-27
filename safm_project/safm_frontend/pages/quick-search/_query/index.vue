<template>
    <div>
        <SampleList :samples="samples" />
    </div>
</template>

<script>
import SampleList from '~/components/SampleList.vue'

export default {
    components: {
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
                let samples = await $axios.$get(`/quick?search=${params.query}`)
                
                return { samples }
            }
        } catch (e) {
            return { samples: [] }
        }
    }
}
</script>
