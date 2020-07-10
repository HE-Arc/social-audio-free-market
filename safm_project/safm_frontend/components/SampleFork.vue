<template>
    <div class="sample-fork">
        <v-card>
            <v-card-title class="headline">
                <nuxt-link :to="`/sample/${id}`">{{ name }}</nuxt-link>
            </v-card-title>
            <v-card-text>
                By <nuxt-link :to="`/profile/${userId}`">{{ username }}</nuxt-link>
            </v-card-text>
            <WaveForm :id="id" />
            <v-card-text align="center">
                <BtnPlayPause :sampleId="id" />
            </v-card-text>
            <v-card-text v-if="datetime_download">
                {{ `Downloaded on ${new Date(datetime_download).toLocaleDateString()}` }}
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import BtnPlayPause from '~/components/sample/BtnPlayPause'

export default {
    components: {
        WaveForm,
        BtnPlayPause
    },

    props: [
        'id',
        'name',
        'userId',
        'username',
        'datetime_download'
    ]
}
</script>

<style scoped>
.sample-fork {
    width: 100%;
}
</style>
