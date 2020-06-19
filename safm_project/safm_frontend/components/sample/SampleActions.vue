<template>
    <div class="d-flex justify-space-between">
        <BtnPlayPause :sampleId="sampleId" />
        <v-btn
            large
            :color="repeat ? 'accent' : ''"
            @click="toggleRepeat"
        >
            <v-icon>{{ repeatIcon }}</v-icon>
        </v-btn>
        <BtnDownload :sampleId="sampleId" />
    </div>
</template>

<script>
import BtnPlayPause from '~/components/sample/BtnPlayPause'
import BtnDownload from '~/components/sample/BtnDownload'

export default {
    components: {
        BtnPlayPause,
        BtnDownload
    },

    props: [
        'sampleId'
    ],

    data () {
        return {
            repeat: false
        }
    },

    computed: {
        repeatIcon () {
            return this.repeat ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
        toggleRepeat () {
            this.repeat = !this.repeat
            this.$emit('onClickRepeat')
        }
    }
}
</script>
