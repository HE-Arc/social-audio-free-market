export default function ({ store, redirect }) {
    // If the user is already authenticated
    if (store.state.auth) {
        return redirect('/')
    }
}
