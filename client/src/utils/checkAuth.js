const TOKEN_KEY = 'authToken'
const USER_KEY = 'user'
const TOKEN_EXPIRY = 24 * 60 * 60 * 1000

export class AuthService {
    constructor() {
        this._isRefreshing = false
    }

    async checkAuth(force = false) {
        const token = this.getToken()
        if (!token) {
            this.clearAuth()
            return null
        }

        if (!this.isValidToken(token)) {
            this.clearAuth()
            return null
        }

        if (token && this.isTokenExpired(token)) {
            this.clearAuth()
            return null
        }
        
        const cachedUser = this.getUser()
        const now = Date.now()

        if (cachedUser && cachedUser._timestamp && 
            (now - cachedUser._timestamp < 5 * 60 * 1000) && !force) {
            return cachedUser
        }

        if (this.isOnline()) {
            try {
                const user = await this.fetchCurrentUser()
                if (user) {
                    user._timestamp = now
                    this.saveUser(user)
                    return user
                } else {
                    this.clearAuth()
                    return null
                }
            } catch (error) {
                console.error('Auth check failed: ', error)

                if (error.status === 401 || error.status === 403) {
                    this.clearAuth()
                    return null
                }

                if (!this.isOnline() && cachedUser) {
                    return cachedUser
                }
            }
        } else {
            return cachedUser || null
        }
        
        return null
    }

    isTokenExpired(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]))
            return payload.exp && payload.exp * 1000 < Date.now()
        } catch {
            return true
        }
    }

    async fetchCurrentUser() {
        const token = this.getToken()
        if (!token) return null
        
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 8000)

        try {
            const response = await fetch('/api/auth/user', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                signal: controller.signal
            })

            clearTimeout(timeoutId)

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) {
                    throw { status: response.status, message: 'Unauthorized' }
                }
                throw new Error(`HTTP ${response.status}`)
            }

            const data = await response.json()
            return data.user || data.member || null
        } catch (error) {
            clearTimeout(timeoutId)
            throw error
        }
    }

    async login(email, password) {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })

        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Login failed' }))
            throw error
        }

        const data = await response.json()

        this.saveToken(data.access_token)

        const user = data.user || data.member
        if (user) {
            user._timestamp = Date.now()
            this.saveUser(user)
        }

        return { user, token: data.access_token }
    }

    async register(username, email, password) {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        })

        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Registration failed'}))
            throw error
        }

        const data = await response.json()

        this.saveToken(data.access_token)

        const user = data.user || data.member
        if (user) {
            user._timestamp = Date.now()
            this.saveUser(user)
        }

        return { user, token: data.access_token }
    }

    async logout() {
        const token = this.getToken()

        try {
            if (token && this.isOnline()) {
                await fetch('/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    timeout: 5000
                })
            }
        } catch (error) {
            console.log('Logout API call failed, proceeding with local logout')
        } finally {
            this.clearAuth()
        }
    }

    isAuthenticated() {
        const token = this.getToken()
        const user = this.getUser()

        if (!token || !user) return false

        if (this.isTokenExpired(token)) {
            this.clearAuth()
            return false
        }

        if (!this.isValidToken(token)) {
            return false
        }

        if (!user.id && !user.email) {
            return false
        }

        return true
    }

    saveToken(token) {
        localStorage.setItem(TOKEN_KEY, token)
    }

    getToken() {
        return localStorage.getItem(TOKEN_KEY)
    }

    saveUser(user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user))
    }

    getUser() {
        try {
            const userStr = localStorage.getItem(USER_KEY)
            return userStr ? JSON.parse(userStr) : null
        } catch {
            return null
        }
    }

    clearAuth() {
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(USER_KEY)
    }

    isValidToken(token) {
        return token &&
            typeof token === 'string' &&
            token.length >= 10 &&
            token !== 'undefined' &&
            token !== 'null' &&
            token !== 'undefined'
    }

    isOnline() {
        return typeof navigator !== 'undefined' && navigator.onLine
    }

    getAuthStatus() {
        const token = this.getToken()
        const user = this.getUser()
        const isAuthenticated = this.isAuthenticated()
        
        return {
            isAuthenticated,
            hasToken: !!token,
            hasUser: !!user,
            user,
            token
        }
    }
}

export const authService = new AuthService()

export const checkAuth = () => authService.checkAuth()
export const isAuthenticated = () => authService.isAuthenticated()
export const getToken = () => authService.getToken()
export const getUser = () => authService.getUser()
export const logout = () => authService.logout()
export const getAuthStatus = () => authService.getAuthStatus()