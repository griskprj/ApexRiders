export async function checkAuth() {
    try {
        const token = localStorage.getItem('authToken')
        const userStr = localStorage.getItem('user')

        if (!isValidToken(token)) {
            clearAuth()
            return null
        }

        if (userStr) {
            try {
                const user = JSON.parse(userStr)
                if (!user || !(user.id || user.email || user.username)) {
                    clearAuth()
                    return null
                }
            } catch {
                clearAuth()
                return null
            }
        }

        const response = await fetch('/api/auth/user', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        })

        if (response.ok) {
            const data = await response.json()
            const user = data.user || data
            localStorage.setItem('user', JSON.stringify(user))
            return user
        } else {
            if (response.status === 401 || response.status === 422) {
                clearAuth()
            }
            return null
        }
    } catch (error) {
        console.error('Auth check error:', error)
        clearAuth()
        return null
    }
}

function clearAuth() {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
}

function isValidToken(token) {
    return token && 
           token !== 'undefined' && 
           token !== 'null' && 
           token.length >= 10
}

export function isAuthenticated() {
    const token = localStorage.getItem('authToken')
    const user = localStorage.getItem('user')

    if (!isValidToken(token) || !user) {
        return false
    }

    try {
        const userObj = JSON.parse(user)
        return !!(userObj && (userObj.id || userObj.email || userObj.username))
    } catch {
        return false
    }
}

export function getToken() {
    return localStorage.getItem('authToken')
}

export function getUser() {
    const userStr = localStorage.getItem('user')
    try {
        return userStr ? JSON.parse(userStr) : null
    } catch {
        return null
    }
}