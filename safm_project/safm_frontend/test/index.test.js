const test = require('ava')

// Example Test
test('Example Test', (t) => {
    const html = '<h1>Title</h1>'
    t.true(html.includes('Title'))
})
