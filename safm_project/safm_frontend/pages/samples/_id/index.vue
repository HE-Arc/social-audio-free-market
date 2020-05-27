<template>
    <div class="sample-page">
        <section class="section-sample">
        </section>
        <section class="section-comments">
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
                    username: 'Len Faki',
                    text: 'Aliquip laborum dolor ex ut ut qui ipsum. Ullamco tempor deserunt incididunt veniam. Pariatur veniam ad tempor sit. Ipsum dolore pariatur aliqua veniam eu est.',
                    datetime: '26.04.2020 14:30'
                },
                {
                    id: 2,
                    username: 'Solomun',
                    text: 'Amet dolor laboris ea ad mollit elit nulla aliquip. Occaecat consectetur commodo culpa excepteur consectetur occaecat. Ullamco culpa occaecat cillum ipsum deserunt culpa reprehenderit. Occaecat pariatur et reprehenderit eu labore nisi non consequat ipsum nisi tempor ullamco fugiat Lorem. Ut Lorem qui id eu velit id ut fugiat sit cupidatat. Sunt voluptate ex voluptate cillum proident magna.',
                    datetime: '26.04.2020 14:43'
                }
            ]
            return { sample, comments }
        } catch (e) {
            return { sample: [], comments: [] }
        }
    }
}
</script>
