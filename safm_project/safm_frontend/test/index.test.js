const test = require('ava')
const resolve = require('path').resolve
const Nuxt = require('nuxt').Nuxt
const Builder = require('nuxt').Builder
const JSDOM = require('jsdom').JSDOM

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
test('Route / exits and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/', context)
    t.true(html.includes('nuxt'))
})

test('Route /advanced-search exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/advanced-search', context)
    t.true(html.includes('nuxt'))
})
/*
test('Route /profiles exits and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/profiles', context)
    t.true(html.includes('nuxt'))
})
*/
test('Route /quick-search exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/quick-search', context)
    t.true(html.includes('nuxt'))
})

test('Route /register exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/register', context)
    t.true(html.includes('nuxt'))
})
/*
test('Route /samples exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/samples', context)
    t.true(html.includes('nuxt'))
})
*/
test('Route /upload exists and renders HTML', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/upload', context)
    t.true(html.includes('nuxt'))
})

test('Route /upload protected by authentication', async (t) => {
    const context = {}
    const { html } = await nuxt.server.renderRoute('/upload', context)
    const { window } = new JSDOM(html).window

    // Not logged in
    let uploadForm = window.document.querySelector('#sample-upload-form')
    t.is(uploadForm, null)
})

// Close server and ask nuxt to stop listening to file changes
test.after('Closing server and nuxt.js', () => {
    nuxt.close()
})
