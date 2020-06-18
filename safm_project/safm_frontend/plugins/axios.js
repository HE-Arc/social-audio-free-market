
export default function ({ $axios, store }) {
    $axios.onRequest(() => {
        if (store.state.auth) {
            $axios.setHeader('Authorization', `Token ${store.state.auth}`)
        }
    })
}
