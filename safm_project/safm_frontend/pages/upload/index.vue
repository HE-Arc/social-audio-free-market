<template>
    <div>
        <v-container>
            <h1>Upload Sample</h1>
            <form id="sample-upload-form">
                <v-row align=center>
                    <v-col cols="12">
                        <v-file-input
                            v-model="file"
                            label="File*"
                            show-size
                            prepend-icon="mdi-file-music"
                            required
                            accept="audio/*"
                            :error-messages="fileErrors"
                            @blur="$v.file.$touch()"
                            @keypress.enter="upload"
                        ></v-file-input>
                    </v-col>
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
                        <v-checkbox
                            v-model="selectedForkFrom"
                            v-for="(downloaded, i) in downloadedSamples"
                            :key="i"
                            :value="downloaded.sample.id"
                        >
                            <template v-slot:label>
                                <SampleFork
                                    :id="downloaded.sample.id"
                                    :name="downloaded.sample.name"
                                    :username="downloaded.sample.user.username"
                                    :downloaded_datetime="downloaded.datetime_download"
                                />
                            </template>
                        </v-checkbox>
                    </v-col>
                    <v-col cols="12">
                        <v-btn
                            block
                            x-large
                            color="accent"
                            @click="upload"
                        >
                            Upload
                        </v-btn>
                    </v-col>
                </v-row>
            </form>
        </v-container>
    </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import TagsField from '~/components/sample/TagsField'
import SampleFork from '~/components/SampleFork.vue'

export default {
    middleware: 'authenticated',

    mixins: [validationMixin],

    validations: {
        file: { required },
        name: { required }
    },

    components: {
        TagsField,
        SampleFork
    },
    
    data () {
        return {
            file: [],
            name: '',
            description: '',
            key: '',
            keyItems: [{ text: '-', value: '' }, 'A', 'B', 'C', 'D', 'E', 'F', 'G'],
            mode: '',
            modeItems: [
                { text: '-', value: '' },
                { text: 'Minor', value: 'min' },
                { text: 'Major', value: 'maj' }
            ],
            tags: [],
            selectedForkFrom: [],
            downloadedSamples: []
        }
    },

    computed: {
        fileErrors () {
            const errors = []
            if (!this.$v.file.$dirty) return errors
            !this.$v.file.required && errors.push('File is required')

            return errors
        },

        nameErrors () {
            const errors = []
            if (!this.$v.name.$dirty) return errors
            !this.$v.name.required && errors.push('Name is required')

            return errors
        }
    },

    mounted () {
        // On Tags Field update
        this.$nuxt.$on('updateTagsField', (tagsList) => {
            this.tags = tagsList
        })
    },

    async asyncData ({ $axios }) {
        try {
            let downloadedSamples = await $axios.$get('/user/downloads')

            return { downloadedSamples }
        } catch (e) {
            return { downloadedSamples: [] }
        }
    },

    methods: {
        async upload () {
            this.$v.file.$touch()
            this.$v.name.$touch()

            if (!this.$v.file.$invalid && !this.$v.name.$invalid) {
                let body = new FormData()
                body.append('file', this.file)
                body.set('name', this.name)
                
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
                
                if (this.selectedForkFrom) {
                    body.append('forks_from', this.selectedForkFrom)
                }
                
                try {
                    const response = await this.$axios.post('/sample', body)
                    const sampleId = response.data.id

                    this.$nuxt.$emit('snackbar', 'Sample uploaded !')
                    // Redirects to the uploaded sample page
                    this.$router.push(`/samples/${sampleId}`)
                } catch (error) {
                    this.$nuxt.$emit('snackbar', this.$errorArrayToString(error.response.data))
                }
            }
        }
    }
}
</script>
