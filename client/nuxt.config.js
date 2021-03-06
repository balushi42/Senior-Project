export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'spclient',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  loading: {
    color: 'rgb(16, 185, 129)'
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '~/assets/css/main.scss'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/stylelint
    '@nuxtjs/stylelint-module',
    '@nuxtjs/tailwindcss',
    ['@nuxtjs/fontawesome', {
      component: 'Fa',
      icons: {
        solid: [
          'faBars',
          'faTimes',
          'faUpload'
        ]
      }
    }]
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/proxy'
  ],

  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access',
          maxAge: 3000,
          // type: 'Bearer'
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24
        },
        user: {
          property: 'user',
        },
        endpoints: {
          login: { url: '/api/v1/token/', method: 'post' },
          refresh: { url: '/api/v1/token/refresh/', method: 'post' },
          user: { url: '/api/v1/me/', method: 'get' },
          logout: { url: '/api/v1/logout/', method: 'get' }
        },
        // autoLogout: false
      }
    }
  },

  proxy: [
    'http://localhost:8000/api'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    proxy: true
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
