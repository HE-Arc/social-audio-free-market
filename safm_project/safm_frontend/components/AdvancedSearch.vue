<template>
    <form>
        <v-row align="center">
            <v-col cols="6">
                <v-text-field
                    v-model="params.name__icontains"
                    label="Name"
                    @keypress.enter="advancedSearch"
                ></v-text-field>
            </v-col>
            <v-col cols="6">
                <v-text-field
                    v-model="params.user__username__icontains"
                    label="Username"
                    @keypress.enter="advancedSearch"
                ></v-text-field>
            </v-col>
            <v-col cols="12">
                <v-card
                    flat
                    color="transparent"
                >
                    <v-subheader>Duration [s]</v-subheader>
                    <v-card-text>
                        <v-range-slider
                            v-model="durationRange"
                            :min="durationMin"
                            :max="durationMax"
                            step=0.1
                            thumb-label
                            @input="durationRangeOnChange"
                        >
                            <template v-slot:prepend>
                                <v-text-field
                                    :value="durationRange[0]"
                                    type="number"
                                    step=0.1
                                    class="mt-0 pt-0 range-text-field"
                                    @change="$set(durationRange, 0, $event)"
                                ></v-text-field>
                            </template>
                            <template v-slot:append>
                                <v-text-field
                                    :value="durationRange[1]"
                                    type="number"
                                    step=0.1
                                    class="mt-0 pt-0 range-text-field"
                                    @change="$set(durationRange, 1, $event)"
                                ></v-text-field>
                            </template>
                        </v-range-slider>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12">
                <v-card
                    flat
                    color="transparent"
                >
                    <v-subheader>Tempo</v-subheader>
                    <v-card-text>
                        <v-range-slider
                            v-model="tempoRange"
                            :min="tempoMin"
                            :max="tempoMax"
                            thumb-label
                            @input="tempoRangeOnChange"
                        >
                            <template v-slot:prepend>
                                <v-text-field
                                    :value="tempoRange[0]"
                                    type="number"
                                    class="mt-0 pt-0 range-text-field"
                                    @change="$set(tempoRange, 0, $event)"
                                ></v-text-field>
                            </template>
                            <template v-slot:append>
                                <v-text-field
                                    :value="tempoRange[1]"
                                    type="number"
                                    class="mt-0 pt-0 range-text-field"
                                    @change="$set(tempoRange, 1, $event)"
                                ></v-text-field>
                            </template>
                        </v-range-slider>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="6">
                <v-select
                    v-model="params.key"
                    :items="keyItems"
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
                <TagsField loadFromStore="true" />
            </v-col>
            <v-col cols="6">
                <v-select
                    v-model="ordering"
                    :items="orderingItems"
                    label="Order by"
                ></v-select>
            </v-col>
            <v-col cols="6">
                <v-switch
                    v-model="orderingReverse"
                    label="Reversed Order"
                ></v-switch>
            </v-col>
            <v-col cols="12">
                <v-btn
                    block
                    x-large
                    color="accent"
                    @click="advancedSearch"
                >
                    Search
                </v-btn>
            </v-col>
        </v-row>
    </form>
</template>

<script>
import TagsField from '~/components/sample/TagsField'

export default {
    components: {
        TagsField
    },

    data () {
        return {
            // Advanced Search GET request params
            params: {
                name__icontains: '',   // Sample name
                user__username__icontains: '',
                duration__gte: 0,
                duration__lte: 30.0,
                tempo__gte: 1,
                tempo__lte: 200,
                key: [],
                mode: '',
                tags__name__icontains: []
            },
            durationRange: [0.1, 30.0],
            durationMin: 0.1,
            durationMax: 30.0,
            tempoRange: [1, 200],
            tempoMin: 1,
            tempoMax: 200,
            keyItems: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            modeItems: [
                { text: 'Any', value: '' },
                { text: 'Minor', value: 'min' },
                { text: 'Major', value: 'maj' }
            ],
            ordering: '',
            orderingItems: [
                { text: 'Name', value: 'name' },
                { text: 'Username', value: 'user__username' },
                { text: 'Duration', value: 'duration' },
                { text: 'Tempo', value: 'tempo' },
                { text: 'Key', value: 'key' }
            ],
            orderingReverse: false
        }
    },

    mounted () {
        this.restoreState()

        // On Tags Field update
        this.$nuxt.$on('updateTagsField', (tagsList) => {
            this.params.tags__name__icontains = tagsList
        })
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

        advancedSearch () {
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

            // Removes the last '&' character
            params = params.substring(0, params.length - 1)

            // There is an order by property set
            if (this.ordering) {
                params += `&ordering=${this.orderingReverse ? '-' : ''}${this.ordering}`
            }

            this.saveState()

            //FIXME: How to preserve the form inputs values ?
            this.$router.push(`/advanced-search/${params}`)
        },

        saveState () {
            this.$store.commit('setAdvancedSearchParams', {...this.params})
            this.$store.commit('setAdvancedSearchOrdering', this.ordering)
            this.$store.commit('setAdvancedSearchOrderingReverse', this.orderingReverse)
        },

        restoreState () {
            this.params = {...this.$store.state.advancedSearchParams}
            this.durationRange = [this.params.duration__gte, this.params.duration__lte]
            this.tempoRange = [this.params.tempo__gte, this.params.tempo__lte]
            this.ordering = this.$store.state.advancedSearchOrdering
            this.orderingReverse = this.$store.state.advancedSearchOrderingReverse
        }
    }
}
</script>

<style scoped>
.range-text-field {
    width: 60px;
}
</style>
