<template>
    <div>
        <v-container>
            <form>
                <v-row align="center">
                    <v-col cols="12">
                        <v-text-field
                            v-model="username"
                            label="Username"
                            required
                            :error-messages="usernameErrors"
                            @blur="$v.username.$touch()"
                            @keypress.enter="register"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-text-field
                            v-model="email"
                            label="Email"
                            required
                            :error-messages="emailErrors"
                            @blur="$v.email.$touch()"
                            @keypress.enter="register"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-text-field
                            v-model="password"
                            label="Password"
                            required
                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="showPassword ? 'text' : 'password'"
                            @click:append="showPassword = !showPassword"
                            :error-messages="passwordErrors"
                            @blur="$v.password.$touch()"
                            @keypress.enter="register"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            large
                            color="primary"
                            @click="register"
                        >
                            Register
                        </v-btn>
                    </v-col>
                </v-row>
            </form>
        </v-container>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
const Cookie = process.client ? require('js-cookie') : undefined

export default {
    middleware: 'unauthenticated',

    mixins: [validationMixin],

    validations: {
        username: { required },
        email: { required, email },
        password: { required },
    },
    
    data () {
        return {
            username: '',
            email: '',
            password: '',
            showPassword: false
        }
    },

    computed: {
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

        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push('Password is required')

            return errors
        }
    },

    methods: {
        async register () {
            let body = new FormData()
            body.set('username', this.username)
            body.set('email', this.email)
            body.set('password', this.password)

            const authToken = await this.$axios.post('/register', body)
                .then((response) => {
                    return response.data.token
                })
                .catch((error) => {
                    for (let e in error.response.data) {
                        this.$toast.error(error.response.data[e], {
                            duration: 5000
                        })
                    }

                    return null
                })

            if (authToken) {
                this.$store.commit('setAuth', authToken)
                Cookie.set('auth', authToken)

                this.dialog = false
                this.$toast.success('Successful registration !', {
                    duration: 3000
                })

                this.$router.push('/')
            }
        }
    }
}
</script>
