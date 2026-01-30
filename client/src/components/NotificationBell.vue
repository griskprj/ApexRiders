<template>
    <div class="notification-container">
        <!-- Кнопка-колокольчик -->
        <button 
            class="notification-bell" 
            @click="toggleDropdown"
            :class="{ 'has-notifications': unreadCount > 0 }"
        >
            <i class="fas fa-bell"></i>
            <span v-if="unreadCount > 0" class="notification-badge">
                {{ unreadCount > 99 ? '99+' : unreadCount }}
            </span>
        </button>
        
        <!-- Выпадающее меню с уведомлениями -->
        <div v-if="isDropdownOpen" class="notification-dropdown">
            <div class="dropdown-header">
                <h4>Уведомления</h4>
                <div class="header-actions">
                    <button 
                        v-if="unreadCount > 0" 
                        @click="markAllAsRead" 
                        class="btn-mark-all"
                        :disabled="isMarkingAll"
                    >
                        {{ isMarkingAll ? '...' : 'Прочитать все' }}
                    </button>
                    <button @click="refreshNotifications" class="btn-refresh">
                        <i class="fas fa-sync-alt" :class="{ 'fa-spin': isLoading }"></i>
                    </button>
                </div>
            </div>
            
            <div class="notifications-list">
                <div v-if="isLoading" class="loading-notifications">
                    <div class="spinner"></div>
                    <p>Загрузка уведомлений...</p>
                </div>
                
                <div v-else-if="notifications.length === 0" class="empty-notifications">
                    <i class="fas fa-bell-slash"></i>
                    <p>Нет новых уведомлений</p>
                </div>
                
                <div v-else>
                    <div 
                        v-for="notification in notifications" 
                        :key="notification.id"
                        class="notification-item"
                        :class="{ 'unread': !notification.is_read }"
                        @click="handleNotificationClick(notification)"
                    >
                        <div class="notification-icon">
                            <i :class="getNotificationIcon(notification.notification_type)"></i>
                        </div>
                        
                        <div class="notification-content">
                            <div class="notification-header">
                                <h5>{{ notification.title }}</h5>
                                <span class="notification-time">{{ notification.ago_time }}</span>
                            </div>
                            
                            <p class="notification-message">{{ notification.message }}</p>
                            
                            <div v-if="notification.priority === 'high'" class="notification-priority">
                                <i class="fas fa-exclamation-circle"></i>
                                <span>Важное</span>
                            </div>
                            
                            <div v-if="notification.admin_info" class="notification-admin">
                                <span>От: {{ notification.admin_info.username }}</span>
                            </div>
                        </div>
                        
                        <div class="notification-actions">
                            <button 
                                v-if="!notification.is_read"
                                @click.stop="markAsRead(notification)"
                                class="btn-mark-read"
                                title="Отметить как прочитанное"
                            >
                                <i class="fas fa-check"></i>
                            </button>
                            <button 
                                @click.stop="archiveNotification(notification)"
                                class="btn-archive"
                                title="Архивировать"
                            >
                                <i class="fas fa-archive"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="dropdown-footer">
                <router-link to="/notifications" @click="closeDropdown">
                    Показать все уведомления
                </router-link>
            </div>
        </div>
        
        <!-- Overlay для закрытия по клику вне меню -->
        <div 
            v-if="isDropdownOpen" 
            class="dropdown-overlay" 
            @click="closeDropdown"
        ></div>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { authService } from '../utils/checkAuth'

export default {
    name: 'NotificationBell',
    
    setup() {
        const isDropdownOpen = ref(false)
        const notifications = ref([])
        const unreadCount = ref(0)
        const isLoading = ref(false)
        const isMarkingAll = ref(false)
        
        const fetchNotifications = async () => {
            try {
                isLoading.value = true
                const token = authService.getToken()
                
                if (!token) {
                    console.error('No authentication token found')
                    return
                }
                
                const response = await axios.get('/api/notifications', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        unread_only: false,
                        per_page: 5
                    }
                })
                
                notifications.value = response.data.notifications || []
                unreadCount.value = response.data.unread_count || 0
                
            } catch (error) {
                console.error('Ошибка при загрузке уведомлений:', error)
                
                if (error.response && error.response.status === 401) {
                    authService.clearAuth()
                }
            } finally {
                isLoading.value = false
            }
        }
        
        const fetchUnreadCount = async () => {
            try {
                const token = authService.getToken()
                
                if (!token) return
                
                const response = await axios.get('/api/notifications/count', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                unreadCount.value = response.data.unread_count || 0
                
            } catch (error) {
                console.error('Ошибка при загрузке количества уведомлений:', error)
            }
        }
        
        const markAsRead = async (notification) => {
            try {
                const token = authService.getToken()
                
                if (!token) return
                
                await axios.put(`/api/notifications/${notification.id}/read`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                // Обновляем локально
                notification.is_read = true
                unreadCount.value = Math.max(0, unreadCount.value - 1)
                
            } catch (error) {
                console.error('Ошибка при отметке уведомления:', error)
            }
        }
        
        const markAllAsRead = async () => {
            try {
                isMarkingAll.value = true
                const token = authService.getToken()
                
                if (!token) return
                
                await axios.put('/api/notifications/read-all', {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                // Обновляем все уведомления как прочитанные
                notifications.value.forEach(n => n.is_read = true)
                unreadCount.value = 0
                
            } catch (error) {
                console.error('Ошибка при отметке всех уведомлений:', error)
            } finally {
                isMarkingAll.value = false
            }
        }
        
        const archiveNotification = async (notification) => {
            try {
                const token = authService.getToken()
                
                if (!token) return
                
                await axios.put(`/api/notifications/${notification.id}/archive`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                // Удаляем из списка
                notifications.value = notifications.value.filter(n => n.id !== notification.id)
                
                // Обновляем счетчик если уведомление было непрочитанным
                if (!notification.is_read) {
                    unreadCount.value = Math.max(0, unreadCount.value - 1)
                }
                
            } catch (error) {
                console.error('Ошибка при архивации уведомления:', error)
            }
        }
        
        const handleNotificationClick = (notification) => {
            // В зависимости от типа уведомления переходим на нужную страницу
            if (notification.target_type && notification.target_id) {
                let route = ''
                
                switch (notification.target_type) {
                    case 'post':
                        route = `/community/post/${notification.target_id}`
                        break
                    case 'comment':
                        route = `/community/post/${notification.metadata?.post_id || ''}`
                        break
                    case 'product':
                        route = `/market/product/${notification.target_id}`
                        break
                    default:
                        break
                }
                
                if (route) {
                    window.location.href = route
                }
            }
            
            // Отмечаем как прочитанное при клике
            if (!notification.is_read) {
                markAsRead(notification)
            }
        }
        
        const getNotificationIcon = (type) => {
            const icons = {
                'like_post': 'fas fa-thumbs-up',
                'like_comment': 'fas fa-comment-heart',
                'like_product': 'fas fa-heart',
                'admin_report': 'fas fa-exclamation-triangle',
                'admin_broadcast': 'fas fa-bullhorn'
            }
            
            return icons[type] || 'fas fa-bell'
        }
        
        const toggleDropdown = () => {
            isDropdownOpen.value = !isDropdownOpen.value
            
            if (isDropdownOpen.value) {
                fetchNotifications()
            }
        }
        
        const closeDropdown = () => {
            isDropdownOpen.value = false
        }
        
        const refreshNotifications = () => {
            fetchNotifications()
            fetchUnreadCount()
        }
        
        // Периодическая проверка новых уведомлений (каждые 30 секунд)
        let intervalId = null
        
        const startPolling = () => {
            if (intervalId) clearInterval(intervalId)
            
            intervalId = setInterval(() => {
                fetchUnreadCount()
            }, 30000) // 30 секунд
        }
        
        const stopPolling = () => {
            if (intervalId) {
                clearInterval(intervalId)
                intervalId = null
            }
        }
        
        onMounted(() => {
            // Загружаем начальное количество уведомлений
            fetchUnreadCount()
            
            // Запускаем опрос только если пользователь авторизован
            if (authService.isAuthenticated()) {
                startPolling()
            }
        })
        
        onUnmounted(() => {
            stopPolling()
        })
        
        return {
            isDropdownOpen,
            notifications,
            unreadCount,
            isLoading,
            isMarkingAll,
            fetchNotifications,
            markAsRead,
            markAllAsRead,
            archiveNotification,
            handleNotificationClick,
            getNotificationIcon,
            toggleDropdown,
            closeDropdown,
            refreshNotifications
        }
    }
}
</script>

<style scoped>
.notification-container {
    position: relative;
}

.notification-bell {
    position: relative;
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.4rem;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.notification-bell:hover {
    color: var(--text);
    background: rgba(255, 255, 255, 0.1);
}

.notification-bell.has-notifications {
    color: var(--primary);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(255, 69, 0, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); }
}

.notification-badge {
    position: absolute;
    top: 0;
    right: 0;
    background: var(--danger);
    color: white;
    font-size: 0.7rem;
    font-weight: bold;
    min-width: 18px;
    height: 18px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 4px;
}

.notification-dropdown {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    width: 380px;
    max-height: 500px;
    background: var(--bg-secondary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    z-index: 1001;
    overflow: hidden;
}

.dropdown-header {
    padding: 15px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dropdown-header h4 {
    margin: 0;
    color: var(--text);
    font-size: 1.1rem;
}

.header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}

.btn-mark-all, .btn-refresh {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: var(--text-secondary);
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-mark-all:hover {
    background: var(--primary-light);
    color: var(--primary);
}

.btn-refresh {
    padding: 5px;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-refresh:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.notifications-list {
    max-height: 350px;
    overflow-y: auto;
}

.loading-notifications {
    padding: 40px 20px;
    text-align: center;
    color: var(--text-secondary);
}

.loading-notifications .spinner {
    width: 30px;
    height: 30px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 15px;
}

.empty-notifications {
    padding: 40px 20px;
    text-align: center;
    color: var(--text-secondary);
}

.empty-notifications i {
    font-size: 2.5rem;
    margin-bottom: 15px;
    opacity: 0.5;
}

.notification-item {
    padding: 15px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    gap: 15px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.notification-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.notification-item.unread {
    background: rgba(var(--primary-rgb), 0.05);
    border-left: 3px solid var(--primary);
}

.notification-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(var(--primary-rgb), 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    font-size: 1.2rem;
}

.notification-content {
    flex: 1;
    min-width: 0;
}

.notification-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 5px;
}

.notification-header h5 {
    margin: 0;
    font-size: 0.95rem;
    color: var(--text);
    font-weight: 600;
}

.notification-time {
    font-size: 0.8rem;
    color: var(--text-secondary);
    white-space: nowrap;
    margin-left: 10px;
}

.notification-message {
    margin: 0 0 8px 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

.notification-priority {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    margin-top: 5px;
}

.notification-admin {
    margin-top: 5px;
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-style: italic;
}

.notification-actions {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.notification-item:hover .notification-actions {
    opacity: 1;
}

.btn-mark-read, .btn-archive {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.3s ease;
}

.btn-mark-read:hover {
    background: var(--success);
    color: white;
    border-color: var(--success);
}

.btn-archive:hover {
    background: var(--warning);
    color: white;
    border-color: var(--warning);
}

.dropdown-footer {
    padding: 15px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

.dropdown-footer a {
    color: var(--primary);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
}

.dropdown-footer a:hover {
    text-decoration: underline;
}

.dropdown-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
}

/* Стили для скроллбара */
.notifications-list::-webkit-scrollbar {
    width: 6px;
}

.notifications-list::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
}

.notifications-list::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 3px;
}

.notifications-list::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}

@media (max-width: 768px) {
    .notification-dropdown {
        position: fixed;
        top: 70px;
        right: 10px;
        left: 10px;
        width: auto;
        max-height: 70vh;
    }
}
</style>