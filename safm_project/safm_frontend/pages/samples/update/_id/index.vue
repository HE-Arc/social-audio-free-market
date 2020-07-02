<template>
    <div>
        <v-container>
            <h2 class="page-title">Update Sample</h2>
            <form>
                <v-row align="center">
                    <v-col cols="12">
                        <v-text-field
                            v-model="name"
                            label="Name*"
                            required
                            :error-messages="nameErrors"
                            @blur="$v.name.$touch()"
                            @keypress.enter="upload"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-textarea
                            v-model="description"
                            label="Description"
                            @keypress.enter="upload"
                        ></v-textarea>
                    </v-col>
                    <v-col cols="6">
                        <v-select
                            v-model="key"
                            :items="keyItems"
                            label="Key"
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
                        <TagsField />
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            x-large
                            color="accent"
                            
                        >
                            Update
                        </v-btn>
                    </v-col>
                </v-row>
            </form>
        </v-container>
    </div>
</template>

<script>
import TagsField from '~/components/sample/TagsField'

export default {
    middleware: 'authenticated',
    
    components: {
        TagsField
    },

    data () {
        return {
            name: '',
            description: '',
            key: '',
            keyItems: ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G'],
            mode: '',
            modeItems: [
                { text: '-', value: 'None' },
                { text: 'Minor', value: 'min' },
                { text: 'Major', value: 'maj' }
            ],
            tags: [],
        }
    },

    mounted () {
        // On Tags Field update
        this.$nuxt.$on('updateTagsField', (tagsList) => {
            this.tags = tagsList
        })
    },

    async asyncData ({ $axios, params }) {
        try {
            const sample = await $axios.$get(`/sample/${params.id}`)

            return {
                file: sample.file,
                name: sample.name,
                description: sample.description,
                key: sample.key,
                mode: sample.mode,
                tags: sample.tags
            }
        } catch (e) {
            return {
                name: '',
                description: '',
                key: '',
                mode: '',
                tags: []
            }
        }
    },
}
</script>
