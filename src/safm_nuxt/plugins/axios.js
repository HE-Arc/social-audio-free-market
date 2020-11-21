
export default function ({ $axios, store }, inject) {
    // Adds the authentication token to each Axios request if present in the store
    $axios.interceptors.request.use(request => {
        const token = store.state.auth
        if (token) {
            request.headers.common['Authorization'] = `Token ${token}`
        }

        return request
    })

    // Converts an array of errors into a String
    inject('errorArrayToString', (errors) => {
        let str = ''
        for (let e in errors) {
            str += `${e}: ${errors[e]}`
        }

        return str
    })
}
