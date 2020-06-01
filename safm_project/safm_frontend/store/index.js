export const state = () => ({
    auth: null,
    repeatSample: false
})

export const mutations = {
    setAuth (state, auth) {
        state.auth = auth
    },

    toggleRepeatSample (state) {
        state.repeatSample = !state.repeatSample
    }
}
