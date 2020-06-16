const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => ({
    auth: null,
    username: ''
    //repeatSample: false
})

export const mutations = {
    setAuth (state, auth) {
        state.auth = auth
    },

    setUsername (state, username) {
        state.username = username
    }

    /*
    toggleRepeatSample (state) {
        state.repeatSample = !state.repeatSample
    }
    */
}

export const actions = {
    nuxtServerInit ({ commit }, { req }) {
        let auth = null
        let username = ''

        if (req && req.headers.cookie) {
            const parsed = cookieparser.parse(req.headers.cookie)
            // Sets the authentification token if the corresponding cookie is present
            try {
                auth = parsed.auth
                username = parsed.username
            } catch (error) {
                // Not a valid authentication token nor username
                console.log(error)
            }
        }

        commit('setAuth', auth)
        commit('setUsername', username)
    }
}
