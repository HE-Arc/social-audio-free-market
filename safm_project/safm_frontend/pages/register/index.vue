<template>
    <div>
        <v-container>
            <h2 class="page-title">Create Account</h2>
            <form id="register-form">
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
                            type="password"
                            required
                            :error-messages="passwordErrors"
                            @blur="$v.password.$touch()"
                            @keypress.enter="register"
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
                            @keypress.enter="register"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            x-large
                            color="accent"
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
        password_confirm: { required }
    },
    
    data () {
        return {
            username: '',
            email: '',
            password: '',
            password_confirm: ''
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
        },
        
        passwordConfirmErrors () {
            const errors = []
            if (!this.$v.password_confirm.$dirty) return errors
            !this.$v.password_confirm.required && errors.push('Confirm Password is required')

            return errors
        }
    },

    methods: {
        async register () {
            let body = new FormData()
            body.set('username', this.username)
            body.set('email', this.email)
            body.set('password', this.password)
            body.set('password_confirm', this.password_confirm)

            try {
                const response = await this.$axios.post('/register', body)
                const authToken = response.data.token
                const username = response.data.username

                this.$store.commit('setAuth', authToken)
                Cookie.set('auth', authToken)

                this.$store.commit('setUsername', username)
                Cookie.set('username', username)

                this.$axios.setHeader('Authorization', `Token ${authToken}`)

                this.dialog = false
                this.$nuxt.$emit('snackbar', 'Successful registration !')
                // Redirects to the home page
                this.$router.push('/')
            } catch (error) {
                this.$nuxt.$emit('snackbar', error.response.data)
                /*
                for (let e in error.response.data) {

                    this.$toast.error(`${e}: ${error.response.data[e]}`, {
                        duration: 5000
                    })
                }
                */
            }
        }
    }
}
</script>
