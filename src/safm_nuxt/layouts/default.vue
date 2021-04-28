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
            <v-btn
                v-if="!$store.state.auth"

                depressed
                to="/login"
            >
                <v-icon>mdi-login-variant</v-icon>
                <span class="ml-2">Login</span>
            </v-btn>
            <v-menu
                v-else
                offset-y
            >
                <template #activator="{ on }">
                    <v-btn
                        depressed
                        class="account-menu"
                        v-on="on"
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
                    <p>
                        <v-icon large class="mt-4">
                            mdi-github
                        </v-icon>
                    </p>
                    <v-btn
                        text
                        small
                        color="primary"
                        href="https://github.com/HE-Arc/social-audio-free-market"
                        target="_blank"
                        rel="noopener"
                    >
                        View project on Github
                    </v-btn>
                </v-card-text>
                <v-divider />
                <v-card-text>
                    {{ new Date().getFullYear() }} - <strong>Social Audio Free Market</strong>
                </v-card-text>
            </v-card>
        </v-footer>
        <v-snackbar
            v-model="snackbar"
            app
            top
            multi-line
            :timeout="snackbarTimeout"
        >
            {{ snackbarText }}
            <template #action="{ attrs }">
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
import QuickSearch from '~/components/QuickSearch.vue';

export default {
    components: {
        QuickSearch
    },

    data() {
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
        };
    },

    computed: {
        isOffline() {
            return this.$nuxt.isOffline;
        },

        userid() {
            return this.$store.state.user.id;
        },

        username() {
            return this.$store.state.user.name;
        }
    },

    watch: {
        isOffline() {
            // Emits a snackbar event whenever the application connection state changes
            const text = this.isOffline ? 'No Internet connection' : 'You are now online';
            this.$nuxt.$emit('snackbar', text);
        }
    },

    mounted() {
        // On Snackbar
        this.$nuxt.$on('snackbar', (text) => {
            // Displays the snackbar with the given message
            this.snackbarText = text;
            this.snackbar = true;
        });
    },

    methods: {
        // Goes to the home page
        home() {
            this.$router.push('/');
        },

        // Calls a method by its name
        // This allows function names in the data object for the menu
        handleFunctionCall(functionName) {
            this[functionName]();
        },

        // Goes to the upload sample page
        upload() {
            this.$router.push('/upload');
        },

        // Goes to the user profile page
        profile() {
            this.$router.push(`/profile/${this.userid}`);
        },

        // Goes to the user liked samples page
        likes() {
            this.$router.push('/likes');
        },

        // Goes to the user settings page
        settings() {
            this.$router.push('/profile/edit');
        },

        // Logout
        async logout() {
            try {
                // Logs out the user
                await this.$axios.post('/logout');
                // Removes the user credentials from the store and the cookies
                this.$deleteUserCredentials();

                this.$nuxt.$emit('snackbar', 'Successfully logged out !');

                // Refreshes the current page
                // This avoids staying on a protected page when not logged in
                this.$router.go(this.$nuxt.$route.path);
            } catch (e) {
                this.$nuxt.$emit('snackbar', 'An error occured');
            }
        }
    }
};
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
