
export default function ({ $axios, app, store }) {
    $axios.onRequest(config => {
        if (store.state.auth) {
            $axios.setHeader('Authorization', `Token ${store.state.auth}`)
        }
    })
}
