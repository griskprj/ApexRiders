import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import Manuals from '../components/Manuals.vue'
import Courses from '../components/Courses.vue'
import Market from '../components/Market.vue'
import Community from '../components/Community.vue'
import { authService } from '../utils/checkAuth'
import ProductDetails from '../components/ProductDetails.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: { public: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { public: true, guestOnly: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { public: true, guestOnly: true }
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
    },
    {
        path: '/manuals',
        name: 'Manuals',
        component: Manuals,
        meta: { requiresAuth: true }
    },
    {
        path: '/courses',
        name: 'Courses',
        component: Courses,
        meta: { requiresAuth: true }
    },
    {
        path: '/market',
        name: 'Market',
        component: Market,
        meta: { requiresAuth: true }
    },
    {
        path: '/market/:id',
        name: 'MarketDetail',
        component: ProductDetails,
        props: true,
        meta: { requiresAuth: true }
    },
    {
        path: '/community',
        name: 'Community',
        component: Community,
        meta: { requiresAuth: true }
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: Home,
        meta: { public: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    }
})

router.beforeEach(async (to, from, next) => {
    if (to.meta.public) {
        return next()
    }

    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const guestOnly = to.matched.some(record => record.meta.guestOnly)

    const hasToken = authService.getToken()
    const cachedUser = authService.getUser()

    if (hasToken && cachedUser && !guestOnly) {
        return next()
    }

    if (requiresAuth) {
        try {
            if (!navigator.onLine && cachedUser) {
                console.log('Offline mode, using cached user')
                return next()
            }

            const user = await authService.checkAuth()
            if (user) {
                return next()
            } else {
                return next({
                    name: 'Login',
                    query: { redirect: to.fullPath }
                })
            }
        } catch (error) {
            console.error('Auth check error:', error)
            if (cachedUser && hasToken) {
                console.log('Network error, using cached auth')
                return next()
            }
            return next({ name: 'Login' })
        }
    }

    if (guestOnly && hasToken) {
        return next({ name: 'Dashboard' })
    }

    next()
})

export default router