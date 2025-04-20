import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import 'dotenv/config'


// טוען משתני סביבה מקובץ .env
dotenv.config()

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  },
  define: {
    'process.env': process.env
  }
})
