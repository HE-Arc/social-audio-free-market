<template>
    <div>
        <template>
            <form>
                <v-row align="center">
                    <v-col cols="6">
                        <v-text-field
                            v-model="params.name__icontains"
                            label="Name"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-text-field
                            v-model="params.user__username__icontains"
                            label="Username"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-range-slider
                            v-model="durationRange"
                            :min="durationMin"
                            :max="durationMax"
                            step=0.1
                            label="Duration [s]"
                            thumb-label="always"
                            @change="durationRangeOnChange"
                        ></v-range-slider>
                    </v-col>
                    <v-col cols="6">
                        <v-range-slider
                            v-model="tempoRange"
                            :min="tempoMin"
                            :max="tempoMax"
                            label="Tempo"
                            thumb-label="always"
                            @change="tempoRangeOnChange"
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
                                v-for="(tag, i) in params.tags__name__icontains"
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
                name__icontains: '',   // Sample name
                user__username__icontains: '',
                duration__gte: 0,
                duration__lte: 30.0,
                tempo__gte: 1,
                tempo__lte: 200,
                tone: [],   //RENAME TONE TO KEY
                mode: '',
                tags__name__icontains: []
            },
            durationRange: [0.1, 30.0],
            durationMin: 0.1,
            durationMax: 30.0,
            tempoRange: [1, 200],
            tempoMin: 1,
            tempoMax: 200,
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
        durationRangeOnChange () {
            this.params.duration__gte = this.durationRange[0]
            this.params.duration__lte = this.durationRange[1]
        },

        tempoRangeOnChange () {
            this.params.tempo__gte = this.tempoRange[0]
            this.params.tempo__lte = this.tempoRange[1]
        },

        addTag () {
            if (this.tagInput.length > 0) {
                if (! this.params.tags__name__icontains.includes(this.tagInput)) {
                    // Inserts tag at beginning of array
                    this.params.tags__name__icontains.splice(0, 0, this.tagInput)
                    this.tagInput = ''
                }
            }
        },

        removeTag (index) {
            this.params.tags__name__icontains.splice(index, 1)
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
