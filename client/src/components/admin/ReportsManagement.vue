<template>
    <div class="reports-management">
        <div class="page-header">
            <h1><i class="fas fa-flag"></i> Управление жалобами</h1>
            <div class="header-actions">
                <button @click="refreshData" class="btn btn-outline" :disabled="loading">
                    <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i> 
                    {{ loading ? 'Загрузка...' : 'Обновить' }}
                </button>
                <button @click="forceRefresh" class="btn btn-primary" :disabled="loading">
                    <i class="fas fa-redo"></i> Обновить счетчик
                </button>
            </div>
        </div>
        
        <!-- Статистика -->
        <div class="stats-grid">
            <div class="stat-card" @click="setFilter('all')" :class="{ active: statusFilter === 'all' }">
                <div class="stat-icon" style="background: rgba(255, 69, 0, 0.2); color: #ff4500;">
                    <i class="fas fa-flag"></i>
                </div>
                <div class="stat-info">
                    <h3>{{ stats.total || 0 }}</h3>
                    <p>Всего жалоб</p>
                </div>
                <div class="stat-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
            
            <div class="stat-card" @click="setFilter('pending')" :class="{ active: statusFilter === 'pending' }">
                <div class="stat-icon" style="background: rgba(255, 193, 7, 0.2); color: #ffc107;">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="stat-info">
                    <h3>{{ stats.pending || 0 }}</h3>
                    <p>Ожидают проверки</p>
                </div>
                <div class="stat-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
            
            <div class="stat-card" @click="setFilter('reviewing')" :class="{ active: statusFilter === 'reviewing' }">
                <div class="stat-icon" style="background: rgba(0, 123, 255, 0.2); color: #007bff;">
                    <i class="fas fa-search"></i>
                </div>
                <div class="stat-info">
                    <h3>{{ stats.reviewing || 0 }}</h3>
                    <p>На проверке</p>
                </div>
                <div class="stat-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
            
            <div class="stat-card" @click="setFilter('assigned_to_me')" :class="{ active: assignedFilter === 'assigned_to_me' }">
                <div class="stat-icon" style="background: rgba(40, 167, 69, 0.2); color: #28a745;">
                    <i class="fas fa-user-shield"></i>
                </div>
                <div class="stat-info">
                    <h3>{{ stats.assigned_to_me || 0 }}</h3>
                    <p>Назначено мне</p>
                </div>
                <div class="stat-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
        </div>
        
        <!-- Фильтры -->
        <div class="filters">
            <div class="filter-group">
                <label><i class="fas fa-filter"></i> Статус:</label>
                <select v-model="statusFilter" @change="loadReports">
                    <option value="all">Все статусы</option>
                    <option value="pending">Ожидают проверки</option>
                    <option value="reviewing">На проверке</option>
                    <option value="resolved">Решены</option>
                    <option value="dismissed">Отклонены</option>
                </select>
            </div>
            
            <div class="filter-group">
                <label><i class="fas fa-th-large"></i> Тип контента:</label>
                <select v-model="targetTypeFilter" @change="loadReports">
                    <option value="">Все типы</option>
                    <option value="post">Посты</option>
                    <option value="comment">Комментарии</option>
                    <option value="product">Объявления</option>
                    <option value="manual">Мануалы</option>
                </select>
            </div>
            
            <div class="filter-group">
                <label><i class="fas fa-exclamation-circle"></i> Приоритет:</label>
                <select v-model="priorityFilter" @change="loadReports">
                    <option value="">Все приоритеты</option>
                    <option value="high">Высокий</option>
                    <option value="medium">Средний</option>
                    <option value="low">Низкий</option>
                </select>
            </div>
            
            <div class="filter-group">
                <label><i class="fas fa-user-tag"></i> Назначение:</label>
                <select v-model="assignedFilter" @change="loadReports">
                    <option value="all">Все жалобы</option>
                    <option value="assigned_to_me">Назначенные мне</option>
                    <option value="unassigned">Не назначенные</option>
                </select>
            </div>
            
            <div class="filter-group">
                <label><i class="fas fa-list-ol"></i> На странице:</label>
                <select v-model="perPage" @change="loadReports">
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                </select>
            </div>
        </div>
        
        <!-- Таблица жалоб -->
        <div class="reports-table-container">
            <div class="table-header">
                <div class="table-info">
                    <span>Жалобы: {{ totalReports }}</span>
                    <span v-if="reports.length > 0">({{ (currentPage - 1) * perPage + 1 }}-{{ Math.min(currentPage * perPage, totalReports) }})</span>
                </div>
                <div class="table-actions">
                    <button @click="exportReports" class="btn btn-outline btn-sm">
                        <i class="fas fa-download"></i> Экспорт
                    </button>
                </div>
            </div>
            
            <div v-if="loading" class="loading-overlay">
                <div class="spinner"></div>
                <p>Загрузка жалоб...</p>
            </div>
            
            <div class="table-responsive">
                <table class="reports-table">
                    <thead>
                        <tr>
                            <th class="text-center">ID</th>
                            <th>Жалоба</th>
                            <th>Контент</th>
                            <th>Автор</th>
                            <th>Статус</th>
                            <th>Приоритет</th>
                            <th>Назначено</th>
                            <th>Дата</th>
                            <th class="text-center">Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="report in reports" :key="report.id" 
                            :class="`priority-${report.priority} status-${report.status}`"
                            @click="viewReport(report)"
                            class="report-row">
                            <td class="report-id text-center">#{{ report.id }}</td>
                            <td class="report-info">
                                <div class="report-reason">
                                    <strong>{{ report.reason }}</strong>
                                    <div class="report-meta">
                                        <small v-if="report.reporter_username"><i class="fas fa-user-circle"></i> От: {{ report.reporter_username }}</small>
                                        <small v-if="report.details" class="text-truncate"><i class="fas fa-comment-alt"></i> {{ report.details }}</small>
                                    </div>
                                </div>
                            </td>
                            <td class="report-target">
                                <div class="target-type">
                                    <i :class="getTargetIcon(report.target_type)" class="target-icon"></i>
                                    <div class="target-info">
                                        <span class="target-type-text">{{ getTargetTypeText(report.target_type) }}</span>
                                        <small>ID: {{ report.target_id }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <span v-if="report.reported_user_username" class="user-badge">
                                    <i class="fas fa-user"></i>
                                    {{ report.reported_user_username }}
                                </span>
                                <span v-else class="text-muted">Не указан</span>
                            </td>
                            <td>
                                <span class="status-badge" :class="`status-${report.status}`">
                                    <i class="status-icon" :class="getStatusIcon(report.status)"></i>
                                    {{ getStatusText(report.status) }}
                                </span>
                            </td>
                            <td>
                                <span class="priority-badge" :class="`priority-${report.priority}`">
                                    <i class="priority-icon" :class="getPriorityIcon(report.priority)"></i>
                                    {{ getPriorityText(report.priority) }}
                                </span>
                            </td>
                            <td>
                                <div v-if="report.assigned_admin_username" class="admin-assigned">
                                    <i class="fas fa-user-shield"></i>
                                    <span>{{ report.assigned_admin_username }}</span>
                                </div>
                                <span v-else class="text-muted">
                                    <i class="fas fa-user-times"></i> Не назначено
                                </span>
                            </td>
                            <td class="report-date">
                                <div class="date-text">{{ formatDate(report.created_at) }}</div>
                                <small class="date-relative">{{ getRelativeTime(report.created_at) }}</small>
                            </td>
                            <td class="actions">
                                <div class="action-buttons">
                                    <button 
                                        @click.stop="viewReport(report)" 
                                        class="btn-action btn-view"
                                        title="Просмотреть"
                                    >
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    
                                    <button 
                                        v-if="!report.assigned_admin_id"
                                        @click.stop="assignReport(report)" 
                                        class="btn-action btn-assign"
                                        title="Назначить себе"
                                    >
                                        <i class="fas fa-user-check"></i>
                                    </button>
                                    
                                    <button 
                                        v-if="report.assigned_admin_id === currentAdmin?.id && report.status === 'reviewing'"
                                        @click.stop="resolveReport(report)" 
                                        class="btn-action btn-resolve"
                                        title="Завершить"
                                    >
                                        <i class="fas fa-check"></i>
                                    </button>
                                    
                                    <button 
                                        v-if="report.assigned_admin_id === currentAdmin?.id && report.status === 'reviewing'"
                                        @click.stop="dismissReport(report)" 
                                        class="btn-action btn-dismiss"
                                        title="Отклонить"
                                    >
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div v-if="!loading && reports.length === 0" class="empty-state">
                <div class="empty-state-icon">
                    <i class="fas fa-flag"></i>
                </div>
                <h3>Жалобы не найдены</h3>
                <p>Попробуйте изменить параметры фильтрации</p>
                <button @click="resetFilters" class="btn btn-primary">
                    <i class="fas fa-redo"></i> Сбросить фильтры
                </button>
            </div>
        </div>
        
        <!-- Пагинация -->
        <div class="pagination" v-if="totalPages > 1">
            <div class="pagination-info">
                Показано {{ reports.length }} из {{ totalReports }} жалоб
            </div>
            
            <div class="pagination-controls">
                <button 
                    @click="goToPage(currentPage - 1)" 
                    :disabled="currentPage === 1"
                    class="pagination-btn"
                >
                    <i class="fas fa-chevron-left"></i>
                </button>
                
                <div class="page-numbers">
                    <button 
                        v-for="page in visiblePages" 
                        :key="page"
                        @click="goToPage(page)"
                        :class="{ active: page === currentPage }"
                        class="page-btn"
                    >
                        {{ page }}
                    </button>
                </div>
                
                <button 
                    @click="goToPage(currentPage + 1)" 
                    :disabled="currentPage === totalPages"
                    class="pagination-btn"
                >
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            
            <div class="pagination-size">
                <select v-model="perPage" @change="loadReports" class="per-page-select">
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                </select>
            </div>
        </div>
        
        <!-- Модальное окно просмотра жалобы -->
        <div v-if="showReportModal" class="modal-overlay" @click.self="closeReportModal">
            <div class="modal modal-lg">
                <div class="modal-header">
                    <h3><i class="fas fa-flag"></i> Жалоба #{{ selectedReport?.id }}</h3>
                    <button @click="closeReportModal" class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <div class="modal-body">
                    <div v-if="selectedReport" class="report-details">
                        <div class="report-summary">
                            <div class="summary-item">
                                <span class="summary-label">Статус</span>
                                <span class="status-badge" :class="`status-${selectedReport.status}`">
                                    <i class="status-icon" :class="getStatusIcon(selectedReport.status)"></i>
                                    {{ getStatusText(selectedReport.status) }}
                                </span>
                            </div>
                            <div class="summary-item">
                                <span class="summary-label">Приоритет</span>
                                <span class="priority-badge" :class="`priority-${selectedReport.priority}`">
                                    <i class="priority-icon" :class="getPriorityIcon(selectedReport.priority)"></i>
                                    {{ getPriorityText(selectedReport.priority) }}
                                </span>
                            </div>
                            <div class="summary-item">
                                <span class="summary-label">Тип контента</span>
                                <span class="target-type-badge">
                                    <i :class="getTargetIcon(selectedReport.target_type)"></i>
                                    {{ getTargetTypeText(selectedReport.target_type) }}
                                </span>
                            </div>
                        </div>
                        
                        <div class="info-section">
                            <h4><i class="fas fa-info-circle"></i> Информация о жалобе</h4>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="info-label">ID жалобы:</span>
                                    <span class="info-value">#{{ selectedReport.id }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Отправитель:</span>
                                    <span class="info-value">{{ selectedReport.reporter_username || 'Неизвестно' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Жалоба на:</span>
                                    <span class="info-value">{{ selectedReport.reported_user_username || 'Не указано' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Дата отправки:</span>
                                    <span class="info-value">{{ formatDate(selectedReport.created_at) }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Назначено:</span>
                                    <span class="info-value">
                                        {{ selectedReport.assigned_admin_username || 'Не назначено' }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="info-section">
                            <h4><i class="fas fa-exclamation-triangle"></i> Причина жалобы</h4>
                            <div class="reason-box">
                                <div class="reason-title">
                                    <strong>{{ getReasonText(selectedReport.reason) }}</strong>
                                </div>
                                <div v-if="selectedReport.details" class="reason-details">
                                    <p>{{ selectedReport.details }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="info-section" v-if="selectedReport.target_info">
                            <h4><i class="fas fa-file-alt"></i> Контент</h4>
                            <div class="target-preview">
                                <div class="target-header">
                                    <div class="target-type-display">
                                        <i :class="getTargetIcon(selectedReport.target_type)"></i>
                                        <span>{{ getTargetTypeText(selectedReport.target_type).toUpperCase() }} #{{ selectedReport.target_id }}</span>
                                    </div>
                                </div>
                                
                                <div class="target-content">
                                    <div v-if="selectedReport.target_type === 'post'">
                                        <h5>{{ selectedReport.target_info.title }}</h5>
                                        <p>{{ selectedReport.target_info.content_preview }}</p>
                                        <div v-if="selectedReport.target_info.image_url" class="target-image">
                                            <img :src="selectedReport.target_info.image_url" alt="Изображение поста">
                                        </div>
                                        <div class="target-meta">
                                            <small>Автор: {{ selectedReport.target_info.author_username }}</small>
                                            <small>Дата: {{ formatDate(selectedReport.target_info.created_at) }}</small>
                                        </div>
                                    </div>
                                    
                                    <div v-else-if="selectedReport.target_type === 'comment'">
                                        <p class="comment-content">{{ selectedReport.target_info.content_preview }}</p>
                                        <div class="target-meta">
                                            <small>Автор: {{ selectedReport.target_info.author_username }}</small>
                                            <small>Пост: {{ selectedReport.target_info.post_title }}</small>
                                        </div>
                                    </div>
                                    
                                    <div v-else-if="selectedReport.target_type === 'product'">
                                        <h5>{{ selectedReport.target_info.title }}</h5>
                                        <p>{{ selectedReport.target_info.description_preview }}</p>
                                        <div class="target-meta">
                                            <small>Владелец: {{ selectedReport.target_info.owner_username }}</small>
                                            <small>Цена: {{ selectedReport.target_info.price }} ₽</small>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="target-actions">
                                    <button @click="viewTargetContent(selectedReport)" class="btn btn-outline">
                                        <i class="fas fa-external-link-alt"></i> Открыть на сайте
                                    </button>
                                    <button v-if="currentAdmin?.admin_level >= 4" @click="deleteContent(selectedReport)" class="btn btn-danger">
                                        <i class="fas fa-trash"></i> Удалить контент
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Действия модератора -->
                        <div class="info-section" v-if="selectedReport.status === 'pending' || selectedReport.status === 'reviewing'">
                            <h4><i class="fas fa-cogs"></i> Действия модератора</h4>
                            
                            <div v-if="!selectedReport.assigned_admin_id" class="action-section">
                                <p class="action-guide">Жалоба не назначена. Вы можете взять ее на проверку.</p>
                                <button @click="assignCurrentReport" class="btn btn-primary btn-block">
                                    <i class="fas fa-user-check"></i> Назначить себе на проверку
                                </button>
                            </div>
                            
                            <div v-else-if="selectedReport.assigned_admin_id === currentAdmin?.id" class="action-section">
                                <p class="action-guide">Жалоба назначена вам. Выберите действие:</p>
                                <div class="action-buttons-grid">
                                    <button @click="showResolveModal = true" class="btn btn-success">
                                        <i class="fas fa-check"></i> Завершить проверку
                                    </button>
                                    <button @click="showDismissModal = true" class="btn btn-warning">
                                        <i class="fas fa-times"></i> Отклонить жалобу
                                    </button>
                                    <button @click="deleteContent(selectedReport)" class="btn btn-danger">
                                        <i class="fas fa-trash"></i> Удалить контент
                                    </button>
                                </div>
                            </div>
                            
                            <div v-else class="action-section">
                                <p class="text-muted">
                                    <i class="fas fa-info-circle"></i>
                                    Жалоба назначена модератору: <strong>{{ selectedReport.assigned_admin_username }}</strong>
                                </p>
                                <button @click="reassignReport" class="btn btn-outline" v-if="currentAdmin?.admin_level >= 5">
                                    <i class="fas fa-user-cog"></i> Переназначить
                                </button>
                            </div>
                        </div>
                        
                        <!-- История обработки -->
                        <div class="info-section" v-if="selectedReport.resolution">
                            <h4><i class="fas fa-history"></i> Решение</h4>
                            <div class="resolution-box">
                                <div class="resolution-header">
                                    <strong>Тип решения: {{ getResolutionTypeText(selectedReport.resolution_type) }}</strong>
                                    <span class="resolution-date">
                                        <i class="fas fa-calendar-alt"></i>
                                        {{ formatDate(selectedReport.resolved_at) }}
                                    </span>
                                </div>
                                <div class="resolution-content">
                                    <p>{{ selectedReport.resolution }}</p>
                                </div>
                                <div class="resolution-meta">
                                    <small>Решено модератором: {{ selectedReport.assigned_admin_username }}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button @click="closeReportModal" class="btn btn-outline">
                        Закрыть
                    </button>
                    <button v-if="selectedReport?.status !== 'resolved' && selectedReport?.status !== 'dismissed'" 
                            @click="printReport" class="btn btn-secondary">
                        <i class="fas fa-print"></i> Печать
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Модальное окно завершения проверки -->
        <div v-if="showResolveModal" class="modal-overlay" @click.self="showResolveModal = false">
            <div class="modal">
                <div class="modal-header">
                    <h3><i class="fas fa-check-circle"></i> Завершить проверку</h3>
                    <button @click="showResolveModal = false" class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label><i class="fas fa-clipboard-check"></i> Тип решения:</label>
                        <select v-model="resolutionType" class="resolution-select" @change="updatePlaceholder">
                            <option value="warning">Предупреждение</option>
                            <option value="content_hidden">Контент скрыт</option>
                            <option value="content_deleted">Контент удален</option>
                            <option value="user_warned">Пользователю вынесено предупреждение</option>
                            <option value="user_banned">Пользователь забанен</option>
                            <option value="other">Другое</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-edit"></i> Комментарий:</label>
                        <textarea v-model="resolutionText" rows="4" class="resolution-textarea"
                                  :placeholder="resolutionPlaceholder"></textarea>
                        <div class="textarea-info">
                            <small>Опишите решение по жалобе. Будет видно в истории.</small>
                        </div>
                    </div>
                    
                    <div class="form-group" v-if="resolutionType === 'user_banned'">
                        <label><i class="fas fa-calendar-alt"></i> Срок бана:</label>
                        <select v-model="banDuration" class="ban-duration">
                            <option value="1">1 день</option>
                            <option value="3">3 дня</option>
                            <option value="7">7 дней</option>
                            <option value="30">30 дней</option>
                            <option value="permanent">Навсегда</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="showResolveModal = false" class="btn btn-outline">
                        <i class="fas fa-times"></i> Отмена
                    </button>
                    <button @click="confirmResolve" class="btn btn-success" :disabled="!resolutionText.trim()">
                        <i class="fas fa-check"></i> Завершить проверку
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Модальное окно отклонения жалобы -->
        <div v-if="showDismissModal" class="modal-overlay" @click.self="showDismissModal = false">
            <div class="modal">
                <div class="modal-header">
                    <h3><i class="fas fa-times-circle"></i> Отклонить жалобу</h3>
                    <button @click="showDismissModal = false" class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="warning-message">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>Вы уверены, что хотите отклонить эту жалобу?</p>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-comment-alt"></i> Причина отклонения:</label>
                        <textarea v-model="dismissalReason" rows="3" 
                                  placeholder="Укажите причину отклонения жалобы..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="showDismissModal = false" class="btn btn-outline">
                        Отмена
                    </button>
                    <button @click="confirmDismiss" class="btn btn-warning" :disabled="!dismissalReason.trim()">
                        <i class="fas fa-times"></i> Отклонить жалобу
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Модальное окно удаления контента -->
        <div v-if="showActionModal" class="modal-overlay" @click.self="showActionModal = false">
            <div class="modal">
                <div class="modal-header">
                    <h3><i class="fas fa-trash-alt"></i> Удаление контента</h3>
                    <button @click="showActionModal = false" class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="warning-message">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>Вы собираетесь удалить контент. Это действие нельзя отменить.</p>
                    </div>
                    
                    <div class="content-info">
                        <p><strong>Тип:</strong> {{ selectedReport?.target_type }}</p>
                        <p><strong>ID:</strong> {{ selectedReport?.target_id }}</p>
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-comment-alt"></i> Причина удаления:</label>
                        <textarea v-model="deleteReason" rows="3" 
                                  placeholder="Укажите причину удаления контента..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="showActionModal = false" class="btn btn-outline">
                        Отмена
                    </button>
                    <button @click="confirmDeleteContent" class="btn btn-danger" :disabled="!deleteReason.trim()">
                        <i class="fas fa-trash"></i> Удалить контент
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ReportsManagement',
    props: {
        reportsCount: {
            type: Number,
            default: 0
        }
    },
    data() {
        return {
            loading: false,
            reports: [],
            stats: {},
            
            // Фильтры
            statusFilter: 'pending',
            targetTypeFilter: '',
            priorityFilter: '',
            assignedFilter: 'all',
            
            // Пагинация
            currentPage: 1,
            perPage: 20,
            totalPages: 1,
            totalReports: 0,
            
            // Модальные окна
            showReportModal: false,
            showResolveModal: false,
            showDismissModal: false,
            showActionModal: false,
            
            // Выбранная жалоба
            selectedReport: null,
            
            // Формы
            resolutionText: '',
            resolutionType: 'warning',
            resolutionPlaceholder: 'Опишите решение по жалобе...',
            dismissalReason: '',
            deleteReason: '',
            banDuration: '1',
            
            currentAdmin: JSON.parse(localStorage.getItem('user') || '{}'),
            debounceTimer: null
        }
    },
    
    computed: {
        visiblePages() {
            const pages = []
            const maxVisible = 5
            let start = Math.max(1, this.currentPage - 2)
            let end = Math.min(this.totalPages, start + maxVisible - 1)
            
            if (end - start < maxVisible - 1) {
                start = Math.max(1, end - maxVisible + 1)
            }
            
            for (let i = start; i <= end; i++) {
                pages.push(i)
            }
            
            return pages
        }
    },
    
    methods: {
        async loadReports() {
            this.loading = true
            try {
                const token = localStorage.getItem('authToken')
                if (!token) {
                    this.$router.push('/login')
                    return
                }
                
                const params = new URLSearchParams({
                    page: this.currentPage,
                    per_page: this.perPage,
                    status: this.statusFilter
                })
                
                if (this.targetTypeFilter) {
                    params.append('target_type', this.targetTypeFilter)
                }
                
                if (this.priorityFilter) {
                    params.append('priority', this.priorityFilter)
                }
                
                if (this.assignedFilter === 'assigned_to_me') {
                    params.append('assigned_to_me', 'true')
                } else if (this.assignedFilter === 'unassigned') {
                    params.append('assigned_to_me', 'false')
                }
                
                const response = await fetch(`/api/admin/reports?${params}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                if (!response.ok) {
                    throw new Error('Ошибка загрузки жалоб')
                }
                
                const data = await response.json()
                this.reports = data.reports
                this.stats = data.stats
                this.totalReports = data.total
                this.totalPages = data.pages
                
            } catch (error) {
                console.error('Error loading reports:', error)
                this.$notify({
                    title: 'Ошибка',
                    text: 'Не удалось загрузить список жалоб',
                    type: 'error'
                })
            } finally {
                this.loading = false
            }
        },
        
        async loadStats() {
            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch('/api/admin/reports/stats', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                if (response.ok) {
                    const data = await response.json()
                    this.stats = data.stats
                }
            } catch (error) {
                console.error('Error loading stats:', error)
            }
        },
        
        viewReport(report) {
            this.selectedReport = report
            this.showReportModal = true
        },
        
        closeReportModal() {
            this.showReportModal = false
            this.selectedReport = null
            this.resolutionText = ''
            this.dismissalReason = ''
            this.deleteReason = ''
        },
        
        async assignReport(report) {
            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/admin/reports/${report.id}/assign`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })
                
                if (!response.ok) {
                    throw new Error('Ошибка назначения жалобы')
                }
                
                this.$notify({
                    title: 'Успешно',
                    text: 'Жалоба назначена вам на проверку',
                    type: 'success'
                })
                this.loadReports()
                this.$emit('update-count')
                
            } catch (error) {
                console.error('Error assigning report:', error)
                this.$notify({
                    title: 'Ошибка',
                    text: 'Не удалось назначить жалобу',
                    type: 'error'
                })
            }
        },
        
        assignCurrentReport() {
            if (this.selectedReport) {
                this.assignReport(this.selectedReport)
                this.closeReportModal()
            }
        },
        
        resolveReport(report) {
            this.selectedReport = report
            this.showResolveModal = true
        },
        
        dismissReport(report) {
            this.selectedReport = report
            this.showDismissModal = true
        },
        
        deleteContent(report) {
            this.selectedReport = report
            this.showActionModal = true
        },
        
        updatePlaceholder() {
            const placeholders = {
                'warning': 'Опишите предупреждение...',
                'content_hidden': 'Укажите причину скрытия контента...',
                'content_deleted': 'Укажите причину удаления контента...',
                'user_warned': 'Опишите предупреждение пользователю...',
                'user_banned': 'Укажите причину бана и его срок...',
                'other': 'Опишите решение...'
            }
            this.resolutionPlaceholder = placeholders[this.resolutionType] || 'Опишите решение...'
        },
        
        async confirmResolve() {
            if (!this.selectedReport || !this.resolutionText.trim()) return
            
            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/admin/reports/${this.selectedReport.id}/resolve`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        resolution: this.resolutionText,
                        resolution_type: this.resolutionType,
                        ban_duration: this.banDuration
                    })
                })
                
                if (!response.ok) {
                    throw new Error('Ошибка завершения проверки')
                }
                
                this.$notify({
                    title: 'Успешно',
                    text: 'Жалоба успешно обработана',
                    type: 'success'
                })
                this.showResolveModal = false
                this.closeReportModal()
                this.loadReports()
                this.$emit('update-count')
                
            } catch (error) {
                console.error('Error resolving report:', error)
                this.$notify({
                    title: 'Ошибка',
                    text: 'Не удалось завершить проверку',
                    type: 'error'
                })
            }
        },
        
        async confirmDismiss() {
            if (!this.selectedReport || !this.dismissalReason.trim()) return
            
            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/admin/reports/${this.selectedReport.id}/dismiss`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        reason: this.dismissalReason
                    })
                })
                
                if (!response.ok) {
                    throw new Error('Ошибка отклонения жалобы')
                }
                
                this.$notify({
                    title: 'Успешно',
                    text: 'Жалоба отклонена',
                    type: 'success'
                })
                this.showDismissModal = false
                this.closeReportModal()
                this.loadReports()
                this.$emit('update-count')
                
            } catch (error) {
                console.error('Error dismissing report:', error)
                this.$notify({
                    title: 'Ошибка',
                    text: 'Не удалось отклонить жалобу',
                    type: 'error'
                })
            }
        },
        
        async confirmDeleteContent() {
            if (!this.selectedReport || !this.deleteReason.trim()) return
            
            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/admin/reports/${this.selectedReport.id}/delete-content`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        reason: this.deleteReason
                    })
                })
                
                if (!response.ok) {
                    throw new Error('Ошибка удаления контента')
                }
                
                this.$notify({
                    title: 'Успешно',
                    text: 'Контент удален',
                    type: 'success'
                })
                this.showActionModal = false
                this.closeReportModal()
                this.loadReports()
                
            } catch (error) {
                console.error('Error deleting content:', error)
                this.$notify({
                    title: 'Ошибка',
                    text: 'Не удалось удалить контент',
                    type: 'error'
                })
            }
        },
        
        getTargetIcon(type) {
            const icons = {
                'post': 'fas fa-newspaper',
                'comment': 'fas fa-comment',
                'product': 'fas fa-shopping-cart',
                'manual': 'fas fa-book'
            }
            return icons[type] || 'fas fa-file'
        },
        
        getStatusIcon(status) {
            const icons = {
                'pending': 'fas fa-clock',
                'reviewing': 'fas fa-search',
                'resolved': 'fas fa-check',
                'dismissed': 'fas fa-times'
            }
            return icons[status] || 'fas fa-question'
        },
        
        getPriorityIcon(priority) {
            const icons = {
                'high': 'fas fa-exclamation-circle',
                'medium': 'fas fa-exclamation',
                'low': 'fas fa-info-circle'
            }
            return icons[priority] || 'fas fa-question'
        },
        
        getTargetTypeText(type) {
            const texts = {
                'post': 'Пост',
                'comment': 'Комментарий',
                'product': 'Объявление',
                'manual': 'Мануал'
            }
            return texts[type] || type
        },
        
        getStatusText(status) {
            const texts = {
                'pending': 'Ожидает',
                'reviewing': 'На проверке',
                'resolved': 'Решена',
                'dismissed': 'Отклонена'
            }
            return texts[status] || status
        },
        
        getPriorityText(priority) {
            const texts = {
                'high': 'Высокий',
                'medium': 'Средний',
                'low': 'Низкий'
            }
            return texts[priority] || priority
        },
        
        getResolutionTypeText(type) {
            const texts = {
                'warning': 'Предупреждение',
                'content_hidden': 'Контент скрыт',
                'content_deleted': 'Контент удален',
                'user_warned': 'Пользователю вынесено предупреждение',
                'user_banned': 'Пользователь забанен',
                'dismissed': 'Жалоба отклонена',
                'other': 'Другое'
            }
            return texts[type] || type
        },

        getReasonText(reason) {
            const texts = {
                'spam': 'Спам',
                'abuse': 'Оскорбления, агрессия',
                'hate_speech': 'Разжигание ненависти',
                'adult_content': 'Контент для взрослых',
                'illegal_content': 'Незаконный контент',
                'misinformation': 'Ложная информация',
                'copyright_violation': 'Нарушение авторских прав',
                'impersonation': 'Выдача себя за другого',
                'harassment': 'Преследование',
                'other': 'Другое',
            }
            return texts[reason] || reason
        },
        
        formatDate(dateString) {
            if (!dateString) return '-'
            try {
                const date = new Date(dateString)
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                })
            } catch (e) {
                return '-'
            }
        },
        
        getRelativeTime(dateString) {
            if (!dateString) return ''
            try {
                const date = new Date(dateString)
                const now = new Date()
                const diff = now - date
                const minutes = Math.floor(diff / (1000 * 60))
                const hours = Math.floor(diff / (1000 * 60 * 60))
                const days = Math.floor(diff / (1000 * 60 * 60 * 24))
                
                if (minutes < 1) return 'только что'
                if (minutes < 60) return `${minutes} мин назад`
                if (hours < 24) return `${hours} ч назад`
                if (days === 1) return 'вчера'
                if (days < 7) return `${days} дн назад`
                return date.toLocaleDateString('ru-RU')
            } catch (e) {
                return ''
            }
        },
        
        viewTargetContent(report) {
            let url = ''
            switch (report.target_type) {
                case 'post':
                    url = `/community/post/${report.target_id}`
                    break
                case 'comment':
                    url = `/community/post/${report.target_info?.post_id || ''}`
                    break
                case 'product':
                    url = `/market/product/${report.target_id}`
                    break
                case 'manual':
                    url = `/manuals/${report.target_id}`
                    break
            }
            
            if (url) {
                window.open(url, '_blank')
            }
        },
        
        refreshData() {
            this.loadReports()
            this.loadStats()
        },
        
        forceRefresh() {
            this.loadStats()
            this.$emit('update-count')
        },
        
        setFilter(filter) {
            if (filter === 'all') {
                this.statusFilter = 'all'
            } else if (filter === 'pending' || filter === 'reviewing') {
                this.statusFilter = filter
            } else if (filter === 'assigned_to_me') {
                this.assignedFilter = 'assigned_to_me'
            }
            this.loadReports()
        },
        
        resetFilters() {
            this.statusFilter = 'pending'
            this.targetTypeFilter = ''
            this.priorityFilter = ''
            this.assignedFilter = 'all'
            this.currentPage = 1
            this.loadReports()
        },
        
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page
                this.loadReports()
            }
        },
        
        exportReports() {
            // Логика экспорта
            console.log('Exporting reports...')
        },
        
        printReport() {
            window.print()
        },
        
        reassignReport() {
            // Логика переназначения
            console.log('Reassigning report...')
        }
    },
    
    mounted() {
        this.loadReports()
        this.loadStats()
        this.updatePlaceholder()
    }
}
</script>

<style scoped>
.reports-management {
    padding: 20px;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.page-header h1 {
    font-size: 28px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 15px;
}

.page-header h1 i {
    color: var(--primary);
}

.header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}

/* Статистика */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 25px;
    display: flex;
    align-items: center;
    gap: 20px;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.1);
}

.stat-card.active {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.1);
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.stat-info {
    flex: 1;
}

.stat-info h3 {
    font-size: 32px;
    margin-bottom: 5px;
    color: var(--text);
    font-weight: 700;
}

.stat-info p {
    color: var(--text-secondary);
    font-size: 14px;
}

.stat-arrow {
    color: var(--text-secondary);
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.stat-card:hover .stat-arrow {
    opacity: 1;
}

/* Фильтры */
.filters {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    flex-wrap: wrap;
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 200px;
    flex: 1;
}

.filter-group label {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-group select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 14px;
    transition: all 0.3s ease;
}

.filter-group select:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

/* Таблица */
.reports-table-container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    overflow: hidden;
    position: relative;
    min-height: 400px;
}

.table-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0, 0, 0, 0.2);
}

.table-info {
    color: var(--text-secondary);
    font-size: 14px;
}

.table-actions {
    display: flex;
    gap: 10px;
}

.table-responsive {
    overflow-x: auto;
}

.reports-table {
    width: 100%;
    border-collapse: collapse;
}

.reports-table th {
    background: rgba(255, 255, 255, 0.05);
    padding: 15px;
    text-align: left;
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    white-space: nowrap;
}

.reports-table th.text-center {
    text-align: center;
}

.reports-table td {
    padding: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    vertical-align: middle;
}

.reports-table td.text-center {
    text-align: center;
}

.report-row {
    cursor: pointer;
    transition: all 0.3s ease;
}

.report-row:hover {
    background: rgba(255, 255, 255, 0.03);
}

.report-row.priority-high {
    border-left: 4px solid var(--danger);
}

.report-row.priority-medium {
    border-left: 4px solid var(--warning);
}

.report-row.priority-low {
    border-left: 4px solid var(--success);
}

/* Элементы таблицы */
.report-id {
    color: var(--text-secondary);
    font-family: 'Consolas', monospace;
    font-size: 14px;
    font-weight: 600;
}

.report-info .report-reason {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.report-info strong {
    color: var(--text);
    font-size: 14px;
    line-height: 1.4;
}

.report-meta {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.report-meta small {
    color: var(--text-secondary);
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.text-truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
}

.report-target .target-type {
    display: flex;
    align-items: center;
    gap: 12px;
}

.target-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: rgba(74, 108, 247, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4a6cf7;
    font-size: 16px;
}

.target-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.target-type-text {
    color: var(--text);
    font-size: 14px;
    font-weight: 500;
}

.user-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    font-size: 13px;
    color: var(--text);
}

.admin-assigned {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text);
}

.report-date {
    min-width: 140px;
}

.date-text {
    color: var(--text);
    font-size: 13px;
    margin-bottom: 4px;
}

.date-relative {
    color: var(--text-secondary);
    font-size: 12px;
}

/* Бейджи */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-icon {
    font-size: 11px;
}

.status-pending {
    background: rgba(255, 193, 7, 0.15);
    color: #ffc107;
    border: 1px solid rgba(255, 193, 7, 0.3);
}

.status-reviewing {
    background: rgba(0, 123, 255, 0.15);
    color: #007bff;
    border: 1px solid rgba(0, 123, 255, 0.3);
}

.status-resolved {
    background: rgba(40, 167, 69, 0.15);
    color: #28a745;
    border: 1px solid rgba(40, 167, 69, 0.3);
}

.status-dismissed {
    background: rgba(108, 117, 125, 0.15);
    color: #6c757d;
    border: 1px solid rgba(108, 117, 125, 0.3);
}

.priority-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.priority-icon {
    font-size: 11px;
}

.priority-high {
    background: rgba(220, 53, 69, 0.15);
    color: var(--danger);
    border: 1px solid rgba(220, 53, 69, 0.3);
}

.priority-medium {
    background: rgba(255, 193, 7, 0.15);
    color: var(--warning);
    border: 1px solid rgba(255, 193, 7, 0.3);
}

.priority-low {
    background: rgba(40, 167, 69, 0.15);
    color: var(--success);
    border: 1px solid rgba(40, 167, 69, 0.3);
}

/* Действия в таблице */
.actions {
    width: 160px;
}

.action-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
}

.btn-action {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.btn-action:hover {
    transform: translateY(-2px);
    border-color: currentColor;
}

.btn-view:hover {
    background: rgba(74, 108, 247, 0.2);
    color: #4a6cf7;
}

.btn-assign:hover {
    background: rgba(255, 193, 7, 0.2);
    color: #ffc107;
}

.btn-resolve:hover {
    background: rgba(40, 167, 69, 0.2);
    color: #28a745;
}

.btn-dismiss:hover {
    background: rgba(255, 193, 7, 0.2);
    color: #ffc107;
}

/* Empty state */
.empty-state {
    padding: 60px 20px;
    text-align: center;
    color: var(--text-secondary);
}

.empty-state-icon {
    font-size: 60px;
    margin-bottom: 20px;
    opacity: 0.3;
    color: var(--primary);
}

.empty-state h3 {
    font-size: 24px;
    margin-bottom: 10px;
    color: var(--text);
}

.empty-state p {
    margin-bottom: 20px;
    font-size: 16px;
}

/* Пагинация */
.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    flex-wrap: wrap;
    gap: 20px;
}

.pagination-info {
    color: var(--text-secondary);
    font-size: 14px;
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 10px;
}

.pagination-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(0, 0, 0, 0.3);
    color: var(--text);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
}

.pagination-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.page-numbers {
    display: flex;
    gap: 5px;
}

.page-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    border: none;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 14px;
}

.page-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}

.page-btn.active {
    background: var(--primary);
    color: white;
}

.pagination-size .per-page-select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 8px 12px;
    color: var(--text);
    font-size: 14px;
}

/* Loading overlay */
.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(10, 10, 15, 0.8);
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Модальные окна */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    padding: 20px;
}

.modal {
    background: rgba(20, 20, 30, 0.98);
    border-radius: 20px;
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
}

.modal-lg {
    max-width: 800px;
}

.modal-header {
    padding: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0, 0, 0, 0.2);
}

.modal-header h3 {
    font-size: 20px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}

.modal-close {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: transparent;
    color: var(--text);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
}

.modal-body {
    padding: 25px;
    overflow-y: auto;
    max-height: 60vh;
}

.modal-footer {
    padding: 25px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    background: rgba(0, 0, 0, 0.2);
}

/* Стили для модалки с деталями жалобы */
.report-summary {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
}

.summary-label {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.target-type-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(74, 108, 247, 0.1);
    border-radius: 20px;
    color: #4a6cf7;
    font-size: 14px;
    font-weight: 500;
}

.info-section {
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.info-section h4 {
    font-size: 18px;
    color: var(--text);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.info-label {
    color: var(--text-secondary);
    font-size: 13px;
}

.info-value {
    color: var(--text);
    font-size: 14px;
    font-weight: 500;
}

.reason-box {
    background: rgba(255, 71, 87, 0.05);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(255, 71, 87, 0.1);
}

.reason-title {
    margin-bottom: 15px;
}

.reason-title strong {
    color: var(--text);
    font-size: 16px;
}

.reason-details {
    color: var(--text-secondary);
    font-size: 14px;
    line-height: 1.6;
}

.target-preview {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.target-header {
    padding: 15px 20px;
    background: rgba(0, 0, 0, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.target-type-display {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text);
    font-weight: 500;
}

.target-content {
    padding: 20px;
}

.target-content h5 {
    color: var(--text);
    font-size: 18px;
    margin-bottom: 10px;
}

.target-content p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 15px;
}

.comment-content {
    background: rgba(255, 255, 255, 0.03);
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #4a6cf7;
}

.target-meta {
    display: flex;
    gap: 15px;
    color: var(--text-secondary);
    font-size: 13px;
    margin-top: 15px;
}

.target-image {
    margin: 15px 0;
    max-width: 300px;
}

.target-image img {
    width: 100%;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.target-actions {
    padding: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    gap: 10px;
}

.action-section {
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.action-guide {
    color: var(--text-secondary);
    margin-bottom: 15px;
    font-size: 14px;
}

.action-buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
}

.btn-block {
    width: 100%;
}

.resolution-box {
    background: rgba(40, 167, 69, 0.05);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(40, 167, 69, 0.1);
}

.resolution-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.resolution-header strong {
    color: var(--text);
}

.resolution-date {
    color: var(--text-secondary);
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.resolution-content {
    color: var(--text);
    line-height: 1.6;
    margin-bottom: 10px;
}

.resolution-meta {
    color: var(--text-secondary);
    font-size: 13px;
}

/* Стили для модалки завершения */
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text);
    font-weight: 500;
    margin-bottom: 8px;
}

.resolution-select,
.ban-duration {
    width: 100%;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 14px;
}

.resolution-textarea {
    width: 100%;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 15px;
    color: var(--text);
    font-size: 14px;
    resize: vertical;
    min-height: 100px;
    transition: all 0.3s ease;
}

.resolution-textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

.textarea-info {
    color: var(--text-secondary);
    font-size: 12px;
    margin-top: 5px;
}

/* Стили для модалки отклонения */
.warning-message {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: rgba(255, 193, 7, 0.1);
    border-radius: 10px;
    border: 1px solid rgba(255, 193, 7, 0.2);
    margin-bottom: 20px;
}

.warning-message i {
    color: #ffc107;
    font-size: 20px;
}

.warning-message p {
    color: var(--text);
    margin: 0;
}

.content-info {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.content-info p {
    margin: 5px 0;
    color: var(--text);
}

.content-info strong {
    color: var(--text-secondary);
}

/* Кнопки */
.btn {
    padding: 12px 24px;
    border-radius: 10px;
    border: 1px solid transparent;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.btn-primary:hover:not(:disabled) {
    background: #ff5722;
    border-color: #ff5722;
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
    border-color: rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
}

.btn-success {
    background: var(--success);
    color: white;
    border-color: var(--success);
}

.btn-success:hover:not(:disabled) {
    background: #218838;
    border-color: #1e7e34;
}

.btn-warning {
    background: var(--warning);
    color: white;
    border-color: var(--warning);
}

.btn-warning:hover:not(:disabled) {
    background: #e0a800;
    border-color: #d39e00;
}

.btn-danger {
    background: var(--danger);
    color: white;
    border-color: var(--danger);
}

.btn-danger:hover:not(:disabled) {
    background: #c82333;
    border-color: #bd2130;
}

.btn-outline {
    background: transparent;
    color: var(--text);
    border-color: rgba(255, 255, 255, 0.2);
}

.btn-outline:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
}

.btn-sm {
    padding: 8px 16px;
    font-size: 13px;
}

@media (max-width: 1200px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .info-grid {
        grid-template-columns: 1fr;
    }
    
    .summary-item {
        flex: none;
        min-width: 150px;
    }
}

@media (max-width: 768px) {
    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .header-actions {
        width: 100%;
        flex-direction: column;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .filters {
        flex-direction: column;
    }
    
    .filter-group {
        min-width: 100%;
    }
    
    .table-header {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }
    
    .reports-table {
        display: block;
    }
    
    .reports-table th,
    .reports-table td {
        padding: 10px;
    }
    
    .actions {
        width: auto;
    }
    
    .action-buttons {
        flex-wrap: wrap;
    }
    
    .pagination {
        flex-direction: column;
        text-align: center;
    }
    
    .pagination-controls {
        order: 2;
    }
    
    .pagination-info,
    .pagination-size {
        order: 1;
    }
    
    .modal-lg {
        max-width: 95%;
    }
    
    .report-summary {
        flex-direction: column;
    }
    
    .action-buttons-grid {
        grid-template-columns: 1fr;
    }
    
    .target-actions {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
        margin-bottom: 5px;
    }
}
</style>