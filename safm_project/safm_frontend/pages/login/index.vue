<template>
    <div>
        <v-container>
            <h2 class="page-title">Login</h2>
            <form>
                <v-row align="center">
                    <v-col cols="12">
                        <v-text-field
                            v-model="usernameEmail"
                            label="Username / Email"
                            required
                            :error-messages="usernameEmailErrors"
                            @blur="$v.usernameEmail.$touch()"
                            @keypress.enter="login"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-text-field
                            v-model="password"
                            label="Password"
                            type="password"
                            required
                            :error-messages="passwordErrors"
                            @blur="$v.password.$touch()"
                            @keypress.enter="login"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            large
                            color="accent"
                            :loading="loading"
                            @click="login"
                        >
                            Login
                        </v-btn>
                    </v-col>
                </v-row>
            </form>
            <v-layout align-center>
                <v-flex class="text-center">
                    <v-btn
                        text
                        to="/register"
                    >
                        Register
                    </v-btn>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
    middleware: 'unauthenticated',

    mixins: [validationMixin],

    validations: {
        usernameEmail: { required },
        password: { required },
    },

    data () {
        return {
            usernameEmail: '',
            password: '',
            loading: false
        }
    },

    computed: {
        usernameEmailErrors () {
            const errors = []
            if (!this.$v.usernameEmail.$dirty) return errors
            !this.$v.usernameEmail.required && errors.push('Username / Email is required')

            return errors
        },

        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push('Password is required')

            return errors
        }
    },

    methods: {
        async login () {
            if (!this.loading) {
                this.$v.$touch()

                if (!this.$v.$anyError) {
                    this.loading = true

                    let body = new FormData()

                    // Checks wether the usernameEmail field is an email address
                    const re = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
                    if (re.test(this.usernameEmail)) {
                        body.set('email', this.usernameEmail)
                    } else {
                        body.set('username', this.usernameEmail)
                    }

                    body.set('password', this.password)

                    try {
                        const response = await this.$axios.post('/login', body)
                        this.$storeUserCredentials(response)
                        this.$nuxt.$emit('snackbar', 'Successfully logged in !')

                        // Redirects to the last visited page
                        this.$router.go(-1)
                    } catch (error) {
                        this.$nuxt.$emit('snackbar', 'Invalid login')
                        this.loading = false
                    }
                }
            }
        }
    }
}
</script>
