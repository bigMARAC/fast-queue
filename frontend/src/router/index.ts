import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true } 
    },
    {
      path: '/queue/:id',
      name: 'queue',
      component: () => import('../views/QueueView.vue')
    }
  ]
})

router.beforeEach(async (to, from) => { 
    const authStore = useAuthStore();

    if (authStore.loading) {
        await authStore.init();
    }

    const isAuthenticated = !!authStore.user;
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

    if (requiresAuth && !isAuthenticated) {
        return { name: "login" };
    } 
    
    if (to.name === "login" && isAuthenticated) {
        return { name: "dashboard" };
    }

});
export default router