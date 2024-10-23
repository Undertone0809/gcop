import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "GCOP",
  description: "🚀 Your git AI copilot",
  sitemap: {
    hostname: "https://gcop.zeeland.top",
    transformItems: (items) => {
      return items.map(item => ({
        ...item,
        changefreq: 'weekly',
        priority: 0.8,
      }))
    }
  },
  head: [
    ['link', { rel: 'icon', href: '/gcop-logo.ico' }],
    [
      'script',
      {
        defer: 'true',
        'data-website-id': '77d0dd59-9095-463b-a317-b49b373af92d',
        src: 'https://umami.zeeland.top/script.js'
      }
    ],
    ['meta', { property: 'description', content: 'GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.' }],
    ['meta', { property: 'keywords', content: 'gcop, git, git copilot, LLM, git commit, commit message, conventional commit, version control,auto commit, git commit 规范' }],
    ['meta', { property: 'og:site_name', content: 'GCOP' }],
    ['meta', { property: 'og:url', content: 'https://gcop.zeeland.top' }],
    ['meta', { property: 'og:title', content: 'GCOP' }],
    ['meta', { property: 'og:description', content: 'GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.' }],
    ['meta', { property: 'og:image', content: 'https://r2.zeeland.top/images/2024/10/b03949e6bc43d71b7ddab3d70515eee0.png' }],
    ['meta', { property: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { property: 'twitter:image', content: 'https://r2.zeeland.top/images/2024/10/b03949e6bc43d71b7ddab3d70515eee0.png' }],
    ['meta', { property: 'twitter:title', content: 'GCOP' }],
    ['meta', { property: 'twitter:description', content: 'GCOP is an intelligent assistant designed to enhance your Git workflow by automating commit message generation using AI. Help you write better git commit message.' }],
    ['meta', { name: 'baidu-site-verification', content: 'codeva-Z87P16KxE3' }],
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/gcop-logo.png',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/introduction' },
      { text: 'Commands', link: '/guide/commands' },
      { text: 'FAQ', link: '/faq' },
    ],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Introduction', link: '/guide/introduction' },
          { text: 'Quick Start', link: '/guide/quick-start' },
          { text: 'Commands', link: '/guide/commands' },
          { text: 'Configuration', link: '/guide/configuration' },
          { text: 'Connect to Gaianet', link: '/guide/connect2gaianet' },
        ]
      },
      {
        text: 'Reference',
        items: [
          { text: 'How to Config Model', link: '/how-to-config-model' },
          { text: 'FAQ', link: '/faq' },
          { text: 'Changelog', link: '/changelog' },
          { text: 'Contributing', link: '/contributing' },
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/undertone0809/gcop' },
      { icon: 'twitter', link: 'https://x.com/kfhedRk3lXofRIB' }
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2023-present Zeeland'
    },
    search: {
      provider: 'local'
    },
    // Add an edit link for each page
    editLink: {
      pattern: 'https://github.com/undertone0809/gcop/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
  }
})
