<template>
    <div>
        <v-dialog
            v-model="dialog"
            max-width="600"
            light
        >
            <template v-slot:activator="{ on }">
                <v-btn
                    v-on="on"
                    fab
                    depressed
                >
                    <v-icon>mdi-login-variant</v-icon>
                </v-btn>
            </template>
            <v-card>
                <v-card-title
                    class="headline"
                >
                    Login
                </v-card-title>
                <v-card-text>
                    <div v-if="!$store.state.auth">
                        <v-container>
                            <form>
                                <v-row align="center">
                                    <v-col cols="12">
                                        <v-text-field
                                            v-model="usernameEmail"
                                            label="Username / Email"
                                            required
                                            autofocus
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
                                            @click="login"
                                        >
                                            Login
                                        </v-btn>
                                    </v-col>
                                </v-row>
                            </form>
                        </v-container>
                    </div>
                    <div v-else>
                        You are already logged in.
                    </div>
                </v-card-text>
                <v-card-text>
                    <v-container>
                        <v-layout align-center>
                            <v-flex class="text-center">
                                <v-btn
                                    text
                                    to="/register"
                                    @click="dialog = !dialog"
                                >
                                    Register
                                </v-btn>
                            </v-flex>
                        </v-layout>
                    </v-container>
                </v-card-text>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required/*, email*/ } from 'vuelidate/lib/validators'
const Cookie = process.client ? require('js-cookie') : undefined

export default {
    middleware: 'unauthenticated',

    mixins: [validationMixin],

    validations: {
        usernameEmail: { required },
        password: { required },
    },

    data () {
        return {
            dialog: false,
            usernameEmail: '',
            password: ''
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
                const authToken = response.data.token
                const username = response.data.username

                this.$store.commit('setAuth', authToken)
                Cookie.set('auth', authToken)

                this.$store.commit('setUsername', username)
                Cookie.set('username', username)

                this.$axios.setHeader('Authorization', `Token ${authToken}`)

                this.dialog = false
                this.$nuxt.$emit('snackbar', 'Successfully logged in !')
            } catch (error) {
                this.$nuxt.$emit('snackbar', 'Invalid login')
            }
        }
    }
}
</script>
