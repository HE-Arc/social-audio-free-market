<template>
    <div>
        <v-container>
            <h2 class="page-title">{{ sample.name }}</h2>
            <WaveForm
                ref="waveform"
                :id="sample.id"
                @onPlay="onPlay"
                @onPause="onPause"
                @onFinish="onFinish"
            />
            <section>
                <v-row>
                    <v-col cols="4">
                        <v-card>
                            <nuxt-link :to="`/profiles/${sample.user.username}`">
                            <v-img
                                src="https://image.flaticon.com/icons/svg/17/17004.svg"
                                width="100"
                                height="100"
                                color="white"
                            ></v-img>
                            <v-card-title>
                                {{ sample.user.username }}
                            </v-card-title>
                            </nuxt-link>
                            <v-card-actions>
                                <v-row align="center">
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
                    <v-col cols="8">
                            <v-row>
                            <v-col cols="4">
                                <v-icon>mdi-metronome</v-icon>
                                {{ sample.tempo }}
                            </v-col>
                            <v-col cols="4">
                                <v-icon>mdi-timer-outline</v-icon>
                                {{ sample.duration }}
                            </v-col>
                            <v-col cols="4" v-if="sample.key || sample.mode">
                                <v-icon>mdi-music-circle-outline</v-icon>
                                {{ sample.key + sample.mode }}
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </section>
            <section>
                <h3 class="section-title">Comments</h3>
                <Comments :comments="comments" />
            </section>
        </v-container>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import Comments from '~/components/Comments.vue'

export default {
    components: {
        WaveForm,
        Comments
    },

    data () {
        return {
            sample: {},
            isPlaying: false,
            repeatSample: false,
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
            return { sample: {}, comments: [] }
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
        }
    }
}
</script>
