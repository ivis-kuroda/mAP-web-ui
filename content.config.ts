import { defineCollection, defineContentConfig } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    help: defineCollection({
      type: 'page',
      source: '1.help/**/*',
    }),
  },
})
