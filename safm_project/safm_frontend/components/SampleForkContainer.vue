<template>
    <div class="d-flex flex-row">
        <v-layout column fill-width>
            <div class="d-flex flex-column">
                <h3>Created with</h3>
                <div
                    v-for="(sample, i) in forkFrom"
                    :key="i"
                >
                    <SampleFork
                        :id="sample.id"
                        :name="sample.name"
                        :userId="sample.user.id"
                        :username="sample.user.username"
                    />
                </div>
            </div>
        </v-layout>
        <v-layout column fill-width>
            <div class="d-flex flex-column">
                <h3>Used by</h3>
                <div
                    v-for="(sample, i) in forkTo"
                    :key="i"
                >
                    <SampleFork
                        :id="sample.id"
                        :name="sample.name"
                        :userId="sample.user.id"
                        :username="sample.user.username"
                    />
                </div>
            </div>
        </v-layout>
    </div>
</template>

<script>
import SampleFork from '~/components/SampleFork.vue'

export default {
    components: {
        SampleFork
    },

    props: [
        'forkFrom',
        'forkTo'
    ]
}
</script>
