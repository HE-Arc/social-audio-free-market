<template>
    <div>
        <v-container>
            <h1>Request password reset</h1>
            <form @submit.prevent>
                <v-row>
                    <v-col cols="12">
                        <v-text-field
                            v-model="email"
                            label="Email*"
                            required
                            type="email"
                            :error-messages="emailErrors"
                            @blur="$v.email.$touch()"
                            @keypress.enter="requestResetPassword"
                        />
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            x-large
                            color="accent"
                            :loading="loading"
                            @click="requestResetPassword"
                        >
                            Request Email
                        </v-btn>
                    </v-col>
                </v-row>
            </form>
        </v-container>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate';
import { required, email } from 'vuelidate/lib/validators';

export default {

    mixins: [validationMixin],
    middleware: 'unauthenticated',

    validations: {
        email: { required, email }
    },

    data() {
        return {
            email: '',
            loading: false
        };
    },

    head() {
        return {
            title: 'Request Reset Password'
        };
    },

    computed: {
        emailErrors() {
            const errors = [];
            if (!this.$v.email.$dirty) { return []; }
            !this.$v.email.email && errors.push('Must be valid email');
            !this.$v.email.required && errors.push('Email is required');

            return errors;
        }
    },

    methods: {
        // Requests a password reset email
        async requestResetPassword() {
            if (!this.loading) {
                this.$v.$touch();

                if (!this.$v.$anyError) {
                    // Valid form
                    this.loading = true;

                    const body = new FormData();
                    body.set('email', this.email);

                    try {
                        // Requests a password reset email
                        const response = await this.$axios.$post('/password_reset/', body);
                        const status = response.status;

                        if (status === 'OK') {
                            this.$nuxt.$emit('snackbar', 'An email has been sent to you');
                            this.email = '';

                            // Redirects to the home page
                            this.$router.push('/');
                        } else {
                            this.$nuxt.$emit('snackbar', 'An error occured');
                        }
                    } catch (e) {
                        this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data));
                    }

                    this.$v.$reset();
                    this.loading = false;
                }
            }
        }
    }
};
</script>
