let test = require('ava')

// Example Test
test('Example Test', async (t) => {
  const html = '<h1>Title</h1>'
  t.true(html.includes('Title'))
})
