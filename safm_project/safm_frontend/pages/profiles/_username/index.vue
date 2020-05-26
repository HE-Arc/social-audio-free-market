<template>
    <div class="user-profile">
        <section class="user-info">

        </section>
        <section class="user-samples">
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
