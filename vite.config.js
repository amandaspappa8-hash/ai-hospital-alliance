import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    react: ["react", "react-dom"],
                    router: ["react-router-dom"],
                    radix: [
                        "@radix-ui/react-avatar",
                        "@radix-ui/react-checkbox",
                        "@radix-ui/react-dialog",
                        "@radix-ui/react-dropdown-menu",
                        "@radix-ui/react-menubar",
                        "@radix-ui/react-navigation-menu",
                        "@radix-ui/react-popover",
                        "@radix-ui/react-scroll-area",
                        "@radix-ui/react-select",
                        "@radix-ui/react-separator",
                        "@radix-ui/react-slot",
                        "@radix-ui/react-switch",
                        "@radix-ui/react-tabs",
                        "@radix-ui/react-tooltip",
                    ],
                    charts: ["recharts"],
                },
            },
        },
    },
});
