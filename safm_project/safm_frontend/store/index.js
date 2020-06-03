const cookieparser = process.server ? require('cookieparser') : undefined

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

export const actions = {
    nuxtServerInit ({ commit }, { req }) {
        let auth = null
        if (req.headers.cookie) {
            const parsed = cookieparser.parse(req.headers.cookie)
            // Sets the authentification token if the corresponding cookie is present
            try {
                auth = parsed.auth
            } catch (error) {
                // Not a valid authentication token
            }
        }

        commit('setAuth', auth)
    }
}
