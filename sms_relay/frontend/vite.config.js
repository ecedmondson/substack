import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const INPUT_DIR = './src';

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api': {
          target: env.VITE_API_BASE || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '/api'),
        },
      },
    },
    resolve: {
      alias: {
        '~': resolve(INPUT_DIR),
        '@/shared': resolve(INPUT_DIR, 'shared'),
        '@/locale': resolve('../../locale'),
      },
    },
  };
});
