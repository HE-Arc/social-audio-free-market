<template>
    <div class="sample-list">
        <v-row>
            <v-col
                v-for="sample in samples"
                :key="sample.id"
                cols="3"
                md="4"
                sm="6"
                xs="12"
            >
                <SampleCard
                    :id="sample.id"
                    :name="sample.name"
                    :tempo="sample.tempo"
                    :_key="sample.key"
                    :mode="sample.mode"
                    :duration="sample.duration"
                    :tags="sample.tags"
                    :username="sample.user.username"
                />
            </v-col>
        </v-row>
    </div>
</template>

<script>
import SampleCard from '~/components/SampleCard.vue'

export default {
    components: {
        SampleCard
    },

    props: ['samples']
}
</script>
