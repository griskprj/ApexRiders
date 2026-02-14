import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'Logo192.jpg'],

      manifest: {
        name: 'ApexRiders',
        short_name: 'AR',
        description: 'Сообщество мотоциклистов ApexRiders',
        theme_color: '#ff4500',
        background_color: '#0a0a0f',
        display: 'standalone',
        orientation: 'portrait',
        scope: '/',
        start_url: '/dashboard',
        icons: [
          {
            src: "/Logo192.jpg",
            sizes: "192x192",
            type: "image/jpg",
          },
          {
            src: "/Logo512.jpg",
            sizes: "512x512",
            type: "image/jpg",
          },
          {
            src: "/Logo512.jpg",
            sizes: "512x512",
            type: "image/jpg",
            purpose: "any maskable"
          },
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}']
      },
      devOptions: {
        enabled: true,
        type: 'module'
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    open: true,
    cors: true,
    hmr: {
      host: 'localhost',
      protocol: 'ws'
    },
    proxy: {
      '/uploads': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },

      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        ws: true,
        rewrite: (path) => path,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('proxy error', err)
          })
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('Sending Request to the Target:', req.method, req.url)
          })
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url)
          })
        }
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})