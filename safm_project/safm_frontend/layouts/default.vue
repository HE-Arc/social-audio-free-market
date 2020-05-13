<template>
    <v-app dark>
        <v-app-bar
            fixed
            app
        >
            <nuxt-link
                to="/"
            >
                <v-toolbar-title v-text="title" />
            </nuxt-link>
            <v-spacer />
            <QuickSearch />
        </v-app-bar>
        <v-content>
            <v-container>
                <nuxt />
            </v-container>
        </v-content>
        <v-footer
            app
        >
            <span>&copy; {{ new Date().getFullYear() }}</span>
        </v-footer>
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
            title: 'SAFMarket'
        }
    }
}
</script>
