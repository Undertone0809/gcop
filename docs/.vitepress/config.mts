import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "GCOP",
  description: "🚀 Your git AI copilot",
  head: [
    ['link', { rel: 'icon', href: '/images/logo.ico' }],
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/images/gcop-logo.png',
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
