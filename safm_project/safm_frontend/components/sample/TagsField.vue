<template>
    <div>
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
    props: ['tags'],

    data () {
        return {
            tagsList: this.tags ? this.tags : [],
            tagInput: ''
        }
    },

    computed: {
        addTagIcon () {
            return this.tagInput.length > 0 ? 'mdi-plus-circle-outline' : ''
        }
    },

    methods: {
        addTag () {
            if (this.tagInput.length > 0) {
                if (! this.tagsList.includes(this.tagInput)) {
                    // Inserts tag at beginning of array
                    this.tagsList.splice(0, 0, this.tagInput)
                    this.tagInput = ''
                    this.$nuxt.$emit('updateTagsField', this.tagsList)
                }
            }
        },

        removeTag (index) {
            this.tagsList.splice(index, 1)
            this.$nuxt.$emit('updateTagsField', this.tagsList)
        }
    }
}
</script>
