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
      VueDevTools(),
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
        output: {
          manualChunks: (id) => {
            // 分离 Vue 相关
            if (id.includes('vue') || id.includes('pinia') || id.includes('vue-router')) {
              return 'vue-vendor';
            }
            // 分离 Element Plus
            if (id.includes('element-plus')) {
              return 'element-plus';
            }
            // 分离 axios
            if (id.includes('axios')) {
              return 'axios';
            }
            // 分离其他大型依赖
            if (id.includes('node_modules')) {
              return 'vendor';
            }
          }
        }
      },
      // 启用压缩
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      },
      // 设置块大小警告阈值
      chunkSizeWarningLimit: 500
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