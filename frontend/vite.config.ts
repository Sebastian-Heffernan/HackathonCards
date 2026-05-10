import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  // Load variables from .env
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [tailwindcss(), sveltekit()],
    define: {
      'process.title': JSON.stringify('browser'),
    },
    server: {
      proxy: {
        '/api': {
          // CHANGE: Use the env variable instead of the hardcoded string
          target: env.VITE_API_URL, 
          changeOrigin: true, // Usually safer to set to true for cross-origin proxies
          rewrite: (path) => path.replace(/^\/api/, '/api'),
        },
        '/ws': {
          target: env.VITE_API_URL.replace('http', 'ws'),
          ws: true
        }
      }
    }
  };
});