<template>
    <div class="notifications-page">
        <div class="page-header">
            <h1><i class="fas fa-bell"></i> Уведомления</h1>
            <div class="header-actions">
                <button 
                    v-if="unreadCount > 0" 
                    @click="markAllAsRead" 
                    class="btn btn-outline"
                    :disabled="isMarkingAll"
                >
                    <i class="fas fa-check-double"></i>
                    {{ isMarkingAll ? 'Обработка...' : 'Прочитать все' }}
                </button>
                <button @click="refreshNotifications" class="btn btn-outline">
                    <i class="fas fa-sync-alt" :class="{ 'fa-spin': isLoading }"></i>
                    Обновить
                </button>
            </div>
        </div>
        
        <div class="notifications-filters">
            <div class="filter-tabs">
                <button 
                    v-for="filter in filters" 
                    :key="filter.id"
                    @click="setActiveFilter(filter.id)"
                    :class="{ 'active': activeFilter === filter.id }"
                    class="filter-tab"
                >
                    {{ filter.label }}
                    <span v-if="filter.count" class="filter-count">{{ filter.count }}</span>
                </button>
            </div>
        </div>
        
        <div class="notifications-container">
            <div v-if="isLoading && notifications.length === 0" class="loading-state">
                <div class="spinner"></div>
                <p>Загрузка уведомлений...</p>
            </div>
            
            <div v-else-if="filteredNotifications.length === 0" class="empty-state">
                <i class="fas fa-bell-slash"></i>
                <h3>Нет уведомлений</h3>
                <p>{{ getEmptyMessage() }}</p>
            </div>
            
            <div v-else class="notifications-list">
                <div 
                    v-for="notification in filteredNotifications" 
                    :key="notification.id"
                    class="notification-card"
                    :class="{ 
                        'unread': !notification.is_read,
                        'priority-high': notification.priority === 'high',
                        'archived': notification.is_archived
                    }"
                    @click="handleNotificationClick(notification)"
                >
                    <div class="notification-icon">
                        <i :class="getNotificationIcon(notification.notification_type)"></i>
                    </div>
                    
                    <div class="notification-main">
                        <div class="notification-header">
                            <h3>{{ notification.title }}</h3>
                            <span class="notification-time">{{ notification.ago_time }}</span>
                        </div>
                        
                        <p class="notification-message">{{ notification.message }}</p>
                        
                        <div v-if="notification.metadata && Object.keys(notification.metadata).length > 0" 
                             class="notification-metadata">
                            <div v-if="notification.metadata.reason" class="metadata-item">
                                <strong>Причина:</strong> {{ notification.metadata.reason }}
                            </div>
                            <div v-if="notification.metadata.action_taken" class="metadata-item">
                                <strong>Принятые меры:</strong> {{ notification.metadata.action_taken }}
                            </div>
                            <div v-if="notification.metadata.liker_username" class="metadata-item">
                                <strong>От пользователя:</strong> {{ notification.metadata.liker_username }}
                            </div>
                        </div>
                        
                        <div v-if="notification.admin_info" class="notification-admin">
                            <i class="fas fa-user-shield"></i>
                            <span>От администратора: {{ notification.admin_info.username }}</span>
                        </div>
                    </div>
                    
                    <div class="notification-actions">
                        <div v-if="!notification.is_read" class="unread-indicator">
                            <i class="fas fa-circle"></i>
                            <span>Новое</span>
                        </div>
                        
                        <div class="action-buttons">
                            <button 
                                v-if="!notification.is_read"
                                @click.stop="markAsRead(notification)"
                                class="btn-action"
                                title="Отметить как прочитанное"
                            >
                                <i class="fas fa-check"></i>
                            </button>
                            
                            <button 
                                v-if="!notification.is_archived"
                                @click.stop="archiveNotification(notification)"
                                class="btn-action"
                                title="Архивировать"
                            >
                                <i class="fas fa-archive"></i>
                            </button>
                            
                            <button 
                                v-if="notification.is_archived"
                                @click.stop="restoreNotification(notification)"
                                class="btn-action"
                                title="Восстановить из архива"
                            >
                                <i class="fas fa-undo"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Пагинация -->
            <div v-if="totalPages > 1" class="pagination">
                <button 
                    @click="goToPage(currentPage - 1)"
                    :disabled="currentPage === 1"
                    class="pagination-btn"
                >
                    <i class="fas fa-chevron-left"></i>
                </button>
                
                <span class="pagination-info">
                    Страница {{ currentPage }} из {{ totalPages }}
                </span>
                
                <button 
                    @click="goToPage(currentPage + 1)"
                    :disabled="currentPage === totalPages"
                    class="pagination-btn"
                >
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { authService } from '../../utils/checkAuth'

export default {
    name: 'NotificationsPage',
    
    setup() {
        const notifications = ref([])
        const unreadCount = ref(0)
        const isLoading = ref(false)
        const isMarkingAll = ref(false)
        const activeFilter = ref('all')
        const currentPage = ref(1)
        const totalPages = ref(1)
        const totalNotifications = ref(0)
        
        const filters = computed(() => [
            { id: 'all', label: 'Все', count: null },
            { id: 'unread', label: 'Непрочитанные', count: unreadCount.value },
            { id: 'likes', label: 'Лайки', count: getCountByType(['like_post', 'like_comment', 'like_product']) },
            { id: 'admin', label: 'Администрация', count: getCountByType(['admin_report', 'admin_broadcast']) },
            { id: 'archived', label: 'Архив', count: getCountByArchived() }
        ])
        
        function getCountByType(types) {
            return notifications.value.filter(n => 
                types.includes(n.notification_type) && !n.is_archived
            ).length
        }
        
        function getCountByArchived() {
            return notifications.value.filter(n => n.is_archived).length
        }
        
        const filteredNotifications = computed(() => {
            let filtered = notifications.value
            
            switch (activeFilter.value) {
                case 'unread':
                    filtered = filtered.filter(n => !n.is_read && !n.is_archived)
                    break
                case 'likes':
                    filtered = filtered.filter(n => 
                        ['like_post', 'like_comment', 'like_product'].includes(n.notification_type) && 
                        !n.is_archived
                    )
                    break
                case 'admin':
                    filtered = filtered.filter(n => 
                        ['admin_report', 'admin_broadcast'].includes(n.notification_type) && 
                        !n.is_archived
                    )
                    break
                case 'archived':
                    filtered = filtered.filter(n => n.is_archived)
                    break
                default:
                    filtered = filtered.filter(n => !n.is_archived)
            }
            
            return filtered
        })
        
        const fetchNotifications = async (page = 1) => {
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
                        page: page,
                        per_page: 20
                    }
                })
                
                notifications.value = response.data.notifications || []
                unreadCount.value = response.data.unread_count || 0
                totalPages.value = response.data.pages || 1
                totalNotifications.value = response.data.total || 0
                currentPage.value = page
                
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
                
                // Обновляем локально
                notification.is_archived = true
                
                // Обновляем счетчик если уведомление было непрочитанным
                if (!notification.is_read) {
                    unreadCount.value = Math.max(0, unreadCount.value - 1)
                }
                
            } catch (error) {
                console.error('Ошибка при архивации уведомления:', error)
            }
        }
        
        const restoreNotification = async (notification) => {
            // Для восстановления нужно будет создать новый endpoint
            // Пока просто отметим как неархивированное локально
            notification.is_archived = false
        }
        
        const handleNotificationClick = (notification) => {
            // Аналогично компоненту NotificationBell
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
        
        const setActiveFilter = (filterId) => {
            activeFilter.value = filterId
        }
        
        const refreshNotifications = () => {
            fetchNotifications(currentPage.value)
            fetchUnreadCount()
        }
        
        const goToPage = (page) => {
            if (page >= 1 && page <= totalPages.value) {
                fetchNotifications(page)
            }
        }
        
        const getEmptyMessage = () => {
            switch (activeFilter.value) {
                case 'unread':
                    return 'У вас нет непрочитанных уведомлений'
                case 'likes':
                    return 'Пока никто не оценил ваш контент'
                case 'admin':
                    return 'Нет уведомлений от администрации'
                case 'archived':
                    return 'Архив уведомлений пуст'
                default:
                    return 'У вас пока нет уведомлений'
            }
        }
        
        onMounted(() => {
            fetchNotifications()
            fetchUnreadCount()
        })
        
        return {
            notifications,
            unreadCount,
            isLoading,
            isMarkingAll,
            activeFilter,
            filters,
            filteredNotifications,
            currentPage,
            totalPages,
            totalNotifications,
            fetchNotifications,
            markAsRead,
            markAllAsRead,
            archiveNotification,
            restoreNotification,
            handleNotificationClick,
            getNotificationIcon,
            setActiveFilter,
            refreshNotifications,
            goToPage,
            getEmptyMessage
        }
    }
}
</script>

<style scoped>
/* Стили для страницы уведомлений */
.notifications-page {
    padding: 120px 5% 60px;
    max-width: 1200px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.page-header h1 {
    font-size: 2.2rem;
    display: flex;
    align-items: center;
    gap: 15px;
}

.page-header h1 i {
    color: var(--primary);
}

.header-actions {
    display: flex;
    gap: 15px;
}

.notifications-filters {
    margin-bottom: 30px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 10px;
}

.filter-tabs {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 5px;
}

.filter-tab {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-tab:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.filter-tab.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.filter-count {
    background: rgba(0, 0, 0, 0.3);
    color: white;
    font-size: 0.8rem;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: bold;
}

.notifications-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    overflow: hidden;
}

.loading-state, .empty-state {
    padding: 60px 20px;
    text-align: center;
}

.loading-state .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

.empty-state i {
    font-size: 3rem;
    color: var(--text-secondary);
    opacity: 0.5;
    margin-bottom: 20px;
}

.empty-state h3 {
    color: var(--text);
    margin-bottom: 10px;
}

.empty-state p {
    color: var(--text-secondary);
}

.notifications-list {
    max-height: 600px;
    overflow-y: auto;
}

.notification-card {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    gap: 20px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.notification-card:hover {
    background: rgba(255, 255, 255, 0.05);
}

.notification-card.unread {
    background: rgba(var(--primary-rgb), 0.05);
    border-left: 3px solid var(--primary);
}

.notification-card.priority-high {
    background: rgba(var(--danger-rgb), 0.05);
    border-left: 3px solid var(--danger);
}

.notification-card.archived {
    opacity: 0.7;
    background: rgba(255, 255, 255, 0.02);
}

.notification-icon {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(var(--primary-rgb), 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    font-size: 1.3rem;
}

.notification-card.priority-high .notification-icon {
    background: rgba(var(--danger-rgb), 0.1);
    color: var(--danger);
}

.notification-main {
    flex: 1;
    min-width: 0;
}

.notification-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
}

.notification-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text);
    font-weight: 600;
}

.notification-time {
    font-size: 0.9rem;
    color: var(--text-secondary);
    white-space: nowrap;
    margin-left: 15px;
}

.notification-message {
    margin: 0 0 15px 0;
    color: var(--text-secondary);
    line-height: 1.5;
}

.notification-metadata {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    padding: 10px 15px;
    margin-bottom: 15px;
}

.metadata-item {
    margin-bottom: 5px;
    font-size: 0.9rem;
}

.metadata-item:last-child {
    margin-bottom: 0;
}

.metadata-item strong {
    color: var(--text);
    margin-right: 5px;
}

.notification-admin {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.notification-admin i {
    color: var(--warning);
}

.notification-actions {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
}

.unread-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--primary);
    font-size: 0.8rem;
    font-weight: 500;
}

.unread-indicator i {
    font-size: 0.6rem;
}

.action-buttons {
    display: flex;
    gap: 8px;
}

.btn-action {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-action:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    padding: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.pagination-btn {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
    background: var(--primary);
    border-color: var(--primary);
}

.pagination-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.pagination-info {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Стили для скроллбара */
.notifications-list::-webkit-scrollbar {
    width: 8px;
}

.notifications-list::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
}

.notifications-list::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 4px;
}

.notifications-list::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}

@media (max-width: 768px) {
    .notifications-page {
        padding: 100px 3% 40px;
    }
    
    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .page-header h1 {
        font-size: 1.8rem;
    }
    
    .header-actions {
        width: 100%;
        justify-content: flex-start;
    }
    
    .notification-card {
        flex-direction: column;
        gap: 15px;
    }
    
    .notification-actions {
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
    }
    
    .notification-header {
        flex-direction: column;
        gap: 5px;
    }
    
    .notification-time {
        margin-left: 0;
    }
}
</style>