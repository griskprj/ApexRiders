import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../utils/checkAuth'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../components/Home.vue'),
        meta: { public: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../components/Register.vue'),
        meta: { public: true, guestOnly: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../components/Login.vue'),
        meta: { public: true, guestOnly: true }
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('../components/Dashboard.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/manuals',
        name: 'Manuals',
        component: () => import('../components/Manuals.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/create-manual',
        name: 'CreateManual',
        component: () => import('../components/manuals/CreateManual.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/manual/:id',
        name: 'ManualViewer',
        component: () => import('../components/manuals/ManualViewer.vue'),
        props: true,
        meta: { requiresAuth: true }
    },
    {
        path: '/constructor/edit/:id',
        name: 'EditManual',
        component: () => import('../components/manuals/EditManual.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/courses',
        name: 'Courses',
        component: () => import('../components/Courses.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/market',
        name: 'Market',
        component: () => import('../components/Market.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/market/:id',
        name: 'MarketDetail',
        component: () => import('../components/ProductDetails.vue'),
        props: true,
        meta: { requiresAuth: true }
    },
    {
        path: '/community',
        name: 'Community',
        component: () => import('../components/Community.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/community/post/:id',
        name: 'PostView',
        component: () => import('../components/PostView.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('../components/Profile.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/garage/:id',
        name: 'Garage',
        component: () => import('../components/Garage.vue'),
        meta: { requiresAuth: true }
    },

    {
        path: '/admin/dashboard',
        component: () => import('../components/admin/AdminDashboard.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
    },

    {
        path: '/notifications',
        name: 'Notifications',
        component: () => import('../components/NotificationsPage.vue'),
        meta: { requiresAuth: true }
    },

    {
        path: '/about',
        name: 'AboutPage',
        component: () => import('../components/AboutPage.vue'),
        meta: { 
            public: true,
            title: 'О проекте'
         }
    },

    {
        path: '/privacy-policy',
        name: 'PrivacyPolicy',
        component: () => import('../components/PrivacyPolicy.vue'),
        meta: {
            public: true,
            title: 'Политика конфиденциальности'
        }
    },
    {
        path: '/community-rules',
        name: 'CommunityRules',
        component: () => import('../components/CommunityRules.vue'),
        meta: {
            public: true,
            title: 'Правила сообщества'
        }
    },
    {
        path: '/contacts',
        name: 'Contacts',
        component: () => import('../components/Contacts.vue'),
        meta: {
            public: true,
            title: 'Контакты'
        }
    },

    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../components/Home.vue'),
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
    const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)

    if (guestOnly) {
        const isAuthenticated = authService.isAuthenticated()
        if (isAuthenticated) {
            return next('/dashboard')
        }
        return next()
    }

    if (requiresAuth) {
        try {
            const user = await authService.checkAuth(false)
            
            if (!user) {
                authService.clearAuth()
                return next('/login')
            }

            if (requiresAdmin) {
                if (!user.admin_level || user.admin_level <= 0) {
                    return next('/dashboard')
                }
            }

            return next()
        } catch (error) {
            console.error('Auth error:', error)
            authService.clearAuth()
            return next('/login')
        }
    }

    next()
})

router.afterEach((to) => {
    if (to.meta.title) {
        document.title = `${to.meta.title} | ApexRiders`
    } else {
        document.title = 'ApexRiders'
    }
})

export default router