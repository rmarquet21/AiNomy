import { createRouter, createWebHistory } from 'vue-router'
import { setupLayouts } from 'virtual:generated-layouts'
import generatedRoutes from 'virtual:generated-pages'
import { useAuthStore } from '~/common/stores/authentication'
import type { UserModule } from '~/types'

export const routes = setupLayouts(generatedRoutes)

export const install: UserModule = ({ app }) => {
  // authentication route guard
  const router = createRouter({ history: createWebHistory(), routes })

  router.beforeEach((to, _, next) => {
    const auth = useAuthStore()

    if (to.meta.requiresAuth && !auth.token)
      next('/')
    next()
  })

  app.use(router)
}
