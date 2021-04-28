<template>
    <div class="d-flex justify-space-between">
        <BtnPlayPause :sample-id="sampleId" />
        <BtnRepeat :sample-id="sampleId" />
        <BtnDownload :sample-id="sampleId" />
        <BtnLike :sample-id="sampleId" />
    </div>
</template>

<script>
import BtnPlayPause from '~/components/sample/BtnPlayPause';
import BtnRepeat from '~/components/sample/BtnRepeat';
import BtnDownload from '~/components/sample/BtnDownload';
import BtnLike from '~/components/sample/BtnLike';

export default {
    components: {
        BtnPlayPause,
        BtnRepeat,
        BtnDownload,
        BtnLike
    },

    props: [
        'sampleId'
    ]
};
</script>
