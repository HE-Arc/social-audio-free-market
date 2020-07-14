<template>
    <div>
        <v-container>
            <h1>Reset password</h1>
            <div v-if="tokenIsValid">
                <form @submit.prevent>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                v-model="password"
                                label="Password"
                                type="password"
                                required
                                :error-messages="passwordErrors"
                                @blur="$v.password.$touch()"
                                @keypress.enter="resetPassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="password_confirm"
                                label="Password Confirm"
                                type="password"
                                required
                                :error-messages="passwordConfirmErrors"
                                @blur="$v.password_confirm.$touch()"
                                @keypress.enter="resetPassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-btn
                                block
                                x-large
                                color="accent"
                                :loading="loading"
                                @click="resetPassword"
                            >
                                Reset Password
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
            </div>
            <div v-else>
                <p class="text-center">This token is no longer valid.</p>
                <p class=text-center>
                    <v-btn
                        to="/reset_password"
                        color="accent"
                    >
                        Request a new one
                    </v-btn>
                </p>
            </div>
        </v-container>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, minLength, sameAs } from 'vuelidate/lib/validators'

export default {
    middleware: 'unauthenticated',

    mixins: [validationMixin],

    validations: {
        password: { required, minLength: minLength(8) },
        password_confirm: { required, minLength: minLength(8), sameAs: sameAs('password') }
    },

    data () {
        return {
            tokenIsValid: '',
            password: '',
            password_confirm: '',
            loading: false
        }
    },

    computed: {
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return []
            !this.$v.password.required && errors.push('Password is required')
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters')

            return errors
        },
        
        passwordConfirmErrors () {
            const errors = []
            if (!this.$v.password_confirm.$dirty) return []
            !this.$v.password_confirm.required && errors.push('Confirm Password is required')
            !this.$v.password_confirm.minLength && errors.push('Password Confirm must be at least 8 characters')
            !this.$v.password_confirm.sameAs && errors.push('Password confirmation does not match')

            return errors
        }
    },

    async asyncData ({ $axios, params }) {
        try {
            const response = await $axios.$post('/password_reset/validate_token/', { token: params.token })
            const status = response.status
            
            if (status == 'OK') {
                return { tokenIsValid: true }
            }

            return { tokenIsValid: false }
        } catch (e) {
            return { tokenIsValid: false }
        }
    },

    head () {
        return {
            title: 'Reset Password'
        }
    },

    methods: {
        async resetPassword() {
            if (!this.loading) {
                this.$v.$touch()

                if (!this.$v.$anyError) {
                    this.loading = true

                    let body = new FormData()
                    body.set('password', this.password)
                    body.set('token', this.$route.params.token)

                    try {
                        const response = await this.$axios.$post('/password_reset/confirm/', body)
                        const status = response.status

                        if (status == 'OK') {
                            this.$nuxt.$emit('snackbar', 'Your password has been reset !')
                            this.password = ''
                            this.password_confirm = ''
                            // Redirects to the home page
                            //FIXME: Not working ; causes an infinite loop
                            //this.$router.push('/')
                        } else {
                            this.$nuxt.$emit('snackbar', 'An error occured')
                        }
                    } catch (e) {
                        this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data))
                    }

                    this.$v.$reset()
                    this.loading = false
                }
            }
        }
    }
}
</script>
