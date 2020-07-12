<template>
    <div class="sample-fork">
        <div class="d-flex flex-row mb-6">
            <BtnPlayPause :sampleId="id" />
            <div class="pl-4">
                <div>
                    <nuxt-link :to="`/sample/${id}`">{{ name }}</nuxt-link>
                </div>
                <div>
                    <span>By</span>
                    <nuxt-link :to="`/profile/${userId}`">{{ username }}</nuxt-link>
                </div>
            </div>
        </div>
        <div>
            <WaveForm :id="id" height="50" />
        </div>
        <div v-if="datetime_download" class="mt-4">
            <span>{{ `Downloaded on ${new Date(datetime_download).toLocaleDateString()}` }}</span>
        </div>
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
    background: #1c1c1c;
    border-radius: 5px;
    padding: 1em;
    transition: all 0.2s;
}
.sample-fork:hover {
    box-shadow: 1px 1px 15px 5px #111111;
}
</style>
