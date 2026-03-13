import { defineConfig } from "vitepress";
import { withPwa } from "@vite-pwa/vitepress";

const getAnalyticsScripts = () => {
  if (process.env.NODE_ENV === "development") {
    return [];
  }

  return [
    [
      "script",
      {
        defer: "true",
        "data-website-id": "77d0dd59-9095-463b-a317-b49b373af92d",
        src: "https://umami.zeeland.top/script.js",
      },
    ] as [string, Record<string, string>],
    [
      "script",
      {
        async: "true",
        src: "https://www.googletagmanager.com/gtag/js?id=G-T0VJ22HP63",
      },
    ] as [string, Record<string, string>],
    [
      "script",
      {},
      `window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-T0VJ22HP63');`,
    ] as [string, Record<string, string>, string],
  ];
};

// https://vitepress.dev/reference/site-config
export default withPwa(
  defineConfig({
    title: "GCOP",
    description:
      "🚀 GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.",
    sitemap: {
      hostname: "https://gcop.zeeland.top",
      transformItems: (items) => {
        return items.map((item) => ({
          ...item,
          changefreq: "weekly",
          priority: 0.8,
        }));
      },
    },
    head: [
      ...getAnalyticsScripts(),
      ["link", { rel: "icon", href: "/gcop-logo.ico" }],
      [
        "meta",
        {
          property: "description",
          content:
            "GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.",
        },
      ],
      [
        "meta",
        {
          property: "keywords",
          content:
            "gcop, git, git copilot, LLM, git commit, commit message, conventional commit, version control,auto commit, git commit 规范",
        },
      ],
      [
        "meta",
        { property: "og:site_name", content: "GCOP - Your Git AI Copilot" },
      ],
      ["meta", { property: "og:url", content: "https://gcop.zeeland.top" }],
      ["meta", { property: "og:title", content: "GCOP - Your Git AI Copilot" }],
      [
        "meta",
        {
          property: "og:description",
          content:
            "GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.",
        },
      ],
      [
        "meta",
        {
          property: "og:image",
          content: "https://r2.zeeland.top/images/2024/10/b03949e6bc43d71b7ddab3d70515eee0.png",
        },
      ],
      ["meta", { property: "twitter:card", content: "summary_large_image" }],
      [
        "meta",
        {
          property: "twitter:image",
          content: "https://r2.zeeland.top/images/2024/10/b03949e6bc43d71b7ddab3d70515eee0.png",
        },
      ],
      [
        "meta",
        { property: "twitter:title", content: "GCOP - Your Git AI Copilot" },
      ],
      [
        "meta",
        {
          property: "twitter:description",
          content:
            "GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.",
        },
      ],
      [
        "meta",
        { name: "baidu-site-verification", content: "codeva-Z87P16KxE3" },
      ],
    ],
    themeConfig: {
      // https://vitepress.dev/reference/default-theme-config
      logo: "/gcop-logo.png",
      outline: {
        level: [2, 3],
      },
      nav: [
        { text: "Home", link: "/" },
        { text: "Guide", link: "/guide/introduction" },
        { text: "Commands", link: "/guide/commands" },
        { text: "FAQ", link: "/faq" },
      ],
      sidebar: [
        {
          text: "Guide",
          items: [
            { text: "Introduction", link: "/guide/introduction" },
            { text: "Quick Start", link: "/guide/quick-start" },
            { text: "How to guide", link: "/guide/how-to-guide" },
            { text: "Best Practice", link: "/guide/best-practice" },
            { text: "Commands", link: "/guide/commands" },
            { text: "Configuration", link: "/guide/configuration" },
            { text: "Upgrade", link: "/guide/upgrade" },
          ],
        },
        {
          text: "Other",
          items: [
            { text: "How to Config Model", link: "/other/how-to-config-model" },
            { text: "Connect to Gaianet", link: "/other/connect2gaianet" },
            { text: "Changelog", link: "/other/changelog" },
            { text: "Contributing", link: "/other/contributing" },
          ],
        },
      ],
      socialLinks: [
        { icon: "github", link: "https://github.com/undertone0809/gcop" },
        { icon: "x", link: "https://x.com/kfhedRk3lXofRIB" },
      ],
      footer: {
        message: "Released under the MIT License.",
        copyright: "Copyright © 2023-present Zeeland",
      },
      search: {
        provider: "local",
      },
      // Add an edit link for each page
      editLink: {
        pattern: "https://github.com/undertone0809/gcop/edit/main/docs/:path",
        text: "Edit this page on GitHub",
      },
    },
    pwa: {
      manifest: {
        name: "GCOP",
        short_name: "gcop",
        theme_color: "#2b2a27",
        background_color: "#ffffff",
        display: "standalone",
        orientation: "portrait",
        scope: "/",
        start_url: "/",
        icons: [
          {
            src: "/gcop-logo.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable any",
          },
        ],
      },
    },
  })
);
