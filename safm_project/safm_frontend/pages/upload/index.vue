<template>
    <div>
        <v-container>
            <h2 class="page-title">Upload Sample</h2>
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

export default {
    middleware: 'authenticated',

    mixins: [validationMixin],

    validations: {
        file: { required },
        name: { required }
    },
    
    data () {
        return {
            file: [],
            name: '',
            description: '',
            key: '',
            keyItems: ['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G'],
            mode: '',
            modeItems: [
                {
                    text: '-',
                    value: 'None'
                },
                {
                    text: 'Minor',
                    value: 'min'
                },
                {
                    text: 'Major',
                    value: 'maj'
                }
            ],
            tagInput: '',
            tags: []
        }
    },

    computed: {
        addTagIcon () {
            return this.tagInput.length > 0 ? 'mdi-plus-circle-outline' : ''
        },

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

    methods: {
        async upload () {
            let body = new FormData()
            body.append('file', this.file)
            body.set('name', this.name)
            body.set('description', this.description)
            body.set('key', this.key)
            body.set('mode', this.mode)
            body.set('tags', this.tags)

            const sampleId = await this.$axios.post('/upload_sample', body, {
                headers: {
                    'Authorization': `Token ${this.$store.state.auth}`
                }
            })
                .then((response) => {
                    return response.data.id
                })
                .catch((error) => {
                    for (let e in error.response.data) {
                        this.$toast.error(error.response.data[e], {
                            duration: 5000
                        })
                    }

                    return null
                })

            // Redirects to the uploaded sample page
            if (sampleId) {
                this.$toast.success('Sample uploaded !', {
                    duration: 5000
                })
                this.$router.push(`/samples/${sampleId}`)
            }
        },

        addTag () {
            if (this.tagInput.length > 0) {
                if (! this.tags.includes(this.tagInput)) {
                    // Inserts tag at beginning of array
                    this.tags.splice(0, 0, this.tagInput)
                    this.tagInput = ''
                }
            } else {
                this.upload()
            }
        },

        removeTag (index) {
            this.tags.splice(index, 1)
        },
    }
}
</script>
