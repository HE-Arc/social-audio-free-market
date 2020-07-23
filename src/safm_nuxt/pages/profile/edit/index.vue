<template>
    <div>
        <v-container>
            <h1>User Settings</h1>
            <section>
                <h2>Profile</h2>
                <form @submit.prevent>
                    <v-row align="center">
                        <v-col cols="4" sm="2" md="3">
                            <v-img
                                :src="profilePictureSrc"
                                :width="profilePictureSize"
                                :height="profilePictureSize"
                            ></v-img>
                        </v-col>
                        <v-col cols="8"sm="10" md="9">
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
                                outlined
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
                                large
                                color="accent"
                                :loading="loadingProfile"
                                @click="updateProfile"
                            >
                                Update Profile
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
            </section>
            <section>
                <h3 class="section-title">Username</h3>
                <form @submit.prevent>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="formUsername.username"
                                label="Username"
                                required
                                :error-messages="usernameErrors"
                                @blur="$v.formUsername.username.$touch()"
                                @keypress.enter="updateUsername"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                large
                                color="accent"
                                :loading="loadingUsername"
                                @click="updateUsername"
                            >
                                Update Username
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
            </section>
            <section>
                <h2>Email</h2>
                <form @submit.prevent>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="formEmail.email"
                                label="Email"
                                type="email"
                                required
                                :error-messages="emailErrors"
                                @blur="$v.formEmail.email.$touch()"
                                @keypress.enter="updateEmail"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                large
                                color="accent"
                                :loading="loadingEmail"
                                @click="updateEmail"
                            >
                                Update Email
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
            </section>
            <section>
                <h2>Password</h2>
                <form @submit.prevent>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="formPassword.password_current"
                                label="Current Password"
                                type="password"
                                required
                                :error-messages="passwordCurrentErrors"
                                @blur="$v.formPassword.password_current.$touch()"
                                @keypress.enter="updatePassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="formPassword.password"
                                label="New Password"
                                type="password"
                                required
                                :error-messages="passwordErrors"
                                @blur="$v.formPassword.password.$touch()"
                                @keypress.enter="updatePassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="formPassword.password_confirm"
                                label="Confirm Password"
                                type="password"
                                required
                                :error-messages="passwordConfirmErrors"
                                @blur="$v.formPassword.password_confirm.$touch()"
                                @keypress.enter="updatePassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                large
                                color="accent"
                                :loading="loadingPassword"
                                @click="updatePassword"
                            >
                                Update Password
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
            </section>
        </v-container>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email, minLength, sameAs, not } from 'vuelidate/lib/validators'

export default {
    middleware: 'authenticated',

    mixins: [validationMixin],

    validations: {
        formUsername: {
            username: { required },
        },
        formEmail: {
            email: { required, email },
        },
        formPassword: {
            password_current: { required, minLength: minLength(8) },
            password: { required, minLength: minLength(8), notSameAs: not(sameAs('password_current')) },
            password_confirm: { required, minLength: minLength(8), sameAs: sameAs('password') }
        }
    },
    
    data () {
        return {
            profile_picture: null,
            description: '',
            email_public: '',
            loadingProfile: false,
            formUsername: {
                username: '',
            },
            loadingUsername: false,
            formEmail: {
                email: '',
            },
            loadingEmail: false,
            formPassword: {
                password_current: '',
                password: '',
                password_confirm: '',
            },
            loadingPassword: false
        }
    },

    computed: {
        profilePictureSrc () {
            return `${this.$axios.defaults.baseURL}/user/picture/${this.$store.state.user.id}`
        },

        profilePictureSize () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return '75px'
            case 'sm': return '90px'
            case 'md': return '125px'
            case 'lg': return '150px'
            case 'xl': return '175px'
            }
        },

        usernameErrors () {
            const errors = []
            if (!this.$v.formUsername.username.$dirty) return []
            !this.$v.formUsername.username.required && errors.push('Username is required')

            return errors
        },

        emailErrors () {
            const errors = []
            if (!this.$v.formEmail.email.$dirty) return []
            !this.$v.formEmail.email.email && errors.push('Must be valid email')
            !this.$v.formEmail.email.required && errors.push('Email is required')

            return errors
        },

        passwordCurrentErrors () {
            const errors = []
            if (!this.$v.formPassword.password_current.$dirty) return []
            !this.$v.formPassword.password_current.required && errors.push('Current Password is required')
            !this.$v.formPassword.password_current.minLength && errors.push('Current Password must be at least 8 characters')

            return errors
        },

        passwordErrors () {
            const errors = []
            if (!this.$v.formPassword.password.$dirty) return []
            !this.$v.formPassword.password.required && errors.push('New Password is required')
            !this.$v.formPassword.password.minLength && errors.push('New Password must be at least 8 characters')
            !this.$v.formPassword.password.notSameAs && errors.push('New Password must be different than the current one')

            return errors
        },
        
        passwordConfirmErrors () {
            const errors = []
            if (!this.$v.formPassword.password_confirm.$dirty) return []
            !this.$v.formPassword.password_confirm.required && errors.push('Confirm Password is required')
            !this.$v.formPassword.password_confirm.minLength && errors.push('Confirm Password must be at least 8 characters')
            !this.$v.formPassword.password_confirm.sameAs && errors.push('Password confirmation does not match')

            return errors
        }
    },

    async asyncData ({ $axios, error, store }) {
        try {
            const profile = await $axios.$get(`/user/profile/${store.state.user.id}`)
            const email = await $axios.$get(`/user/email/${store.state.user.id}`)

            if (profile.user.id != store.state.user.id) {
                //Only  the user can update its account information and profile
                error({ statusCode: 401, message: 'Unauthorised to update this user profile' })
            }

            return {
                description: profile.description,
                email_public: profile.email_public,
                formUsername: {
                    username: profile.user.username,
                },
                formEmail: {
                    email: email.email
                }
            }
        } catch (e) {
            error({ statusCode: 404, message: 'User profile not found' })
        }
    },

    head () {
        return {
            title: 'Edit Profile'
        }
    },

    methods: {
        // Updates the user profile
        async updateProfile () {
            if (!this.loadingProfile) {
                this.loadingProfile = true

                let body = new FormData()
                
                // Verifications to avoid giving empty values
                if (this.profile_picture) {
                    body.append('profile_picture', this.profile_picture)
                }

                if (this.description) {
                    body.set('description', this.description)
                }

                body.set('email_public', this.email_public)

                try {
                    // Updates the profile
                    await this.$axios.patch(`/user/profile/${this.$store.state.user.id}`, body)

                    this.$nuxt.$emit('snackbar', 'Profile updated !')
                } catch (e) {
                    this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data))
                }

                this.loadingProfile = false

                // Refreshes the page to get the new image
                if (this.profile_picture) {
                    this.$router.go(this.$nuxt.$route.path)
                }
            }
        },

        // Updates the user account information based on the given form data
        // and then triggers a snackbar event with the given message
        async updateUser (body, snackbarMessage) {
            try {
                const response = await this.$axios.patch(`/user/${this.$store.state.user.id}`, body)

                this.$nuxt.$emit('snackbar', snackbarMessage)

                return response.data
            } catch (e) {
                this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data))
                return null
            }
        },

        // Updates the username
        async updateUsername () {
            if (!this.loadingUsername) {
                this.$v.formUsername.$touch()

                if (!this.$v.formUsername.$anyError) {
                    // Valid input
                    this.loadingUsername = true

                    let body = new FormData()
                    body.set('username', this.formUsername.username)

                    // Updates the username
                    const response = await this.updateUser(body, 'Username updated !')
                    if (response) {
                        // Updates the username in the store
                        this.$updateUsername(response.username)
                    }

                    this.loadingUsername = false
                }
            }
        },

        // Updates the user email address
        async updateEmail () {
            if (!this.loadingEmail) {
                this.$v.formEmail.$touch()

                if (!this.$v.formEmail.$anyError) {
                    // Valid input
                    this.loadingEmail = true

                    let body = new FormData()
                    body.set('email', this.formEmail.email)

                    // Updates the user email address
                    this.updateUser(body, 'Email updated !')

                    this.loadingEmail = false
                }
            }
        },

        // Updates the user password
        async updatePassword () {
            if (!this.loadingPassword) {
                this.$v.formPassword.$touch()

                if (!this.$v.formPassword.$anyError) {
                    // Valid form
                    this.loadingProfile = true

                    let body = new FormData()
                    body.set('password_current', this.formPassword.password_current)
                    body.set('password', this.formPassword.password)
                    body.set('password_confirm', this.formPassword.password_confirm)

                    // Updates the user password
                    await this.updateUser(body, 'Password updated !')

                    // Resets the password form fields
                    this.formPassword.password_current = ''
                    this.formPassword.password = ''
                    this.formPassword.password_confirm = ''
                    this.$v.formPassword.$reset()

                    this.loadingProfile = false
                }
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
