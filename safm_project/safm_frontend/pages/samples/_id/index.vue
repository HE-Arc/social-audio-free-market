<template>
    <div>
        <v-container>
            <div v-if="sample">
                <h1>{{ sample.name }}</h1>
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
                            disabled
                        >
                            <v-icon>{{ likeSampleIcon }}</v-icon>
                        </v-btn>
                        <v-btn
                            v-if="canEdit"
                            fab
                            x-large
                            :to="`/samples/edit/${this.sample.id}`"
                        >
                            <v-icon>mdi-pencil</v-icon>
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
                                        :src="profilePictureSrc"
                                        width="100"
                                        height="100"
                                    ></v-img>
                                    <v-card-title class="justify-center">
                                        {{ username }}
                                    </v-card-title>
                                </nuxt-link>
                                <v-card-actions>
                                    <v-row>
                                        <v-col cols="12">
                                            <v-icon class="mr-1">mdi-music-note</v-icon>
                                            <span class="mr-2">{{ numberSamples }}</span>
                                            <span class="mr-1">·</span>
                                            <v-icon class="mr-1">mdi-account-multiple</v-icon>
                                            <span>-</span>
                                        </v-col>
                                        <v-col cols="12">
                                            <v-btn
                                                small
                                                color="accent"
                                                disabled
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
                    <h2>Fork</h2>
                    <div v-if="forkFrom.length > 0 || forkTo.length > 0">
                        <SampleForkContainer
                            :forkFrom="forkFrom"
                            :forkTo="forkTo"
                        />
                    </div>
                    <div v-else>
                        This sample does not have any fork.
                    </div>
                </section>
            </div>
            <div v-else>
                <ErrorDisplay title="This sample does not exist" />
            </div>
        </v-container>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import SampleActions from '~/components/sample/SampleActions.vue'
import SampleForkContainer from '~/components/SampleForkContainer.vue'
import ErrorDisplay from '~/components/ErrorDisplay.vue'

export default {
    components: {
        WaveForm,
        SampleActions,
        SampleForkContainer,
        ErrorDisplay
    },

    data () {
        return {
            sample: '',
            userId: '',
            username: '',
            numberSamples: '',
            likedSample: false,
            forkFrom: [],
            forkTo: []
        }
    },

    computed: {
        profilePictureSrc () {
            return `${this.$axios.defaults.baseURL}/user/picture/${this.userId}`
        },

        likeSampleIcon () {
            return this.likedSample ? 'mdi-heart' : 'mdi-heart-outline'
        },

        canEdit () {
            if (this.$store.state.user) {
                return this.userId == this.$store.state.user.id
            }
            
            return false
        },

        keyMode () {
            if (this.sample.key != ' ' || this.sample.mode != ' ') {
                return this.sample.key + (this.sample.mode == 'min' ? 'm' : this.sample.mode == 'maj' ? 'M' : '')
            }

            return '-'
        }
    },

    async asyncData({ $axios, params }) {
        try {
            const sample = await $axios.$get(`/sample/${params.id}`)
            const numberSamples = await $axios.$get(`/user/samples/count/${sample.user.id}`)
            const forkFrom = await $axios.$get(`/forks/from/${params.id}`)
            const forkTo = await $axios.$get(`/forks/to/${params.id}`)

            return {
                sample: sample,
                userId: sample.user.id,
                username: sample.user.username,
                numberSamples: numberSamples.count,
                forkFrom: forkFrom,
                forkTo: forkTo
            }
        } catch (e) {
            return {
                sample: '',
                userId: '',
                username: '',
                numberSamples: '',
                forkFrom: [],
                forkTo: []
            }
        }
    }
}
</script>

<style scoped>
.v-image {
    border-radius: 100px;
    margin: 0 auto;
}
</style>
