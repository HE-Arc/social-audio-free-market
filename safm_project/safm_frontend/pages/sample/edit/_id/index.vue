<template>
    <div>
        <v-container>
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
                            :loading="loadingUpdate"
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
                :loading="loadingRemove"
                @click="remove"
                :disabled="!removeEnable"
            >
                Remove
            </v-btn>
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
            loadingUpdate: false,
            removeEnable: false,
            loadingRemove: false
        }
    },

    mounted () {
        // On Tags Field update
        this.$nuxt.$on('updateTagsField', (tagsList) => {
            this.tags = tagsList
        })
    },

    async asyncData ({ $axios, params, error, store }) {
        try {
            const sample = await $axios.$get(`/sample/${params.id}`)
            
            if (sample.user.id != store.state.user.id) {
                error({ statusCode: 401, message: 'Unauthorised to update this sample' })
            }
            
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
            error({ statusCode: 404, message: 'Sample not found' })
        }
    },

    head () {
        return {
            title: `Edit ${this.name}`
        }
    },

    methods: {
        async update () {
            if (!this.loadingUpdate) {
                this.loadingUpdate = true

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
                } catch (e) {
                    this.$nuxt.$emit('snackbar', this.$errorArrayToString(e.response.data))
                    this.loadingUpdate = false
                }
            }
        },

        async remove () {
            if (!this.loadingRemove) {
                this.loadingRemove = true

                try {
                    const response = await this.$axios.delete(`/sample/${this.id}`)
                    const detail = response.data.detail

                    this.$nuxt.$emit('snackbar', detail)
                    // Redirects to the user profile page
                    this.$router.push(`/profile/${this.sampleUserId}`)
                } catch (e) {
                    this.$nuxt.$emit('snackbar', 'An error occured')
                    this.loadingRemove = true
                }
            }
        }
    }
}
</script>
