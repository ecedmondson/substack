import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig(() => { 
  const INPUT_DIR = './src';
  return {
    plugins: [react()],
    resolve: {
      alias: {
        '~': resolve(INPUT_DIR),
        '@/shared': resolve(INPUT_DIR, './shared'),
        '@/locale': resolve('../../locale'),
      },
    }
  }
});

