<template>
    <div :class="`sample-fork${checkbox ? ' with-checkbox' : ''}`">
        <div class="d-flex flex-row mb-6">
            <BtnPlayPause :sampleId="id" />
            <div class="pl-4">
                <div>
                    <nuxt-link :to="`/sample/${id}`">{{ name }}</nuxt-link>
                </div>
                <div>
                    <span>By</span>
                    <nuxt-link :to="`/profile/${userId}`">{{ username }}</nuxt-link>
                </div>
            </div>
        </div>
        <div>
            <WaveForm :id="id" height="50" />
        </div>
        <div v-if="datetime_download" class="mt-4">
            <span>{{ `Downloaded on ${new Date(datetime_download).toLocaleDateString()}` }}</span>
        </div>
        <div v-if="checkbox">
            <v-checkbox
                v-model="selected"
                class="checkbox"
                @change="checkboxChange"
            >
            </v-checkbox>
        </div>
    </div>
</template>

<script>
import WaveForm from '~/components/WaveForm.vue'
import BtnPlayPause from '~/components/sample/BtnPlayPause'

export default {
    components: {
        WaveForm,
        BtnPlayPause
    },

    props: [
        'id',
        'name',
        'userId',
        'username',
        'datetime_download',
        'checkbox',
        'checked'
    ],

    data () {
        return {
            selected: this.checked ? this.checked : false
        }
    },

    methods: {
        checkboxChange () {
            this.$nuxt.$emit('forkCheckbox', this.id, this.selected)
        }
    }
}
</script>

<style scoped>
.sample-fork {
    background: #1c1c1c;
    border-radius: 5px;
    padding: 1em;
    position: relative;
    transition: all 0.2s;
}
.sample-fork:hover {
    box-shadow: 1px 1px 15px 5px #111111;
}
.sample-fork.with-checkbox {
    padding: 1.5em 1em 1em 1em;
}
.checkbox {
    position: absolute;
    top: 0;
    right: 0;
    margin: 0.8em 0 0 0;
    padding: 0;
}
</style>
