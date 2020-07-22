<template>
    <v-app dark>
        <v-app-bar
            fixed
            app
        >
            <v-btn
                text
                @click="home"
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
                offset-y
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
        <v-main>
            <v-container>
                <nuxt />
            </v-container>
        </v-main>
        <v-footer padless class="mt-12">
            <v-card
                flat
                class="text-center v-card-footer"
            >
                <v-card-text>
                    <p>Bachelor project developed at the Haute-École ARC, Switzerland.</p>
                    <v-btn
                        x-large
                        icon
                        color="primary"
                        href="https://github.com/HE-Arc/social-audio-free-market"
                        target="_blank"
                    >
                        <v-icon>mdi-github</v-icon>
                    </v-btn>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-text>
                    {{ new Date().getFullYear() }} - <strong>Social Audio Free Market</strong>
                </v-card-text>
            </v-card>
        </v-footer>
        <v-snackbar
            app
            v-model="snackbar"
            top
            multi-line
            :timeout="snackbarTimeout"
        >
            {{ snackbarText }}
            <template v-slot:action="{ attrs }">
                <v-btn
                    text
                    color="accent"
                    v-bind="attrs"
                    @click="snackbar = false"
                >
                    Close
                </v-btn>
            </template>
        </v-snackbar>
    </v-app>
</template>

<script>
import QuickSearch from '~/components/QuickSearch.vue'

export default {
    components: {
        QuickSearch
    },

    data () {
        return {
            title: 'SAFMarket',
            accountMenu: [
                { icon: 'mdi-cloud-upload', title: 'Upload', method: 'upload' },
                { icon: 'mdi-account', title: 'Profile', method: 'profile' },
                { icon: 'mdi-heart', title: 'Likes', method: 'likes' },
                { icon: 'mdi-cogs', title: 'Settings', method: 'settings' },
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
        home () {
            this.$router.push('/')
        },

        handleFunctionCall (functionName) {
            this[functionName]()
        },

        upload () {
            this.$router.push('/upload')
        },

        profile () {
            this.$router.push(`/profile/${this.userid}`)
        },
        
        likes () {
            this.$router.push('/likes')
        },

        settings () {
            this.$router.push('/profile/edit')
        },

        async logout () {
            try {
                await this.$axios.post('/logout')
                this.$deleteUserCredentials()

                this.$nuxt.$emit('snackbar', 'Successfully logged out !')

                // Refreshes the current page
                // This avoids staying on a protected page when not logged in
                this.$router.go(this.$nuxt.$route.path)
            } catch (e) {
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
h1 {
    font-size: 2.7em;
    text-align: center;
    margin: 0.5em 0;
}
h2 {
    font-size: 2.3em;
    margin: 0 0 1em 0;
}
h3 {
    font-size: 1.8em;
    margin: 0 0 0.7em 0;
}
section {
    padding: 3em 0;
}
.v-card-footer {
    width: 100%;
}
</style>
