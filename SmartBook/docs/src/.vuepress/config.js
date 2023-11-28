import { defineUserConfig } from "vuepress";
import { hopeTheme } from "vuepress-theme-hope";
import { description } from "../../package.json";
import { getDirname, path } from "@vuepress/utils";
import { registerComponentsPlugin } from "@vuepress/plugin-register-components";

const __dirname = getDirname(import.meta.url);
//--------------------------------------------------------------------

export default defineUserConfig({
    /**
     * Ref：https://v1.vuepress.vuejs.org/config/#title
     */
    title: "SmartBook",
    /**
     * Ref：https://v1.vuepress.vuejs.org/config/#description
     */
    description: description,
    /**
     * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
     */
    base: "/SmartBook-Interface/",
    plugins: [
        [
            registerComponentsPlugin({
                components: {
                    BiasChart: path.resolve(
                        __dirname,
                        "./components/BiasChart.vue"
                    ),
                    DetailSlider: path.resolve(
                        __dirname,
                        "./components/DetailSlider.vue"
                    ),
                },
            }),
        ],
    ],
    theme: hopeTheme({
        /**
         * Extra tags to be injected to the page HTML `<head>`
         *
         * ref：https://v1.vuepress.vuejs.org/config/#head
         */
        head: [
            ["meta", { name: "theme-color", content: "#3eaf7c" }],
            ["meta", { name: "apple-mobile-web-app-capable", content: "yes" }],
            [
                "meta",
                {
                    name: "apple-mobile-web-app-status-bar-style",
                    content: "black",
                },
            ],
        ],

        /**
         * Theme configuration, here is the default theme configuration for VuePress.
         *
         * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
         */
        themeConfig: {
            repo: "",
            editLinks: false,
            docsDir: "",
            editLinkText: "",
            lastUpdated: false,
            nav: [
                {
                    text: "Book",
                    link: "/book/",
                },
                {
                    text: "Guide",
                    link: "/guide/",
                },
                {
                    text: "Config",
                    link: "/config/",
                },
            ],
            sidebar: {
                // "/book/": [
                //     {
                //         title: "Book",
                //         collapsable: false,
                //         activeMatch: "/book/",
                //     },
                // ],
                "/book/": "structure",
            },
        },
    }),
});
