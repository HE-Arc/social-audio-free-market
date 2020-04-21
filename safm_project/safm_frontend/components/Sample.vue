<template>
    <v-card class="sample card">
        <v-card-title>{{ sample.name }}</v-card-title>
        <v-card-text>
            <v-row align="center">
                <v-col cols="4">
                    <v-icon>mdi-metronome</v-icon>
                    {{ sample.tempo }}
                </v-col>
                <v-col cols="4">
                    <v-icon>mdi-music-circle-outline</v-icon>
                    {{ sample.tone + sample.mode }}
                </v-col>
                <v-col cols="4">
                    <v-icon>mdi-timer-outline</v-icon>
                    {{ sample.duration + 's' }}
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-text>
            <v-chip
                v-for="tag in sample.tags"
                :key="tag.id"
                class="tag ma-1"
                label
                small
                outlined
            >
                {{ tag.name }}
            </v-chip>
        </v-card-text>
        <v-card-actions>
            <v-row align="center">
                <v-col cols="4">
                    <v-btn block>
                        <v-icon>mdi-play</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn block>
                        <v-icon>mdi-download-outline</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="4">
                    <v-btn block>
                        <v-icon>mdi-eye-outline</v-icon>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-actions>
    </v-card>
</template>

<script>
export default {
    props: ['sample']
}
</script>
