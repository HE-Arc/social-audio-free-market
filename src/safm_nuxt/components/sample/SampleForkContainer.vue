<template>
    <v-row>
        <v-col cols="12" md="6">
            <v-row>
                <v-col cols="12">
                    <h3>Created with</h3>
                </v-col>
                <v-col
                    cols="12"
                    sm="6"
                    v-for="(sample, i) in forkFrom"
                    :key="i"
                >
                    <SampleFork
                        :id="sample.id"
                        :name="sample.name"
                        :userId="sample.user.id"
                        :username="sample.user.username"
                    />
                </v-col>
            </v-row>
        </v-col>
        <v-col cols="12" md="6">
            <v-row>
                <v-col cols="12">
                    <h3>Used by</h3>
                </v-col>
                <v-col
                    cols="12"
                    sm="6"
                    v-for="(sample, i) in forkTo"
                    :key="i"
                >
                    <SampleFork
                        :id="sample.id"
                        :name="sample.name"
                        :userId="sample.user.id"
                        :username="sample.user.username"
                    />
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
import SampleFork from '~/components/sample/SampleFork.vue'

export default {
    components: {
        SampleFork
    },

    props: [
        'forkFrom',
        'forkTo'
    ],

    computed: {
        flexOrientation () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return 'row'
            case 'sm': return 'row'
            case 'md': return 'column'
            case 'lg': return 'column'
            case 'xl': return 'column'
            }
        }
    }
}
</script>
