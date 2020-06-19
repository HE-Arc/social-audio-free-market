<template>
    <div class="d-flex justify-space-between">
        <BtnPlayPause :sampleId="sampleId" />
        <BtnRepeat :sampleId="sampleId" />
        <BtnDownload :sampleId="sampleId" />
    </div>
</template>

<script>
import BtnPlayPause from '~/components/sample/BtnPlayPause'
import BtnRepeat from '~/components/sample/BtnRepeat'
import BtnDownload from '~/components/sample/BtnDownload'

export default {
    components: {
        BtnPlayPause,
        BtnRepeat,
        BtnDownload
    },

    props: [
        'sampleId'
    ]
}
</script>
