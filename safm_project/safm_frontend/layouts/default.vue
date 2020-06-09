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
            <Login v-if="!$store.state.auth" />
            <v-menu
                v-else
                open-on-hover
                offset-y
            >
                <template v-slot:activator="{ on }">
                    <v-btn
                        v-on="on"
                        depressed
                        class="account-menu"
                        :to="`/profiles/${$store.state.username}`"
                    >
                        <v-icon>mdi-account</v-icon>
                        {{ username }}
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
        <v-footer
            app
        >
            <v-container>
                <!--v-row>
                    <v-col cols="4">
                        <v-switch
                            :v-model="`this.$store.state.repeatSample`"
                            :prepend-icon="repeatIcon"
                            @change="repeatSampleOnToggle"
                        ></v-switch>
                    </v-col>
                </v-row-->
            </v-container>
        </v-footer>
    </v-app>
</template>

<script>
import QuickSearch from '~/components/QuickSearch.vue'
import Login from '~/components/auth/Login.vue'
const Cookie = process.client ? require('js-cookie') : undefined

export default {
    components: {
        QuickSearch,
        Login
    },

    data () {
        return {
            title: 'SAFMarket',
            accountMenu: [
                { icon: 'mdi-cloud-upload', title: 'Upload', method: 'upload' },
                { icon: 'mdi-logout', title: 'Logout', method: 'logout' }
            ]
        }
    },

    computed: {
        username () {
            return this.$store.state.username
        },

        /*
        repeatIcon () {
            return this.$store.state.repeatSample ? 'mdi-repeat' : 'mdi-repeat-off'
        }
        */
    },

    methods: {
        /*
        repeatSampleOnToggle () {
            this.$store.commit('toggleRepeatSample')
        },
        */

        handleFunctionCall (functionName) {
            this[functionName]()
        },

        upload () {
            this.$router.push('/upload')
        },

        async logout () {
            await this.$axios.post('/logout', {}, {
                headers: {
                    'Authorization': `Token ${this.$store.state.auth}`
                }
            })
                .then(() => {
                    this.$store.commit('setAuth', null)
                    Cookie.remove('auth')
                    Cookie.remove('username')
                    
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
