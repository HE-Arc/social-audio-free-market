<template>
    <div>
        <v-card>
            <v-card-title class="headline">
                <nuxt-link :to="`/samples/${id}`">{{ name }}</nuxt-link>
            </v-card-title>
            <v-card-text>
                By <nuxt-link :to="`/profiles/${username}`">{{ username }}</nuxt-link>
            </v-card-text>
            <WaveForm :id="id" />
            <v-card-text>
                <BtnPlayPause :sampleId="id" />
            </v-card-text>
            <v-card-text v-if="datetime_download">
                Downloaded on {{ datetime_download }}
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
        'username',
        'datetime_download'
    ]
}
</script>
