<template>
    <div>
        <v-container>
            <h1>Create Account</h1>
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
                        />
                    </v-col>
                    <v-col cols="12">
                        <v-text-field
                            v-model="email"
                            label="Email"
                            required
                            :error-messages="emailErrors"
                            @blur="$v.email.$touch()"
                            @keypress.enter="register"
                        />
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
                        />
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
                        />
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            x-large
                            color="accent"
                            :loading="loading"
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
import { validationMixin } from 'vuelidate';
import { required, email, minLength, sameAs } from 'vuelidate/lib/validators';

export default {

    mixins: [validationMixin],
    middleware: 'unauthenticated',

    validations: {
        username: { required },
        email: { required, email },
        password: { required, minLength: minLength(8) },
        password_confirm: { required, minLength: minLength(8), sameAs: sameAs('password') }
    },

    data() {
        return {
            username: '',
            email: '',
            password: '',
            password_confirm: '',
            loading: false
        };
    },

    head() {
        return {
            title: 'Register'
        };
    },

    computed: {
        usernameErrors() {
            const errors = [];
            if (!this.$v.username.$dirty) { return []; }
            !this.$v.username.required && errors.push('Username is required');

            return errors;
        },

        emailErrors() {
            const errors = [];
            if (!this.$v.email.$dirty) { return []; }
            !this.$v.email.email && errors.push('Must be valid email');
            !this.$v.email.required && errors.push('Email is required');

            return errors;
        },

        passwordErrors() {
            const errors = [];
            if (!this.$v.password.$dirty) { return []; }
            !this.$v.password.required && errors.push('Password is required');
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters');

            return errors;
        },

        passwordConfirmErrors() {
            const errors = [];
            if (!this.$v.password_confirm.$dirty) { return []; }
            !this.$v.password_confirm.required && errors.push('Confirm Password is required');
            !this.$v.password_confirm.minLength && errors.push('Password Confirm must be at least 8 characters');
            !this.$v.password_confirm.sameAs && errors.push('Password confirmation does not match');

            return errors;
        }
    },

    methods: {
        // Creates an account
        async register() {
            if (!this.loading) {
                this.$v.$touch();

                if (!this.$v.$anyError) {
                    // Valid form
                    this.loading = true;

                    const body = new FormData();
                    body.set('username', this.username);
                    body.set('email', this.email);
                    body.set('password', this.password);
                    body.set('password_confirm', this.password_confirm);

                    try {
                        // Creates an account
                        const response = await this.$axios.post('/register', body);
                        const userid = this.$storeUserCredentials(response);
                        this.$nuxt.$emit('snackbar', 'Successful registration !');

                        // Redirects to the user profile page
                        this.$router.push(`/profile/${userid}`);
                    } catch (e) {
                        this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data));
                        this.loading = false;
                    }
                }
            }
        }
    }
};
</script>
