<template>
    <div class="d-flex justify-space-between">
        <v-btn
            large
            :color="playPauseColor"
            @click="togglePlayPause"
        >
            <v-icon>{{ playPauseIcon }}</v-icon>
        </v-btn>
        <v-btn
            large
            :color="repeat ? 'accent' : ''"
            @click="toggleRepeat"
        >
            <v-icon>{{ repeatIcon }}</v-icon>
        </v-btn>
        <v-btn
            large
            @click="download"
        >
            <v-icon>mdi-download-outline</v-icon>
        </v-btn>
    </div>
</template>

<script>
export default {
    data () {
        return {
            isPlaying: false,
            repeat: false
        }
    },

    computed: {
        playPauseColor () {
            return this.isPlaying ? 'primary' : ''
        },

        playPauseIcon () {
            return this.isPlaying ? 'mdi-pause' : 'mdi-play'
        },

        repeatIcon () {
            return this.repeat ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
        togglePlayPause () {
            this.isPlaying = !this.isPlaying
            this.$emit('onClickPlayPause')
        },

        toggleRepeat () {
            this.repeat = !this.repeat
            this.$emit('onClickRepeat')
        },

        download() {
            this.$emit('onClickDownload')
        },

        setPlaying (isPlaying) {
            this.isPlaying = isPlaying
        }
    }
}
</script>
