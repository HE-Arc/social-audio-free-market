<template>
    <v-app dark>
        <v-app-bar
            fixed
            app
        >
            <nuxt-link to="/" >
                <v-toolbar-title v-text="title" />
            </nuxt-link>
            <v-spacer />
            <QuickSearch />
            <Login v-if="!$store.state.auth" />
            <Logout v-else />
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
                <v-row>
                    <v-col cols="4">
                        <v-switch
                            :v-model="`this.$store.state.repeatSample`"
                            :prepend-icon="repeatIcon"
                            @change="repeatSampleOnToggle"
                        ></v-switch>
                    </v-col>
                </v-row>
            </v-container>
        </v-footer>
    </v-app>
</template>

<script>
import QuickSearch from '~/components/QuickSearch.vue'
import Login from '~/components/auth/Login.vue'
import Logout from '~/components/auth/Logout.vue'

export default {
    components: {
        QuickSearch,
        Login,
        Logout
    },

    data () {
        return {
            title: 'SAFMarket'
        }
    },

    computed: {
        repeatIcon () {
            return this.$store.state.repeatSample ? 'mdi-repeat' : 'mdi-repeat-off'
        }
    },

    methods: {
        repeatSampleOnToggle () {
            this.$store.commit('toggleRepeatSample')
        }
    }
}
</script>
