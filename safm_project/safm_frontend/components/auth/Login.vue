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
                                            v-model="username"
                                            label="Username"
                                            required
                                            autofocus
                                            :error-messages="usernameErrors"
                                            @blur="$v.username.$touch()"
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
        username: { required },
        password: { required },
    },

    data () {
        return {
            dialog: false,
            username: '',
            password: ''
        }
    },

    computed: {
        usernameErrors () {
            const errors = []
            if (!this.$v.username.$dirty) return errors
            !this.$v.username.required && errors.push('Username is required')

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
            body.set('username', this.username)
            body.set('password', this.password)

            const authToken = await this.$axios.post('/login', body)
                .then((response) => {
                    return response.data.token
                })
                .catch(() => {
                    return null
                })

            if (authToken) {
                this.$store.commit('setAuth', authToken)
                Cookie.set('auth', authToken)

                this.$store.commit('setUsername', this.username)
                Cookie.set('username', this.username)

                this.dialog = false
                this.$toast.success('Successfully logged in !', {
                    duration: 3000
                })
            } else {
                this.$toast.error('Invalid login', {
                    duration: 3000
                })
            }
        }
    }
}
</script>
