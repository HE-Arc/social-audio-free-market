<template>
    <div>
        <v-container>
            <h1>{{ sample.name }}</h1>
            <BtnEdit
                :sampleId="sample.id"
                :sampleUserId="userId"
                fixed
                bigMargin
            />
            <section>
                <WaveForm
                    ref="waveform"
                    :id="sample.id"
                />
            </section>
            <v-card>
                <v-card-text>
                    <SampleActions :sampleId="sample.id" />
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
                            <nuxt-link :to="`/profile/${userId}`">
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
                                <v-row :class="`text-center ${this.propertySize}`">
                                    <v-col cols="4">
                                        <v-icon
                                            :large="large"
                                            :class="iconMr"
                                        >
                                            mdi-metronome
                                        </v-icon>
                                        {{ sample.tempo }}
                                    </v-col>
                                    <v-col cols="4">
                                        <v-icon
                                            :large="large"
                                            :class="iconMr"
                                        >
                                            mdi-timer-outline
                                        </v-icon>
                                        {{ sample.duration }}s
                                    </v-col>
                                    <v-col cols="4">
                                        <v-icon
                                            :large="large"
                                            :class="iconMr"
                                        >
                                            mdi-music-circle-outline
                                        </v-icon>
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
        </v-container>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import SampleActions from '~/components/sample/SampleActions.vue'
import BtnEdit from '~/components/sample/BtnEdit.vue'
import SampleForkContainer from '~/components/sample/SampleForkContainer.vue'

export default {
    components: {
        WaveForm,
        SampleActions,
        BtnEdit,
        SampleForkContainer
    },

    data () {
        return {
            sample: '',
            userId: '',
            username: '',
            numberSamples: '',
            forkFrom: [],
            forkTo: []
        }
    },

    computed: {
        profilePictureSrc () {
            return `${this.$axios.defaults.baseURL}/user/picture/${this.userId}`
        },

        large () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return false
            case 'sm': return false
            case 'md': return true
            case 'lg': return true
            case 'xl': return true
            }
        },

        iconMr () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return 'mr-1'
            case 'sm': return 'mr-1'
            case 'md': return 'mr-2'
            case 'lg': return 'mr-2'
            case 'xl': return 'mr-2'
            }
        },

        propertySize () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return 'title'
            case 'sm': return 'title'
            case 'md': return 'headline'
            case 'lg': return 'headline'
            case 'xl': return 'headline'
            }
        },
        
        keyMode () {
            if (this.sample.key != ' ' || this.sample.mode != ' ') {
                // Converts the mode into either m or M
                return this.sample.key + (this.sample.mode == 'min' ? 'm' : this.sample.mode == 'maj' ? 'M' : '')
            }

            return '-'
        }
    },

    async asyncData({ $axios, params, error }) {
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
            error({ statusCode: 404, message: 'Sample not found' })
        }
    },

    head () {
        return {
            title: this.sample.name
        }
    }
}
</script>

<style scoped>
a {
    text-decoration: none;
}
.v-image {
    border-radius: 100px;
    margin: 0 auto;
}
</style>
