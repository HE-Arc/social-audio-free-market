<template>
    <main>
        <v-container>
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="6"
                >
                    <Sample :sample="sample"/>
                </v-col>
            </v-row>
        </v-container>
    </main>
</template>

<script>
import Sample from '~/components/Sample.vue'

export default {
    components: {
        Sample
    },

    async asyncData ({ $axios, params }) {
        try {
            const options = {
                credentials: 'same-origin'
            }
            let samples = await $axios.$get('/quick?search=acid', options)

            return { samples }
        } catch (e) {
            return { samples: [] }
        }
    },

    data () {
        return {
            samples: []
        }
    },
}
</script>
