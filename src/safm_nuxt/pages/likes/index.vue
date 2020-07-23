<template>
    <div>
        <h1>Liked Samples</h1>
        <div v-if="likedSamples.length > 0">
            <SampleList :samples="likedSamples" />
        </div>
        <div v-else>
            <p>You don't like any sample yet.</p>
        </div>
    </div>
</template>

<script>
import SampleList from '~/components/sample/SampleList.vue'

export default {
    middleware: 'authenticated',

    components: {
        SampleList
    },

    data () {
        return {
            likedSamples: []
        }
    },

    async asyncData ({ $axios, error }) {
        try {
            const response = await $axios.$get('/user/samples/likes')
            
            let likedSamples = []
            for (let sample of response) {
                likedSamples.push(sample['sample'])
            }
                
            return { likedSamples }
        } catch (e) {
            error({ statusCode: 401, message: 'You must be logged in.' })
        }
    },

    head () {
        return {
            title: 'Likes'
        }
    },
}
</script>
