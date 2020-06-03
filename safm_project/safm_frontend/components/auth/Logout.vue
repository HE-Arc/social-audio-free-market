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
                    <v-icon>mdi-logout-variant</v-icon>
                </v-btn>
            </template>
            <v-card>
                <v-card-title
                    class="headline"
                >
                    Logout ?
                </v-card-title>
                <v-card-text>
                    <div v-if="$store.state.auth">
                        <v-container>
                            <v-btn
                                block
                                large
                                color="error"
                                @click="logout"
                            >
                                Logout
                            </v-btn>
                        </v-container>
                    </div>
                    <div v-else>
                        You are not logged in.
                    </div>
                </v-card-text>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
const Cookie = process.client ? require('js-cookie') : undefined

export default {
    middleware: 'authenticated',

    data () {
        return {
            dialog: false
        }
    },

    methods: {
        async logout () {
            await this.$axios.post('/logout', {}, {
                headers: {
                    'Authorization': `Token ${this.$store.state.auth}`
                }
            })
                .then(() => {
                    this.$store.commit('setAuth', null)
                    Cookie.remove('auth')
                    
                    this.$toast.success('Successfully logged out !', {
                        duration: 3000
                    })
                })
                .catch(() => {
                    this.$toast.global.error()
                })
        }
    }
}
</script>
