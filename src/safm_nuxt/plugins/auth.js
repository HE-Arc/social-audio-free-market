const Cookie = process.client ? require('js-cookie') : undefined

export default ({ store, $axios }, inject) => {
    // Stores the user authentication credentials
    inject('storeUserCredentials', (response) => {
        const authToken = response.data.token
        const userid = response.data.userid
        const username = response.data.username

        store.commit('setAuth', authToken)
        Cookie.set('auth', authToken)

        store.commit('setUser', {
            id: userid,
            name: username
        })
        Cookie.set('userid', userid)
        Cookie.set('username', username)

        $axios.setHeader('Authorization', `Token ${authToken}`)

        return userid
    })

    // Removes the user authentication credentials
    inject('deleteUserCredentials', () => {
        store.commit('setAuth', null)
        Cookie.remove('auth')
        store.commit('setUser', null)
        Cookie.remove('userid')
        Cookie.remove('username')

        $axios.setHeader('Authorization', null)
    })

    // Updates the username in the store
    inject('updateUsername', (username) => {
        store.commit('setUsername', username)
        Cookie.set('username', username)
    })
}
