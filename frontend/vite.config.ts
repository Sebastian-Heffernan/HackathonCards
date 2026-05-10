import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [tailwindcss(), sveltekit()],
    
        define: {
        'process.title': JSON.stringify('browser'),
    },
    server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://cardssembly-xylv-git-main-sebastian-heffernans-projects.vercel.app',
        ws: true
      }
    }
  }
});
