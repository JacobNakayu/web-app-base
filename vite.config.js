/** @type {import('vite').UserConfig} */
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig(({mode}) =>{
    return {
        plugins: [vue()],
        css: {
            preprocessorOptions: {
                scss: {
                    // additionalData: '@import "./src/styles/base.scss";'
                }
            }
        },
        build: {
            outDir: 'vite_build', // Directory where built files are output
            emptyOutdir: true,
            rollupOptions: {
                input: 'index.html',
                output: {
                    entryFileNames: 'js/[name].js',
                    chunkFileNames: 'js/[name].js',
                    assetFileNames: 'assets/[name].[ext]',
                }
            }
        },
        server: {
            proxy: {
                '/api': 'http://127.0.0.1:8080/api'
            }
        }
    }    
    
});





