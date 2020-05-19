<template>
    <div>
        <template>
            <form>
                <v-row align="center">
                    <v-col cols="6">
                        <v-text-field
                            v-model="params.name"
                            label="Name"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-text-field
                            v-model="params.user__username"
                            label="Username"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-range-slider
                            v-model="durationRange"
                            :min="params.duration_gte"
                            :max="params.duration_lte"
                            step=0.1
                            label="Duration [s]"
                            thumb-label="always"
                        ></v-range-slider>
                    </v-col>
                    <v-col cols="6">
                        <v-range-slider
                            v-model="tempoRange"
                            :min="params.tempo_gte"
                            :max="params.tempo_lte"
                            label="Tempo"
                            thumb-label="always"
                        ></v-range-slider>
                    </v-col>
                    <v-col cols="6">
                        <v-select
                            v-model="params.tone"
                            :items="toneItems"
                            label="Key"
                            multiple
                        ></v-select>
                    </v-col>
                    <v-col cols="6">
                        <v-select
                            v-model="params.mode"
                            :items="modeItems"
                            label="Mode"
                        ></v-select>
                    </v-col>
                    <v-col cols="12">
                        <v-text-field
                            v-model="tagInput"
                            label="Add a tag"
                            @keypress.enter="addTag"
                        >
                            <template v-slot:append>
                                <v-icon @click="addTag">{{ addTagIcon }}</v-icon>
                            </template>
                        </v-text-field>
                        <v-chip-group>
                            <v-chip
                                v-for="(tag, i) in params.tags__name"
                                :key="tag"
                                close
                                @click:close="removeTag(i)"
                            >
                                {{ tag }}
                            </v-chip>
                        </v-chip-group>
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            large
                            color="primary"
                            @click="advancedSearch"
                        >
                            Search
                        </v-btn>
                    </v-col>
                </v-row>
            </form>
        </template>
        <div class="search-results">
            <v-row>
                <v-col
                    v-for="sample in samples"
                    :key="sample.id"
                    cols="6"
                >
                    <Sample :sample="sample" />
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>
import Sample from '~/components/Sample.vue'

export default {
    components: {
        Sample
    },

    data () {
        return {
            // Advanced Search params
            params: {
                name: '',   // Sample name
                user__username: '',
                duration_gte: 0.1,
                duration_lte: 30.0,
                tempo_gte: 1,
                tempo_lte: 200,
                tone: [],   //RENAME TONE TO KEY
                mode: '',
                tags__name: []
            },
            durationRange: [0.1, 30.0],
            tempoRange: [1, 200],
            toneItems: ['A', 'B', 'C'], // FETCH TONES FROM API
            modeItems: ['Any', 'Minor', 'Major'],
            tagInput: '',
            samples: []
        }
    },

    computed: {
        addTagIcon () {
            return this.tagInput.length > 0 ? 'mdi-plus-circle-outline' : ''
        }
    },
    
    methods: {
        addTag () {
            if (this.tagInput.length > 0) {
                if (! this.params.tags__name.includes(this.tagInput)) {
                    // Inserts tag at beginning of array
                    this.params.tags__name.splice(0, 0, this.tagInput)
                    this.tagInput = ''
                }
            }
        },

        removeTag (index) {
            this.params.tags.splice(index, 1)
        },

        async advancedSearch () {
            let params = ''

            for (let [key, value] of Object.entries(this.params)) {
                // The param has a value
                if (value) {
                    // The param is an array
                    if (typeof(value) === 'object') {
                        for (let index in value) {
                            params += `${key}=${value[index]}&`
                        }
                    // The param is an input
                    } else {
                        params += `${key}=${value}&`
                    }
                }
            }

            // Removes the last '&'
            params = params.substring(0, params.length - 1)
            
            try {
                this.samples = await this.$axios.$get('/ad_search?' + params)
            } catch (e) {
                this.samples = []
            }
        }
    }
}
</script>
