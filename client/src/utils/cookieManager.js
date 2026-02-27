/** 
 * Менеджер для работы с cookie-согласием
 * @module cookieManager
 * @description Предоставляет методы для установки, получения и управления
 * согласием пользователя на использование cookie-файлов
*/

export const cookieManager = {
    setConsent(consentType) {
        document.cookie = `cookie_consent=${consentType}; max-age=31536000; path=/; SameSite=Lax`
        localStorage.setItem('cookie_consent', consentType)
        
        if (consentType !== 'all') {
            this.removeNonEssentialCookies()
        }
    },

    getConsent() {
        const cookieConsent = document.cookie
            .split('; ')
            .find(row => row.startsWith('cookie_consent='))
            ?.split('=')[1]

        const localConsent = localStorage.getItem('cookie_consent')
        
        if (cookieConsent && !localConsent) {
            localStorage.setItem('cookie_consent', cookieConsent)
            return cookieConsent
        }
        
        if (localConsent && !cookieConsent) {
            document.cookie = `cookie_consent=${localConsent}; max-age=31536000; path=/; SameSite=Lax`
            return localConsent
        }

        return cookieConsent || localConsent || null
    },

    hasConsent() {
        return this.getConsent() !== null
    },

    getConsentType() {
        return this.getConsent()
    },

    hasConsentFor(type) {
        const consent = this.getConsent()
        if (!consent) return false
        
        if (type === 'necessary') return true
        
        return consent === 'all'
    },

    removeNonEssentialCookies() {
        const cookies = document.cookie.split('; ')
        cookies.forEach(cookie => {
            const [name] = cookie.split('=')
            if (!['cookie_consent', 'session', 'authToken', 'PHPSESSID'].includes(name)) {
                document.cookie = `${name}=; max-age=0; path=/`
                document.cookie = `${name}=; max-age=0; path=/; domain=${window.location.hostname}`
            }
        })
    },

    deleteAllCookies() {
        const cookies = document.cookie.split('; ')
        cookies.forEach(cookie => {
            const [name] = cookie.split('=')
            document.cookie = `${name}=; max-age=0; path=/`
            document.cookie = `${name}=; max-age=0; path=/; domain=${window.location.hostname}`
        })
        
        localStorage.removeItem('cookie_consent')
        
        console.log('All cookies deleted')
    }
}