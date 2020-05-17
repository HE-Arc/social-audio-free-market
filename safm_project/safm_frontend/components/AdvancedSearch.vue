<template>
    <form>
        <v-row align="center">
            <v-col cols="6">
                <v-text-field
                    v-model="sampleName"
                    label="Sample Name"
                ></v-text-field>
            </v-col>
            <v-col cols="6">
                <v-text-field
                    v-model="username"
                    label="Username"
                ></v-text-field>
            </v-col>
            <v-col cols="6">
                <v-range-slider
                    v-model="durationRange"
                    :min="duration_gte"
                    :max="duration_lte"
                    step=0.1
                    label="Duration [s]"
                    thumb-label="always"
                ></v-range-slider>
            </v-col>
            <v-col cols="6">
                <v-range-slider
                    v-model="tempoRange"
                    :min="tempo_gte"
                    :max="tempo_lte"
                    label="Tempo"
                    thumb-label="always"
                ></v-range-slider>
            </v-col>
            <v-col cols="6">
                <v-select
                    v-model="tone"
                    :items="toneItems"
                    label="Key"
                    multiple
                ></v-select>
            </v-col>
            <v-col cols="6">
                <v-select
                    v-model="mode"
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
                        v-for="(tag, i) in tags"
                        :key="tag"
                        close
                        @click:close="removeTag(i)"
                    >
                        {{ tag }}
                    </v-chip>
                </v-chip-group>
            </v-col>
        </v-row>
    </form>
</template>

<script>
export default {

    data () {
        return {
            duration_gte: 0.1,
            duration_lte: 30.0,
            durationRange: [0.1, 30.0],
            tempo_gte: 1,
            tempo_lte: 200,
            tempoRange: [1, 200],
            tone: '',   //RENAME TONE TO KEY
            toneItems: ['A', 'B', 'C'], // FETCH TONES FROM API
            mode: '',
            modeItems: ['Any', 'Minor', 'Major'],
            tagInput: '',
            tags: []
        }
    },

    computed: {
        addTagIcon () {
            return this.tagInput.length > 0 ? 'mdi-plus-circle-outline' : ''
        }
    },
    
    methods: {
        addTag() {
            if (this.tagInput.length > 0) {
                if (! this.tags.includes(this.tagInput)) {
                    // Inserts tag at beginning of array
                    this.tags.splice(0, 0, this.tagInput)
                    this.tagInput = ''
                }
            }
        },

        removeTag (index) {
            this.tags.splice(index, 1)
        }
    }
}
</script>
