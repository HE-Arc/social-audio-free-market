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

// Example of testing only generated html

test('Route / exits and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/', context)
    t.true(html.includes('nuxt'))
})
/*
test('Route /quick-search exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/quick-search', context)
    t.true(html.includes('main'))
})

test('No quick search results when query parameter does not match', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/quick-search', context)
    t.false(html.includes('sample'))
})

test('Route /samples/<id> exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/samples/1', context)
    t.true(html.includes('main'))
})

test('Route /profiles/<username> exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/profiles/1', context)
    t.true(html.includes('main'))
})
*/
// Close server and ask nuxt to stop listening to file changes
test.after('Closing server and nuxt.js', () => {
    nuxt.close()
})
