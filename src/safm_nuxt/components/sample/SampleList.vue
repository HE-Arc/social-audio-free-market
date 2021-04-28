<template>
    <div>
        <div class="sample-list">
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="12"
                    lg="3"
                    md="4"
                    sm="6"
                >
                    <SampleCard
                        :id="sample.id"
                        :name="sample.name"
                        :tempo="sample.tempo"
                        :_key="sample.key"
                        :_mode="sample.mode"
                        :duration="sample.duration"
                        :tags="sample.tags"
                        :user-id="sample.user.id"
                        :username="sample.user.username"
                    />
                </v-col>
            </v-row>
        </div>
        <v-btn
            fab
            fixed
            bottom
            right
            :disabled="stopAllDisabled"
            color="error"
            @click="stopAll"
        >
            <v-icon>mdi-stop</v-icon>
        </v-btn>
    </div>
</template>

<script>
import SampleCard from '~/components/sample/SampleCard.vue';

export default {
    components: {
        SampleCard
    },

    props: ['samples'],

    data() {
        return {
            numberPlaying: 0
        };
    },

    computed: {
        stopAllDisabled() {
            return this.numberPlaying < 1;
        }
    },

    mounted() {
        // On sample play
        this.$nuxt.$on('samplePlay', () => {
            ++this.numberPlaying;
        });

        // On sample pause
        this.$nuxt.$on('samplePause', () => {
            --this.numberPlaying;
        });
    },

    methods: {
        // On stop all button click
        stopAll() {
            this.$nuxt.$emit('sampleStopAll');
        }
    }
};
</script>

<style>
.sample .v-btn__content {
    text-transform: none !important;
}
</style>
