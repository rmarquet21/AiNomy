// register vue composition api globally
import App from './App.vue'
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'vue-toastification/dist/index.css'
import './common/styles/main.css'
import 'element-plus/dist/index.css'

const app = createApp(App)

Object.values(import.meta.globEager('./**/modules/*.ts')).forEach((i) => {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  return i.install?.({ app })
})

app.mount('#app')
