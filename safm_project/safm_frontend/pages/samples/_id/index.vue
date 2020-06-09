<template>
    <div>
        <h2 class="page-title">{{ sample.name }}</h2>
        <section>
            <h3 class="section-title">Comments</h3>
            <Comments :comments="comments" />
        </section>
    </div>
</template>

<script>
import Comments from '~/components/Comments.vue'

export default {
    components: {
        Comments
    },

    data () {
        return {
            sample: [],
            comments: []
        }
    },

    async asyncData({ $axios, params }) {
        try {
            let sample = await $axios.$get(`/sample/${params.id}`)

            // THIS IS TEMPORARY ; WILL BE DEVELOPED LATER
            let comments = [
                {
                    id: 1,
                    username: 'qtipee',
                    text: 'Comments are not yet integrated.',
                    datetime: '08.06.2020 12:15'
                }
            ]
            return { sample, comments }
        } catch (e) {
            return { sample: [], comments: [] }
        }
    }
}
</script>
