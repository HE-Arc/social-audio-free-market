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
            username: '',
            profile: {},
            samples: []
        }
    },

    async asyncData({ $axios, params }) {
        try {
            const profile = await $axios.$get(`/profile/${params.id}`)
            const samples = await $axios.$get(`/samples/${params.id}`)

            return {
                username: profile.user.username,
                profile: profile,
                samples: samples
            }
        } catch (e) {
            return {
                username: '',
                userProfile: {},
                samples: []
            }
        }
    }
}
</script>
