<template>
    <div>
        <v-dialog
            v-model="dialog"
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
                                            autofocus
                                            required
                                            @keypress.enter="login"
                                        ></v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-text-field
                                            v-model="password"
                                            label="Password"
                                            type="password"
                                            required
                                            @keypress.enter="login"
                                        ></v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-btn
                                            block
                                            large
                                            color="primary"
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
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
const Cookie = process.client ? require('js-cookie') : undefined

export default {
    data () {
        return {
            dialog: false,
            username: '',
            password: ''
        }
    },

    methods: {
        async login () {
            let body = new FormData()
            body.set('username', this.username)
            body.set('password', this.password)

            await this.$axios.post('/login', body)
                .then((response) => {
                    const authToken = response.data.token
                    this.$store.commit('setAuth', authToken)
                    Cookie.set('auth', authToken)

                    this.dialog = false
                    this.$toast.success('Successfully logged in !', {
                        theme: 'bubble',
                        duration: 3000
                    })
                })
                .catch((error) => {
                    this.password = ''
                    
                    this.$toast.error('Invalid login', {
                        theme: 'bubble',
                        duration: 3000
                    })
                })
        }
    }
}
</script>
