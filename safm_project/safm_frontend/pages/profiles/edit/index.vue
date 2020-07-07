<template>
    <div>
        <v-container>
            <h1>User Settings</h1>
            <section>
                <h2>Profile</h2>
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
                                large
                                color="accent"
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
                <form>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="username"
                                label="Username"
                                required
                                :error-messages="usernameErrors"
                                @blur="$v.username.$touch()"
                                @keypress.enter="updateUsername"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                large
                                color="accent"
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
                <form>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="email"
                                label="Email"
                                type="email"
                                required
                                :error-messages="emailErrors"
                                @blur="$v.email.$touch()"
                                @keypress.enter="updateEmail"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                large
                                color="accent"
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
                <form>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="password_current"
                                label="Current Password"
                                type="password"
                                required
                                :error-messages="passwordCurrentErrors"
                                @blur="$v.password_current.$touch()"
                                @keypress.enter="updatePassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="password"
                                label="New Password"
                                type="password"
                                required
                                :error-messages="passwordErrors"
                                @blur="$v.password.$touch()"
                                @keypress.enter="updatePassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="password_confirm"
                                label="Confirm Password"
                                type="password"
                                required
                                :error-messages="passwordConfirmErrors"
                                @blur="$v.password_confirm.$touch()"
                                @keypress.enter="updatePassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                large
                                color="accent"
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
import { required, email, minLength } from 'vuelidate/lib/validators'

export default {
    middleware: 'authenticated',

    mixins: [validationMixin],

    validations: {
        username: { required },
        email: { required, email },
        password_current: { required, minLength: minLength(8) },
        password: { required, minLength: minLength(8) },
        password_confirm: { required, minLength: minLength(8) }
    },
    
    data () {
        return {
            profile_picture: [],
            description: '',
            email_public: '',
            username: '',
            email: '',
            password_current: '',
            password: '',
            password_confirm: ''
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
        },

        usernameErrors () {
            const errors = []
            if (!this.$v.username.$dirty) return errors
            !this.$v.username.required && errors.push('Username is required')

            return errors
        },

        emailErrors () {
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid email')
            !this.$v.email.required && errors.push('Email is required')

            return errors
        },

        passwordCurrentErrors () {
            const errors = []
            if (!this.$v.password_current.$dirty) return errors
            !this.$v.password_current.required && errors.push('Current Password is required')
            !this.$v.password_current.minLength && errors.push('Current Password must be at least 8 characters')

            return errors
        },

        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push('New Password is required')
            !this.$v.password.minLength && errors.push('New Password must be at least 8 characters')

            return errors
        },
        
        passwordConfirmErrors () {
            const errors = []
            if (!this.$v.password_confirm.$dirty) return errors
            !this.$v.password_confirm.required && errors.push('Confirm Password is required')
            !this.$v.password_confirm.minLength && errors.push('Confirm Password must be at least 8 characters')

            return errors
        }
    },

    async asyncData ({ $axios, store }) {
        try {
            const profile = await $axios.$get(`/user/profile/${store.state.user.id}`)
            const email = await $axios.$get(`/user/email/${store.state.user.id}`)

            return {
                description: profile.description,
                email_public: profile.email_public,
                username: profile.user.username,
                email: email.email
            }
        } catch (e) {
            return {
                profile_picture: '',
                description: '',
                email_public: '',
                username: '',
                email: ''
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
                this.$nuxt.$emit('snackbar', this.$errorArrayToString(error.response.data))
            }
        },

        async updateUser (body, snackbarMessage) {
            try {
                const response = await this.$axios.patch(`/user/${this.$store.state.user.id}`, body)

                this.$nuxt.$emit('snackbar', snackbarMessage)

                return response.data
            } catch (error) {
                this.$nuxt.$emit('snackbar', this.$errorArrayToString(error.response.data))
                return null
            }
        },

        async updateUsername () {
            this.$v.username.$touch()

            if (!this.$v.username.$invalid) {
                let body = new FormData()
                body.set('username', this.username)

                const response = await this.updateUser(body, 'Username updated !')
                if (response) {
                    this.$updateUsername(response.username)
                }
            }
        },

        async updateEmail () {
            this.$v.email.$touch()

            if (!this.$v.email.$invalid) {
                let body = new FormData()
                body.set('email', this.email)

                this.updateUser(body, 'Email updated !')
            }
        },

        async updatePassword () {
            this.$v.password_current.$touch()
            this.$v.password.$touch()
            this.$v.password_confirm.$touch()

            if (!this.$v.password_current.$invalid &&
                !this.$v.password.$invalid &&
                !this.$v.password_confirm.$invalid) {
                let body = new FormData()
                body.set('password_current', this.password_current)
                body.set('password', this.password)
                body.set('password_confirm', this.password_confirm)

                this.updateUser(body, 'Password updated !')
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
