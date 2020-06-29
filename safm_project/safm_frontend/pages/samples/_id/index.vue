<template>
    <div>
        <v-container>
            <h2 class="page-title">{{ sample.name }}</h2>
            <section>
                <WaveForm
                    ref="waveform"
                    :id="sample.id"
                />
            </section>
            <v-card>
                <v-card-text>
                    <SampleActions :sampleId="sample.id" />
                    <v-spacer></v-spacer>
                    <v-btn
                        fab
                        x-large
                        @click="likedSample = !likedSample"
                        class="pink--text"
                    >
                        <v-icon>{{ likeSampleIcon }}</v-icon>
                    </v-btn>
                </v-card-text>
            </v-card>
            <section>
                <v-row>
                    <v-col
                        cols="12"
                        sm="3"
                        md="2"
                    >
                        <v-card class="text-center">
                            <nuxt-link :to="`/profiles/${userId}`">
                                <v-img
                                    src="https://image.flaticon.com/icons/svg/17/17004.svg"
                                    width="100"
                                    height="100"
                                    color="white"
                                ></v-img>
                                <v-card-title class="justify-center">
                                    {{ username }}
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
                    <v-col
                        cols="12"
                        sm="9"
                        md="10"
                    >
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
import SampleActions from '~/components/sample/SampleActions.vue'
import SampleForkContainer from '~/components/SampleForkContainer.vue'

export default {
    components: {
        WaveForm,
        SampleActions,
        SampleForkContainer
    },

    data () {
        return {
            sample: {},
            userId: '',
            username: '',
            likedSample: false,
            forkFrom: [],
            forkTo: []
        }
    },

    computed: {
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
        const sample = await $axios.$get(`/sample/${params.id}`)
        const forkFrom = await $axios.$get(`/fork_from/${params.id}`)
        const forkTo = await $axios.$get(`/fork_to/${params.id}`)

        return {
            sample: sample,
            userId: sample.user.id,
            username: sample.user.username,
            forkFrom: forkFrom,
            forkTo: forkTo
        }
    }
}
</script>

<style scoped>
.v-image {
    margin: 0 auto;
}
</style>
