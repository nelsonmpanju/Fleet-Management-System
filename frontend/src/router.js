import { createRouter, createWebHistory } from 'vue-router';
import { session, userResource } from '@/store';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    name: 'Login',
    path: '/login',
    component: () => import('@/pages/Login.vue'),
  }
];

const router = createRouter({
  history: createWebHistory('/map'),
  routes,
});

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn;

  try {
    await userResource.promise;
  } catch (error) {
    isLoggedIn = false;
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' });
  } else if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
