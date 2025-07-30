import { fileURLToPath, URL } from 'node:url'

import { defineConfig , loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'
import { createHtmlPlugin } from "vite-plugin-html";
//import { getFilePreview } from '../api/fileHttp.js'

const getViteEnv = (mode, target) => {
  return loadEnv(mode, process.cwd())[target];
};

// https://vitejs.dev/config/
export default ({mode})=>{
  return defineConfig({
    base: './',
    plugins: [
      vue(),
      // 临时注释掉 Vue DevTools
      // VueDevTools(),
      VueSetupExtend(),
      createHtmlPlugin({
        inject: {
          data: {
            title: getViteEnv(mode, "VITE_APP_TITLE"),
          },
        },
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    build: {
      rollupOptions: {
        external: [
          'vue',
          'element-plus'
        ],
        output: {
          globals: {
            vue: 'Vue',
            'element-plus': 'ElementPlus'
          }
        }
      },
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      }
    },
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        }
      }
    }
  })
}