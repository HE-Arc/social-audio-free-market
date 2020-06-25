const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => ({
    auth: null,
    username: '',
    advancedSearchParams: {
        name__icontains: '',   // Sample name
        user__username__icontains: '',
        duration__gte: 0,
        duration__lte: 30.0,
        tempo__gte: 1,
        tempo__lte: 200,
        key: [],
        mode: '',
        tags__name__icontains: []
    },
    advancedSearchOrdering: '',
    advancedSearchOrderingReverse: false
})

export const mutations = {
    setAuth (state, auth) {
        state.auth = auth
    },

    setUsername (state, username) {
        state.username = username
    },

    setAdvancedSearchParams (state, params) {
        state.advancedSearchParams = params
    },

    setAdvancedSearchOrdering (state, ordering) {
        state.advancedSearchOrdering = ordering
    },

    setAdvancedSearchOrderingReverse (state, orderingReverse) {
        state.advancedSearchOrderingReverse = orderingReverse
    }
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
            }
        }

        commit('setAuth', auth)
        commit('setUsername', username)
    }
}
