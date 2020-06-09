<template>
    <div>
        <h2 class="page-title">{{ username }}</h2>
        <section>
            <h3 class="section-title">User Samples</h3>
            <SampleList :samples="samples" />
        </section>
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
            userProfile: [],
            samples: []
        }
    },

    computed: {
        username () {
            return this.$route.params.username
        }
    },

    async asyncData({ $axios, params }) {
        try {
            let userProfile = await $axios.$get(`/profile/${params.username}`)
            let samples = await $axios.$get(`/samples/${params.username}`)

            return { userProfile, samples }
        } catch (e) {
            return { userProfile: [], samples: [] }
        }
    }
}
</script>
