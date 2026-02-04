import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/recordings': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    }
  }
})
