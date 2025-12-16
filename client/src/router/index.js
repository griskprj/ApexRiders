import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import Manuals from '../components/Manuals.vue'
import Courses from '../components/Courses.vue'
import Market from '../components/Market.vue'
import { isAuthenticated } from '../utils/checkAuth'
import Community from '../components/Community.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
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

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    
    const isAuth = isAuthenticated()

    if (requiresAuth && !isAuth) {
        console.log('Auth required, redirecting to login')
        next({ name: 'Login', query: { redirect: to.fullPath } })
    } else if (to.name === 'Login' && isAuth) {
        console.log('Already authenticated, redirecting from login')
        next({ name: 'Dashboard' })
    } else {
        next()
    }
})


export default router