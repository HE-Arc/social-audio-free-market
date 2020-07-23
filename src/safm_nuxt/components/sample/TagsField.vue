<template>
    <div>
        <v-text-field
            v-model="tagInput"
            label="Add a tag"
            :error-messages="tagInputErrors"
            @keypress.enter="addTag"
        >
            <template v-slot:append>
                <v-icon @click="addTag">{{ addTagIcon }}</v-icon>
            </template>
        </v-text-field>
        <v-chip-group>
            <v-chip
                v-for="(tag, i) in tagsList"
                :key="i"
                close
                @click:close="removeTag(i)"
            >
                {{ tag }}
            </v-chip>
        </v-chip-group>
    </div>
</template>

<script>
export default {
    props: ['tags', 'loadFromStore'],

    data () {
        return {
            // Copy to avoid mutating props
            tagsList: this.tags ? [...this.tags] : [],
            tagInput: '',
            tagInputErrors: ''
        }
    },

    computed: {
        addTagIcon () {
            return this.tagInput.length > 0 ? 'mdi-plus-circle-outline' : ''
        }
    },

    mounted () {
        if (this.loadFromStore) {
            // Fetches the tags list from the store
            this.tagsList = [...this.$store.state.advancedSearchParams.tags__name__icontains]
        }
    },

    methods: {
        // Adds a tag to the tags list
        addTag () {
            // Converts all characters to lower cases
            this.tagInput = this.tagInput.toLowerCase()
            
            if (/^[a-z]+[a-z0-9]+$/.test(this.tagInput)) {
                // Tag validation
                if (!this.tagsList.includes(this.tagInput)) {
                    // Inserts tag at beginning of array
                    this.tagsList.splice(0, 0, this.tagInput)
                    this.tagInput = ''
                    this.$nuxt.$emit('updateTagsField', this.tagsList)
                    this.tagInputErrors = ''
                } else {
                    // The tag is already in the tags list
                    this.tagInputErrors = 'Tag already added'
                }
            } else {
                // Invalid tag
                this.tagInputErrors = 'Invalid tag: only letters and numbers, at least two characters and must begin with a letter'
            }
        },

        // Removes the tag at the given index from the tags list
        removeTag (index) {
            this.tagsList.splice(index, 1)
            this.$nuxt.$emit('updateTagsField', this.tagsList)
        }
    }
}
</script>
