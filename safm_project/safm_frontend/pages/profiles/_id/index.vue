<template>
    <div>
        <v-container>
            <v-img
                :src="profilePictureSrc"
                :width="profilePictureSize"
                :height="profilePictureSize"
            ></v-img>
            <h2 class="page-title">{{ username }}</h2>
            <v-row>
                <v-col
                    cols="12"
                    sm="3"
                    md="2"
                >
                    <v-card>
                        <v-card-actions class="justify-center">
                            <v-icon class="mr-1">mdi-music-note</v-icon>
                            <span class="mr-2">{{ numberSamples }}</span>
                            <span class="mr-1">·</span>
                            <v-icon class="mr-1">mdi-account-multiple</v-icon>
                            <span>-</span>
                        </v-card-actions>
                        <v-card-actions class="justify-center">
                            <v-btn
                                small
                                color="accent"
                                disabled
                            >
                                <v-icon class="mr-1">mdi-account-plus</v-icon>
                                Follow
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <v-col
                    cols="12"
                    sm="9"
                    md="10"
                >
                    <v-card>
                        <v-card-text class="px-6 body-1">
                            {{ profile.description }}
                        </v-card-text>
                        <div v-if="profile.email_public">
                            <v-divider class="mx-6"></v-divider>
                            <v-card-text class="px-6 body-2">
                                <v-icon>mdi-email-outline</v-icon>
                                <span class="mx-2">{{ userEmail }}</span>
                            </v-card-text>
                        </div>
                        <v-divider class="mx-6"></v-divider>
                        <v-card-text class="px-6 body-2">
                            {{ `Joined on ${new Date(dateJoined).toLocaleDateString()}` }}
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
        <section>
            <v-container>
                <h3 class="section-title">User Samples</h3>
                <SampleList :samples="samples" />
            </v-container>
        </section>
    </div>
</template>

<script>
import SampleList from '~/components/SampleList.vue'

export default {
    components: {
        SampleList
    },

    data () {
        return {
            username: '',
            profile: {},
            userEmail: '',
            dateJoined: '',
            samples: []
        }
    },

    computed: {
        profilePictureSrc () {
            return `${this.$axios.defaults.baseURL}/user/picture/${this.profile.user.id}`
        },

        profilePictureSize () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return '150px'
            case 'sm': return '175px'
            case 'md': return '200px'
            case 'lg': return '225px'
            case 'xl': return '250px'
            }
        },

        numberSamples () {
            return this.samples.length
        }
    },

    async asyncData({ $axios, params }) {
        try {
            const profile = await $axios.$get(`/user/profile/${params.id}`)
            const samples = await $axios.$get(`/user/samples/${params.id}`)

            let userEmail = ''
            if (profile.email_public) {
                const response = await $axios.$get(`/user/email/${params.id}`)
                userEmail = response.email
            }

            return {
                username: profile.user.username,
                profile: profile,
                userEmail: userEmail,
                dateJoined: profile.user.date_joined,
                samples: samples
            }
        } catch (e) {
            return {
                username: '',
                userProfile: {},
                userEmail: '',
                dateJoined: '',
                samples: []
            }
        }
    }
}
</script>

<style scoped>
.v-image {
    border-radius: 200px;
    margin: 0 auto;
}
</style>
