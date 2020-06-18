<template>
    <div>
        <WaveForm :id="id" />
        <p>
            <nuxt-link :to="`/samples/${id}`">{{ name }}</nuxt-link>
        </p>
        <p>
            By
            <nuxt-link :to="`/profiles/${username}`">{{ username }}</nuxt-link>
        </p>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'

export default {
    components: {
        WaveForm
    },

    props: [
        'id',
        'name',
        'username'
    ]
}
</script>
