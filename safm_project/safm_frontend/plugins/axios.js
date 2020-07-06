
export default function ({ $axios, store }, inject) {
    // On Request event
    $axios.onRequest(() => {
        if (store.state.auth) {
            $axios.setHeader('Authorization', `Token ${store.state.auth}`)
        }
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
