import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      "/login": "http://localhost:8080",
      "/create_html": "http://localhost:8080",
    },
  },
  build: {
    outDir: "dist",
  },
});
