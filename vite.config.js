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
    // 根据环境设置不同的base路径
    base: mode === 'production' ? '/' : './',
    plugins: [
      vue(),
      VueSetupExtend(),
      createHtmlPlugin({
        inject: {
          data: {
            title: getViteEnv(mode, "VITE_APP_TITLE") || "知了oa系统",
          },
        },
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    // 暂时移除 external 配置
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'vue-vendor': ['vue', 'vue-router', 'pinia'],
            'element-plus': ['element-plus']
          }
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