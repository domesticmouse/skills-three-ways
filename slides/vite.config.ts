import { defineConfig } from 'vite'

export default defineConfig({
  optimizeDeps: {
    include: ['asciinema-player'],
  },
  ssr: {
    noExternal: ['asciinema-player'],
  },
})
