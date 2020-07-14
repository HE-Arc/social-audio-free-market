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
                            outlined
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
                        <TagsField :tags="tags" />
                    </v-col>
                    <v-row>
                        <v-col cols="12">
                            <p>Sample created with:</p>
                        </v-col>
                        <v-col
                            v-for="fork in forksFrom"
                            :key="fork.id"
                            cols="12"
                            sm="6"
                            md="4"
                            lg="3"
                        >
                            <SampleFork
                                :id="fork.id"
                                :name="fork.name"
                                :username="fork.user.username"
                                checkbox
                                checked
                            />
                        </v-col>
                        <v-col cols="12">
                            <SearchSampleFork />
                        </v-col>
                        <v-col
                            v-for="fork in searchForkResults"
                            :key="fork.id"
                            cols="12"
                            sm="6"
                            md="4"
                            lg="3"
                        >
                            <SampleFork
                                :id="fork.id"
                                :name="fork.name"
                                :username="fork.user.username"
                                addable
                            />
                        </v-col>
                    </v-row>
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
import SampleFork from '~/components/SampleFork.vue'
import SearchSampleFork from '~/components/sample/SearchSampleFork.vue'

export default {
    middleware: 'authenticated',
    
    components: {
        TagsField,
        SampleFork,
        SearchSampleFork
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
            forksFrom: [],
            searchForkResults: [],
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

        // On Fork checkbox change
        this.$nuxt.$on('forkCheckbox', (forkId, selected) => {
            if (selected) {
                this.forksFromId.push(forkId)
            } else {
                const index = this.forksFromId.indexOf(forkId)
                this.forksFromId.splice(index, 1)
            }
        })

        // On Search Forks event
        this.$nuxt.$on('searchForks', (results) => {
            this.searchForkResults = []

            // Filters the results
            for (let fork of results) {
                let forkId = fork.id

                // Current fork is different from this page sample
                if (forkId != this.id) {
                    for (let forkFrom of this.forksFrom) {
                        // Current fork is not already a fork from this page sample
                        if (forkFrom.id == forkId) {
                            forkId = -1
                            break
                        }
                    }

                    if (forkId > 0) {
                        this.searchForkResults.push(fork)
                    }
                }
            }
        })

        // On Fork Add event
        this.$nuxt.$on('forkAdd', (id) => {
            for (let i = 0; i < this.searchForkResults.length; i++) {
                let forkFromId = this.searchForkResults[i].id

                if (forkFromId == id) {
                    this.forksFrom.push(this.searchForkResults[i])
                    this.forksFromId.push(forkFromId)
                    this.searchForkResults.splice(i, 1)
                }
            }
        })
    },

    async asyncData ({ $axios, params, error, store }) {
        try {
            const sample = await $axios.$get(`/sample/${params.id}`)
            
            if (sample.user.id != store.state.user.id) {
                error({ statusCode: 401, message: 'Unauthorised to update this sample' })
            }

            const forksFrom = await $axios.$get(`/forks/from/${params.id}`)

            // Converts the tags objects into an array of tags names (string)
            let tags = []
            for (let tag of sample.tags) {
                tags.push(tag.name)
            }

            // Array of forks from ID
            let forksFromId = []
            for (let fork of forksFrom) {
                forksFromId.push(fork.id)
            }
            
            return {
                id: sample.id,
                sampleUserId: sample.user.id,
                file: sample.file,
                name: sample.name,
                description: sample.description,
                key: sample.key,
                mode: sample.mode,
                tags: tags,
                forksFrom: forksFrom,
                forksFromId: forksFromId
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

                if (this.forksFromId) {
                    body.set('forks_from', this.forksFromId)
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
