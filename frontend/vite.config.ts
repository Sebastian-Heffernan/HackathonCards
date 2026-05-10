import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiUrl = env.VITE_API_URL || 'http://localhost:3000';

  return {
    plugins: [tailwindcss(), sveltekit()],
    define: {
      'process.title': JSON.stringify('browser'),
    },
    server: {
      proxy: {
        // Standard API Proxy
        '/api': {
          target: apiUrl,
          changeOrigin: true,
          secure: true,
        },
        // WebSocket Proxy
        '/ws': {
          target: apiUrl.replace(/^http/, 'ws'),
          ws: true,
          changeOrigin: true,
        }
      }
    }
  };
});