<template>
    <div>
        <v-container>
            <div v-if="sampleUserId == $store.state.user.id">
                <h1>Update Sample</h1>
                <form>
                    <v-row align="center">
                        <v-col cols="12">
                            <v-text-field
                                v-model="name"
                                label="Name"
                                required
                                @keypress.enter="update"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-textarea
                                v-model="description"
                                label="Description"
                                @keypress.enter="update"
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
                                @click="update"
                            >
                                Update
                            </v-btn>
                        </v-col>
                    </v-row>
                </form>
                <v-switch v-model="removeEnable" color="error">
                    <template v-slot:label>
                        Remove
                    </template>
                </v-switch>
                <v-btn
                    block
                    x-large
                    color="error"
                    @click="remove"
                    :disabled="!removeEnable"
                >
                    Remove
                </v-btn>
            </div>
            <div v-else>
                <ErrorDisplay title="You cannot edit this sample" />
            </div>
        </v-container>
    </div>
</template>

<script>
import TagsField from '~/components/sample/TagsField'
import ErrorDisplay from '~/components/ErrorDisplay.vue'

export default {
    middleware: 'authenticated',
    
    components: {
        TagsField,
        ErrorDisplay
    },

    data () {
        return {
            id: '',
            sampleUserId: '',
            name: '',
            description: '',
            key: '',
            keyItems: [{ text: '-', value: ' ' }, 'A', 'B', 'C', 'D', 'E', 'F', 'G'],
            mode: '',
            modeItems: [
                { text: '-', value: ' ' },
                { text: 'Minor', value: 'min' },
                { text: 'Major', value: 'maj' }
            ],
            tags: [],
            removeEnable: false
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
                id: sample.id,
                sampleUserId: sample.user.id,
                file: sample.file,
                name: sample.name,
                description: sample.description,
                key: sample.key,
                mode: sample.mode,
                tags: sample.tags
            }
        } catch (e) {
            return {
                id: '',
                sampleUserId: '',
                name: '',
                description: '',
                key: '',
                mode: '',
                tags: []
            }
        }
    },

    methods: {
        async update () {
            let body = new FormData()

            if (this.name) {
                body.set('name', this.name)
            }
            
            if (this.description) {
                body.set('description', this.description)
            }
            
            if (this.key) {
                body.set('key', this.key)
            }

            if (this.mode) {
                body.set('mode', this.mode)
            }
            
            if (this.tags) {
                body.set('tags', this.tags)
            }

            try {
                await this.$axios.patch(`/sample/${this.id}`, body)

                this.$nuxt.$emit('snackbar', 'Sample updated !')
                // Redirects to the uploaded sample page
                this.$router.push(`/sample/${this.id}`)
            } catch (error) {
                this.$nuxt.$emit('snackbar', this.$errorArrayToString(error.response.data))
            }
        },

        async remove () {
            const response = await this.$axios.delete(`/sample/${this.id}`)
            const detail = response.data.detail

            this.$nuxt.$emit('snackbar', detail)
            // Redirects to the user profile page
            this.$router.push(`/profile/${this.sampleUserId}`)
        }
    }
}
</script>
