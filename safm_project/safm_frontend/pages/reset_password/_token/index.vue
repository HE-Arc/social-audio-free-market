<template>
    <div>
        <v-container>
            <h1>Reset password</h1>
            <div v-if="tokenIsValid">

            </div>
            <div v-else>
                <p align="center">This token is no longer valid.</p>
                <p align=center>
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
export default {
    middleware: 'unauthenticated',

    data () {
        return {
            tokenIsValid: ''
        }
    },

    async asyncData ({ $axios, params, error }) {
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
    }
}
</script>
