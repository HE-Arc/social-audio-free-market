<template>
    <v-btn
        v-if="canEdit"
        fab
        :absolute="absolute"
        :fixed="fixed"
        top
        right
        :to="`/sample/edit/${this.sampleId}`"
        :class="`mt-${this.bigMargin ? this.bigMarginValue : '1'}`"
    >
        <v-icon>mdi-pencil</v-icon>
    </v-btn>
</template>

<script>
export default {
    props: {
        sampleId: Number,
        sampleUserId: Number,
        absolute: Boolean,
        fixed: Boolean,
        bigMargin: Boolean
    },

    computed: {
        canEdit () {
            if (this.$store.state.user) {
                // Only the author of a sample can edit or delete it
                return this.sampleUserId == this.$store.state.user.id
            }
            
            return false
        },

        bigMarginValue () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return 12
            case 'sm': return 14
            case 'md': return 16
            case 'lg': return 16
            case 'xl': return 16
            }
        }
    }
}
</script>
