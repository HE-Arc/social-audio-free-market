<template>
    <main>
       <v-container>
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
        </v-container>
    </main>
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
            let userProfile = await $axios.$get(`/profile/${params.id}`)
            let samples = await $axios.$get(`/samples/${params.id}`)

            return { userProfile, samples }
        } catch (e) {
            return { userProfile: [], samples: [] }
        }
    }
}
</script>
