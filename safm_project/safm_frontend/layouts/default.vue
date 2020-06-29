<template>
    <v-app dark>
        <v-app-bar
            fixed
            app
        >
            <v-btn
                to="/"
                text
            >
                {{ title }}
            </v-btn>
            <v-spacer />
            <QuickSearch />
            <v-tooltip
                v-if="!$store.state.auth"
                bottom
            >
                <template v-slot:activator="{ on }">
                    <v-btn
                        fab
                        depressed
                        to="/login"
                        v-on="on"
                    >
                        <v-icon>mdi-login-variant</v-icon>
                    </v-btn>
                </template>
                <span>Login</span>
            </v-tooltip>
            <v-menu
                v-else
                open-on-hover
                offset-y
                transition="scale-transition"
            >
                <template v-slot:activator="{ on }">
                    <v-btn
                        v-on="on"
                        depressed
                        class="account-menu"
                    >
                        {{ username }}
                        <v-icon>mdi-menu-down</v-icon>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item-group>
                        <v-list-item
                            v-for="(item, i) in accountMenu"
                            :key="i"
                            @click="handleFunctionCall(item.method)"
                        >
                            <v-list-item-icon>
                                <v-icon>{{ item.icon }}</v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                                <v-list-item-title>{{ item.title }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-menu>
        </v-app-bar>
        <v-content>
            <v-container>
                <nuxt />
            </v-container>
        </v-content>
        <v-footer></v-footer>
        <v-snackbar
            v-model="snackbar"
            app
            :timeout="snackbarTimeout"
        >
            {{ snackbarText }}
            <v-btn
                text
                color="accent"
                @click="snackbar = false"
            >
                Close
            </v-btn>
        </v-snackbar>
    </v-app>
</template>

<script>
import QuickSearch from '~/components/QuickSearch.vue'
const Cookie = process.client ? require('js-cookie') : undefined

export default {
    components: {
        QuickSearch
    },

    data () {
        return {
            title: 'SAFMarket',
            accountMenu: [
                { icon: 'mdi-account', title: 'Profile', method: 'profile' },
                { icon: 'mdi-cloud-upload', title: 'Upload', method: 'upload' },
                { icon: 'mdi-logout', title: 'Logout', method: 'logout' }
            ],
            snackbar: false,
            snackbarText: '',
            snackbarTimeout: 3000
        }
    },

    computed: {
        isOffline () {
            return this.$nuxt.isOffline
        },

        userid () {
            return this.$store.state.user.id
        },

        username () {
            return this.$store.state.user.name
        }
    },

    mounted () {
        // On Snackbar
        this.$nuxt.$on('snackbar', (text) => {
            this.snackbarText = text
            this.snackbar = true
        })
    },

    watch: {
        isOffline () {
            const text = this.isOffline ? 'No Internet connection' : 'You are now online'
            this.$nuxt.$emit('snackbar', text)
        }
    },

    methods: {
        handleFunctionCall (functionName) {
            this[functionName]()
        },

        profile () {
            this.$router.push(`/profiles/${this.userid}`)
        },

        upload () {
            this.$router.push('/upload')
        },

        async logout () {
            try {
                await this.$axios.post('/logout')

                this.$store.commit('setAuth', null)
                Cookie.remove('auth')
                this.$store.commit('setUser', null)
                Cookie.remove('userid')
                Cookie.remove('username')

                this.$axios.setHeader('Authorization', '')

                this.$nuxt.$emit('snackbar', 'Successfully logged out !')
            } catch (error) {
                this.$nuxt.$emit('snackbar', 'An error occured')
            }
        }
    }
}
</script>

<style>
.account-menu {
    text-transform: none !important;
}

.page-title {
    font-size: 2.7em;
    text-align: center;
    margin: 0.5em 0;
}
section {
    padding: 3em 0;
}
.section-title {
    font-size: 2.3em;
    margin: 0 0 1em 0;
}

.custom-loader {
    animation: loader 1s infinite;
    display: flex;
}
@-moz-keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
@-webkit-keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
@-o-keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
@keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
