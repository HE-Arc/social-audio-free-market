<template>
    <div class="user-profile">
        <section class="user-info">

        </section>
        <section class="user-samples">
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="6"
                >
                    <Sample :sample="sample" />
                </v-col>
            </v-row>
        </section>
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
