<template>
    <div>
        <v-container>
            <h2 class="page-title">{{ sample.name }}</h2>
            <section>
                <WaveForm
                    ref="waveform"
                    :id="sample.id"
                    @onPlay="onPlay"
                    @onPause="onPause"
                    @onFinish="onFinish"
                />
            </section>
            <v-card>
                <v-card-actions>
                    <v-btn
                        fab
                        x-large
                        :color="playPauseColor"
                        @click="playPause"
                        class="mx-2"
                    >
                        <v-icon>{{ playPauseIcon }}</v-icon>
                    </v-btn>
                    <v-btn
                        fab
                        x-large
                        :color="repeatSample ? 'accent' : ''"
                        @click="repeatSample = !repeatSample"
                        class="mx-2"
                    >
                        <v-icon>{{ repeatSampleIcon }}</v-icon>
                    </v-btn>
                    <v-btn
                        fab
                        x-large
                        @click="downloadSample"
                        class="mx-2"
                    >
                        <v-icon>mdi-download-outline</v-icon>
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                        fab
                        x-large
                        @click="likedSample = !likedSample"
                        class="pink--text"
                    >
                        <v-icon>{{ likeSampleIcon }}</v-icon>
                    </v-btn>
                </v-card-actions>
            </v-card>
            <section>
                <v-row>
                    <v-col cols="2" lg="2" md="3" sm=12>
                        <v-card class="text-center">
                            <nuxt-link :to="`/profiles/${sample.user.username}`">
                                <v-img
                                    src="https://image.flaticon.com/icons/svg/17/17004.svg"
                                    width="100"
                                    height="100"
                                    color="white"
                                ></v-img>
                                <v-card-title class="justify-center">
                                    {{ sample.user.username }}
                                </v-card-title>
                            </nuxt-link>
                            <v-card-actions>
                                <v-row>
                                    <v-col cols="12">
                                        <v-icon class="mr-1">mdi-music-note</v-icon>
                                        <span class="mr-2">8</span>
                                        <span class="mr-1">·</span>
                                        <v-icon class="mr-1">mdi-account-multiple</v-icon>
                                        <span>21</span>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-btn
                                            small
                                            color="accent"
                                        >
                                            <v-icon class="mr-1">mdi-account-plus</v-icon>
                                            Follow
                                        </v-btn>
                                    </v-col>
                                </v-row>
                            </v-card-actions>     
                        </v-card>
                    </v-col>
                    <v-col cols="10" lg="10" md="9" sm=12>
                        <v-card>
                            <v-card-actions>
                                <v-row class="text-center headline">
                                    <v-col cols="4">
                                        <v-icon large class="mr-2">mdi-metronome</v-icon>
                                        {{ sample.tempo }}
                                    </v-col>
                                    <v-col cols="4">
                                        <v-icon large class="mr-2">mdi-timer-outline</v-icon>
                                        {{ sample.duration }}s
                                    </v-col>
                                    <v-col cols="4">
                                        <v-icon large class="mr-2">mdi-music-circle-outline</v-icon>
                                        {{ keyMode }}
                                    </v-col>
                                </v-row>
                            </v-card-actions>
                            <v-divider class="mx-6"></v-divider>
                            <v-card-text>
                                <v-chip
                                    v-for="tag in sample.tags"
                                    :key="tag.id"
                                    class="tag mx-1"
                                    label
                                    small
                                >
                                    {{ tag.name }}
                                </v-chip>
                            </v-card-text>
                            <v-divider class="mx-6"></v-divider>
                            <v-card-text class="px-6 body-1">
                                {{ sample.description }}
                            </v-card-text>
                            <v-divider class="mx-6"></v-divider>
                            <v-card-text class="px-6 body-2">
                                {{ `Uploaded on ${new Date(sample.datetime_upload).toLocaleDateString()}` }}
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </section>
            <section>
                <h3 class="section-title">Fork</h3>
                <SampleForkContainer
                    :forkFrom="forkFrom"
                    :forkTo="forkTo"
                />
            </section>
        </v-container>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import SampleForkContainer from '~/components/SampleForkContainer.vue'
const fileDownload = process.client ? require('js-file-download') : undefined

export default {
    components: {
        WaveForm,
        SampleForkContainer
    },

    data () {
        return {
            sample: {},
            isPlaying: false,
            repeatSample: false,
            downloadLink: ``,
            likedSample: false,
            forkFrom: [],
            forkTo: []
        }
    },

    computed: {
        playPauseIcon () {
            return this.isPlaying ? 'mdi-pause' : 'mdi-play'
        },

        playPauseColor () {
            return this.isPlaying ? 'primary' : ''
        },

        repeatSampleIcon () {
            return this.repeatSample ? 'mdi-repeat' : 'mdi-repeat-off'
        },

        likeSampleIcon () {
            return this.likedSample ? 'mdi-heart' : 'mdi-heart-outline'
        },

        keyMode () {
            if (this.sample.key || this.sample.mode) {
                return this.sample.key + (this.sample.mode == 'min' ? 'm' : this.sample.mode == 'maj' ? 'M' : '')
            }

            return '-'
        }
    },

    async asyncData({ $axios, params }) {
        try {
            let sample = await $axios.$get(`/sample/${params.id}`)
            let forkFrom = await $axios.$get(`/fork_from/${params.id}`)
            let forkTo = await $axios.$get(`/fork_to/${params.id}`)
            
            return { sample, forkFrom, forkTo }
        } catch (e) {
            return { sample: {}, forkFrom: [], forkTo: [] }
        }
    },

    methods: {
        playPause () {
            this.$refs.waveform.playPause()
        },

        onPlay () {
            this.isPlaying = true
        },

        onPause () {
            this.isPlaying = false
        },

        onFinish () {
            if (this.repeatSample) {
                this.$refs.waveform.play()
            } else {
                this.isPlaying = false
            }
        },

        downloadSample () {
            this.$axios.get(`/sample_file/${this.sample.id}/1`, {
                responseType: 'blob'
            })
                .then((response) => {
                    let contentDisposition = response.request.getResponseHeader('Content-Disposition')

                    if (contentDisposition) {
                        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
                        let matches = filenameRegex.exec(contentDisposition)

                        if (matches !== null && matches[1]) {
                            let filename = matches[1].replace(/['"]/g, '')
                            fileDownload(response.data, filename)
                        }
                    }
                })
                .catch((error) => {
                    for (let e in error.response.data) {
                        this.$toast.error(`${e}: ${error.response.data[e]}`, {
                            duration: 5000
                        })
                    }
                })
        }
    }
}
</script>

<style scoped>
.v-image {
    margin: 0 auto;
}
</style>
