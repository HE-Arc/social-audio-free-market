<template>
    <div>
        <v-container>
            <h2 class="page-title">User Settings</h2>
            <section>
                <h3 class="section-title">Profile</h3>
                <form>
                    <v-row align="center">
                        <v-col cols="2">
                            <v-img
                                :src="profilePictureSrc"
                                :width="profilePictureSize"
                                :height="profilePictureSize"
                            ></v-img>
                        </v-col>
                        <v-col cols="10">
                            <v-file-input
                                v-model="profile_picture"
                                label="Profile picture"
                                show-size
                                prepend-icon="mdi-file-image"
                                accept="image/*"
                            ></v-file-input>
                        </v-col>
                        <v-col cols="12">
                            <v-textarea
                                v-model="description"
                                label="Description"
                            ></v-textarea>
                        </v-col>
                        <v-col cols="12">
                            <v-switch v-model="email_public">
                                <template v-slot:label>
                                    Public email address
                                </template>
                            </v-switch>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                block
                                x-large
                                color="accent"
                                @click="updateProfile"
                            >
                                Update Profile
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
            </section>
        </v-container>
    </div>
</template>

<script>
export default {
    middleware: 'authenticated',
    
    data () {
        return {
            profile_picture: [],
            description: '',
            email_public: '',
        }
    },

    computed: {
        profilePictureSrc () {
            return `${this.$axios.defaults.baseURL}/user/picture/${this.$store.state.user.id}`
        },

        profilePictureSize () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return '75px'
            case 'sm': return '100px'
            case 'md': return '125px'
            case 'lg': return '150px'
            case 'xl': return '175px'
            }
        }
    },

    async asyncData ({ $axios, store }) {
        try {
            const profile = await $axios.$get(`/user/profile/${store.state.user.id}`)

            return {
                description: profile.description,
                email_public: profile.email_public
            }
        } catch (e) {
            return {
                profile_picture: '',
                description: '',
                email_public: ''
            }
        }
    },

    methods: {
        async updateProfile () {
            let body = new FormData()

            if (this.profile_picture) {
                body.append('profile_picture', this.profile_picture)
            }

            if (this.description) {
                body.set('description', this.description)
            }

            body.set('email_public', this.email_public)

            try {
                await this.$axios.patch(`/user/profile/${this.$store.state.user.id}`, body)

                this.$nuxt.$emit('snackbar', 'Profile updated !')
            } catch (error) {
                this.$nuxt.$emit('snackbar', error)
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
