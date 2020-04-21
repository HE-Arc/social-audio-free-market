<template>
    <main>
        <v-container>
            <v-text-field
                v-model="quickSearchInput"
                label="Quick Search"
                outlined
                hide-details
                single-line
                @keypress.enter="quickSearch"
            >
                <template v-slot:append>
                    <v-icon @click="quickSearch">{{ searchIcon }}</v-icon>
                </template>
            </v-text-field>
        </v-container>

        <v-container>
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="6"
                >
                    <Sample :sample="sample"/>
                </v-col>
            </v-row>
        </v-container>
    </main>
</template>

<script>
import Sample from '~/components/Sample.vue'

export default {
    components: {
        Sample
    },

    data () {
        return {
            quickSearchInput: '',
            samples: []
        }
    },

    computed: {
        searchIcon () {
            return this.quickSearchInput.length > 0 ? 'mdi-magnify' : ''
        }
    },

    methods: {
        async quickSearch () {
            try {
                if (this.quickSearchInput.length > 0) {
                    this.samples = await this.$axios.$get('/quick?search=' + this.quickSearchInput)
                }
            } catch (err) {
                console.log(err)
                this.samples = []
            }
        },
    },
}
</script>
