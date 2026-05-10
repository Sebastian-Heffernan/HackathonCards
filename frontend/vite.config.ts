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
          target: env.VITE_API_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '/api'), // Adjust if FastAPI has a prefix
        },
        '/ws': {
          target: env.VITE_API_URL.replace('http', 'ws'),
          ws: true
        }
      }
    }
  };
});