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
                    <v-col cols="3">
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
                    <v-col cols="9">
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
                                Veniam pariatur deserunt exercitation anim enim veniam id aliquip sit velit. Laborum officia proident laboris incididunt incididunt excepteur ad reprehenderit. Irure nostrud non sunt consequat adipisicing proident ex enim. Duis non labore dolor fugiat incididunt amet velit ut irure sit amet esse tempor.
                                Ad nisi et qui qui officia dolor ullamco duis tempor aute nulla eiusmod elit. Ipsum proident consectetur ipsum ipsum et laboris dolor id ad ut deserunt velit ad. Lorem amet proident qui commodo ut cillum excepteur cillum anim ullamco ea nulla esse ipsum. Minim ex labore deserunt occaecat proident non incididunt velit consequat deserunt et cupidatat. Laboris occaecat mollit proident exercitation ea mollit elit. Incididunt nisi nostrud ullamco exercitation velit irure. Culpa proident non elit pariatur adipisicing Lorem occaecat ad mollit occaecat.
                            </v-card-text>
                        </v-card>
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

    computed: {
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
