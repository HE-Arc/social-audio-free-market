<template>
    <div class="d-flex flex-row">
        <v-layout column fill-width>
            <div class="d-flex flex-column">
                <div>Created with</div>
                <div
                    v-for="(sample, i) in forkFrom"
                    :key="i"
                >
                    <SampleFork
                        :id="sample.sample_from.id"
                        :name="sample.sample_from.name"
                        :userId="sample.sample_from.user.id"
                        :username="sample.sample_from.user.username"
                    />
                </div>
            </div>
        </v-layout>
        <v-layout column fill-width>
            <div class="d-flex flex-column">
                <div>Used by</div>
                <div
                    v-for="(sample, i) in forkTo"
                    :key="i"
                >
                    <SampleFork
                        :id="sample.sample_to.id"
                        :name="sample.sample_to.name"
                        :userId="sample.sample_to.user.id"
                        :username="sample.sample_to.user.username"
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
