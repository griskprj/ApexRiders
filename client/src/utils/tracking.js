// Утилита для работы с пикселями
export const tracking = {
  // Mail.ru Pixel
  mailRu: {
    pageView(url = null, referrer = null) {
      if (this.isLocalhost()) {
        console.log(`[Mail.ru] PageView: ${url || window.location.pathname}`)
        return
      }
      
      const params = { id: "3736665", type: "pageView" }
      if (url) params.url = url
      if (referrer) params.referrer = referrer
      
      this.pushToMailRu(params)
    },
    
    goal(goalName, goalValue = null) {
      if (this.isLocalhost()) {
        console.log(`[Mail.ru] Goal: ${goalName}`, goalValue ? `Value: ${goalValue}` : '')
        return
      }
      
      const params = { id: "3736665", type: "reachGoal", goal: goalName }
      if (goalValue !== null) params.value = goalValue
      
      this.pushToMailRu(params)
    },
    
    pushToMailRu(params) {
      if (window._tmr) {
        window._tmr.push(params)
      } else {
        window._tmr = window._tmr || []
        window._tmr.push(params)
      }
    }
  },
  
  // VK Pixel
  vk: {
    event(eventName, eventParams = {}) {
      if (this.isLocalhost()) {
        console.log(`[VK] ${eventName}:`, eventParams)
        return
      }
      
      if (window.VK && window.VK.Retargeting) {
        window.VK.Retargeting.Event(eventName, eventParams)
      }
    },
    
    // Стандартные события VK
    viewContent(params) {
      this.event('ViewContent', params)
    },
  },
  
  // Общие цели
  trackRegistration(isNewUser = true, userData = {}) {
    // Mail.ru
    if (isNewUser) {
      this.mailRu.goal('registration_complete', 0)
      this.mailRu.goal('new_user_registered')
    } else {
      this.mailRu.goal('user_login')
    }
    
    // VK
    this.vk.event(isNewUser ? 'CompleteRegistration' : 'Login', {
      user_id: userData.id || userData.email,
      email: userData.email
    })
  },
  
  // Проверка на localhost
  isLocalhost() {
    return window.location.hostname === 'localhost' || 
           window.location.hostname === '127.0.0.1'
  }
}

// Экспорт по умолчанию
export default tracking