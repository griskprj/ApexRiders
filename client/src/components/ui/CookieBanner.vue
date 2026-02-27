<template>
    <div v-if="!isConsentGiven" class="cookie-banner">
        <div class="cookie-content">
            <div class="cookie-message">
                <i class="fas fa-info-circle"></i>
                <p>
                    Этот сайт использует технические cookie-файлы для обеспечения работоспособности.
                    Продолжая использовать сайт, вы соглашаетесь с 
                    <router-link to="/privacy-policy">Политикой конфиденциальности</router-link>.
                </p>
            </div>

            <BaseButton
                variant="primary"
                size="small"
                @click="acceptCookies"
            >
                Хорошо
            </BaseButton>
        </div>
    </div>
</template>

<script>
/** 
 * Компонент CookieBanner
 * @description Отображает баннер с уведомлением об использовании cookie.
 * Показывается только если пользователь еще не дал согласие.
 * 
 * @component
 * @version 1.0.0
 * @example
 * <CookieBanner @consent-given="handleConsent" />
 * 
 * @emits consent-given - Срабатывает после того, как пользователь нажал "Хорошо"
 * **/

import BaseButton from './BaseButton.vue';
import { cookieManager } from '../../utils/cookieManager';

export default {
    name: 'CookieBanner',
    components: { BaseButton },
    
    data() {
        return {
            isConsentGiven: false
        }
    },
    
    mounted() {
        this.isConsentGiven = cookieManager.hasConsent();
    },
    
    methods: {
        acceptCookies() {
            cookieManager.setConsent('necessary');
            this.isConsentGiven = true;
            this.$emit('consent-given');
        }
    }
}
</script>

<style scoped>
.cookie-banner {
    position: fixed;
    bottom: 20px;
    left: 20px;
    right: 20px;
    max-width: 600px;
    margin: 0 auto;
    background: var(--bg-secondary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px 20px;
    z-index: 9999;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s ease;
}

.cookie-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
}

.cookie-message {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
    min-width: 250px;
}

.cookie-message i {
    color: var(--primary);
    font-size: 20px;
    flex-shrink: 0;
}

.cookie-message p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
}

.cookie-message a {
    color: var(--primary);
    text-decoration: none;
    transition: color 0.3s ease;
}

.cookie-message a:hover {
    color: var(--primary-dark);
    text-decoration: underline;
}

/* Adaptive */
@media (max-width: 768px) {
    .cookie-banner {
        bottom: 10px;
        left: 10px;
        right: 10px;
        padding: 16px;
    }
    
    .cookie-content {
        flex-direction: column;
        align-items: stretch;
        gap: 16px;
    }
    
    .cookie-message {
        min-width: auto;
    }
    
    .cookie-message i {
        align-self: flex-start;
        margin-top: 2px;
    }
    
    :deep(.btn-small) {
        width: 100%;
    }
}

/* Animation */
@keyframes slideUp {
    from {
        transform: translateY(100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
</style>