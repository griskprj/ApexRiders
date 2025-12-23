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

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { guestOnly: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { guestOnly: true }
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
        path: '/community',
        name: 'Community',
        component: Community,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const guestOnly = to.matched.some(record => record.meta.guestOnly)

    const isAuth = authService.isAuthenticated()

    if (requiresAuth && !isAuth) {
        await authService.checkAuth(true)

        if (!authService.isAuthenticated()) {
            console.log('Auth required, redirecting to login')
            return next({
                name: 'Login',
                query: { redirect: to.fullPath }
            })
        }
    }

    if (guestOnly && isAuth) {
        console.log('Already authenticated, redirecting to dashboard')
        return next({ name: 'Dashboard' })
    }

    next()
})

export default router