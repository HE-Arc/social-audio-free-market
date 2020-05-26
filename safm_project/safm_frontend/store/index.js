
export const state = () => ({
    repeatSample: false
})

export const mutations = {
    toggleRepeatSample (state) {
        state.repeatSample = !state.repeatSample
    }
}
