const test = require('ava')
const resolve = require('path').resolve
const Nuxt = require('nuxt').Nuxt
const Builder = require('nuxt').Builder

// In order to close the server instance at the end
let nuxt = null

// Init Nuxt.js and create a server listening on localhost:4000
test.before(async () => {
    const config = {
        dev: false,
        rootDir: resolve(__dirname, '..')
    }
    nuxt = new Nuxt(config)
    await new Builder(nuxt).build()
    await nuxt.server.listen(4000, 'localhost')
}, 30000)

// Routes exist and render HTML
test('Application routes exist and render HTML', async (t) => {
    // Routes that do not require an authentication
    const routes = [
        { route: '/', html: 'SAFMarket' },
        { route: 'advanced-search', html: 'Advanced Search' },
        { route: 'login', html: 'Login' },
        //{ route: 'quick-search/test', html: 'Search Results' },
        { route: 'register', html: 'Create Account' },
        { route: 'reset_password', html: 'Request password reset' }
    ]

    for (let item of routes) {
        const context = {}
        const { html } = await nuxt.server.renderRoute(item.route, context)
        t.true(html.includes(item.html))
    }
})

// Close server and ask nuxt to stop listening to file changes
test.after('Closing server and nuxt.js', () => {
    nuxt.close()
})
