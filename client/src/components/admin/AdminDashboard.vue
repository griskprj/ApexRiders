<template>
    <div class="admin-dashboard">
        <!-- Навигация админки -->
        <nav class="admin-navbar">
            <div class="admin-navbar-content">
                <div class="admin-brand">
                    <i class="fas fa-shield-alt"></i>
                    <span>Админ-панель</span>
                </div>
                
                <div class="admin-user-info">
                    <span class="admin-username">{{ currentAdmin?.username || 'Администратор' }}</span>
                    <span class="admin-badge" :class="getAdminBadgeClass">
                        {{ getCurrentAdminLevelText }}
                    </span>
                    <button @click="logout" class="btn btn-outline btn-sm">
                        <i class="fas fa-sign-out-alt"></i> Выйти
                    </button>
                </div>
            </div>
        </nav>
        
        <div class="admin-container">
            <!-- Боковое меню -->
            <aside class="admin-sidebar">
                <div class="sidebar-header">
                    <h3><i class="fas fa-user-circle"></i> Управление</h3>
                </div>
                
                <div class="sidebar-menu">
                    <button 
                        @click="currentView = 'dashboard'" 
                        :class="{ 'active': currentView === 'dashboard' }"
                        class="sidebar-item"
                    >
                        <i class="fas fa-tachometer-alt"></i>
                        <span>Дашборд</span>
                    </button>
                    
                    <button 
                        @click="currentView = 'users'" 
                        :class="{ 'active': currentView === 'users' }"
                        class="sidebar-item"
                    >
                        <i class="fas fa-users"></i>
                        <span>Пользователи</span>
                        <span class="badge">{{ stats.total_users || 0 }}</span>
                    </button>
                    
                    <div class="sidebar-section" v-if="currentAdmin?.admin_level >= 2">
                        <h4><i class="fas fa-newspaper"></i> Контент</h4>
                        <button class="sidebar-item">
                            <i class="fas fa-file-alt"></i>
                            <span>Посты</span>
                        </button>
                        <button class="sidebar-item">
                            <i class="fas fa-book"></i>
                            <span>Мануалы</span>
                        </button>
                    </div>
                    
                    <div class="sidebar-section" v-if="currentAdmin?.admin_level >= 4">
                        <h4><i class="fas fa-flag"></i> Модерация</h4>
                        <button class="sidebar-item">
                            <i class="fas fa-exclamation-triangle"></i>
                            <span>Жалобы</span>
                            <span class="badge badge-danger">3</span>
                        </button>
                    </div>
                    
                    <div class="sidebar-section" v-if="currentAdmin?.admin_level >= 5">
                        <h4><i class="fas fa-cogs"></i> Система</h4>
                        <button class="sidebar-item">
                            <i class="fas fa-sliders-h"></i>
                            <span>Настройки</span>
                        </button>
                        <button class="sidebar-item">
                            <i class="fas fa-history"></i>
                            <span>Логи</span>
                        </button>
                    </div>
                </div>
                
                <div class="sidebar-footer">
                    <div class="system-status">
                        <div class="status-indicator active"></div>
                        <span>Система активна</span>
                    </div>
                    <button @click="goToSite" class="btn btn-outline btn-sm">
                        <i class="fas fa-external-link-alt"></i> На сайт
                    </button>
                </div>
            </aside>
            
            <!-- Основной контент -->
            <main class="admin-main">
                <!-- Дашборд -->
                <div v-if="currentView === 'dashboard'" class="dashboard-content">
                    <div class="page-header">
                        <h1><i class="fas fa-tachometer-alt"></i> Дашборд</h1>
                        <div class="header-actions">
                            <button @click="refreshData" class="btn btn-outline">
                                <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i> Обновить
                            </button>
                        </div>
                    </div>
                    
                    <!-- Статистика -->
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-icon" style="background: rgba(74, 108, 247, 0.2); color: #4a6cf7;">
                                <i class="fas fa-user-friends"></i>
                            </div>
                            <div class="stat-info">
                                <h3>{{ stats.total_users || 0 }}</h3>
                                <p>Всего пользователей</p>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon" style="background: rgba(50, 205, 50, 0.2); color: #32cd32;">
                                <i class="fas fa-check-circle"></i>
                            </div>
                            <div class="stat-info">
                                <h3>{{ stats.verified_users || 0 }}</h3>
                                <p>Верифицировано</p>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon" style="background: rgba(255, 69, 0, 0.2); color: #ff4500;">
                                <i class="fas fa-user-shield"></i>
                            </div>
                            <div class="stat-info">
                                <h3>{{ stats.admin_users || 0 }}</h3>
                                <p>Администраторы</p>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon" style="background: rgba(255, 107, 107, 0.2); color: #ff6b6b;">
                                <i class="fas fa-user-plus"></i>
                            </div>
                            <div class="stat-info">
                                <h3>{{ stats.new_today || 0 }}</h3>
                                <p>Новых сегодня</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Блоки с информацией -->
                    <div class="info-grid">
                        <!-- Текущий администратор -->
                        <div class="info-card">
                            <div class="info-card-header">
                                <h3><i class="fas fa-user-shield"></i> Ваш аккаунт</h3>
                            </div>
                            <div class="info-card-body">
                                <div class="user-info-large">
                                    <div class="user-avatar-large">
                                        <i class="fas fa-user"></i>
                                    </div>
                                    <div class="user-details-large">
                                        <h4>{{ currentAdmin?.username || 'Администратор' }}</h4>
                                        <p>{{ currentAdmin?.email || 'Email не указан' }}</p>
                                        <div class="user-status">
                                            <span class="badge" :class="getAdminBadgeClass">{{ getCurrentAdminLevelText }}</span>
                                            <span v-if="currentAdmin?.is_super_admin" class="badge badge-super">
                                                <i class="fas fa-star"></i> Супер-админ
                                            </span>
                                            <span v-if="currentAdmin?.is_verified" class="badge badge-verified">
                                                <i class="fas fa-check-circle"></i> Верифицирован
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <div class="user-stats">
                                    <div class="stat-item">
                                        <i class="fas fa-calendar-alt"></i>
                                        <div>
                                            <small>Дата регистрации</small>
                                            <p>{{ formatDate(currentAdmin?.join_at) }}</p>
                                        </div>
                                    </div>
                                    <div class="stat-item">
                                        <i class="fas fa-sign-in-alt"></i>
                                        <div>
                                            <small>Последний вход в админку</small>
                                            <p>{{ formatDate(currentAdmin?.last_admin_login) }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Последние пользователи -->
                        <div class="info-card">
                            <div class="info-card-header">
                                <h3><i class="fas fa-users"></i> Последние регистрации</h3>
                            </div>
                            <div class="info-card-body">
                                <div v-if="recentUsers.length === 0" class="empty-list">
                                    <i class="fas fa-user-clock"></i>
                                    <p>Нет новых пользователей</p>
                                </div>
                                <div v-else class="users-list">
                                    <div v-for="user in recentUsers" :key="user.id" class="user-item">
                                        <div class="user-item-avatar">
                                            <i class="fas fa-user"></i>
                                        </div>
                                        <div class="user-item-info">
                                            <strong>{{ user.username }}</strong>
                                            <small>{{ user.email }}</small>
                                        </div>
                                        <div class="user-item-date">
                                            {{ formatDateShort(user.join_at) }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Быстрые действия -->
                        <div class="info-card">
                            <div class="info-card-header">
                                <h3><i class="fas fa-bolt"></i> Быстрые действия</h3>
                            </div>
                            <div class="info-card-body">
                                <div class="quick-actions">
                                    <button @click="currentView = 'users'" class="quick-action">
                                        <i class="fas fa-users"></i>
                                        <span>Управление пользователями</span>
                                    </button>
                                    <button class="quick-action" :disabled="currentAdmin?.admin_level < 2">
                                        <i class="fas fa-plus-circle"></i>
                                        <span>Добавить пост</span>
                                    </button>
                                    <button class="quick-action" :disabled="currentAdmin?.admin_level < 4">
                                        <i class="fas fa-flag"></i>
                                        <span>Проверить жалобы</span>
                                    </button>
                                    <button class="quick-action" :disabled="currentAdmin?.admin_level < 5">
                                        <i class="fas fa-chart-line"></i>
                                        <span>Аналитика сайта</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Управление пользователями -->
                <div v-if="currentView === 'users'" class="admin-users">
                    <div class="page-header">
                        <h1><i class="fas fa-users"></i> Управление пользователями</h1>
                        <div class="header-actions">
                            <div class="search-box">
                                <i class="fas fa-search"></i>
                                <input 
                                    type="text" 
                                    v-model="searchQuery"
                                    placeholder="Поиск по имени или email..."
                                    @input="debouncedSearch"
                                >
                            </div>
                            <button @click="refreshData" class="btn btn-outline">
                                <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i> Обновить
                            </button>
                        </div>
                    </div>
                    
                    <!-- Фильтры -->
                    <div class="filters">
                        <div class="filter-group">
                            <label>Уровень администратора:</label>
                            <select v-model="adminLevelFilter" @change="loadUsers">
                                <option value="">Все уровни</option>
                                <option value="0">Пользователи (0)</option>
                                <option value="1">Авторы мануалов (1)</option>
                                <option value="2">Модераторы постов (2)</option>
                                <option value="3">Модераторы мануалов (3)</option>
                                <option value="4">Супер-модераторы (4)</option>
                                <option value="5">Супервайзеры (5)</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label>Показать:</label>
                            <select v-model="perPage" @change="loadUsers">
                                <option value="10">10 на странице</option>
                                <option value="20">20 на странице</option>
                                <option value="50">50 на странице</option>
                                <option value="100">100 на странице</option>
                            </select>
                        </div>
                    </div>
                    
                    <!-- Таблица пользователей -->
                    <div class="users-table-container">
                        <div v-if="loading" class="loading-overlay">
                            <div class="spinner"></div>
                            <p>Загрузка данных...</p>
                        </div>
                        
                        <table class="users-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Пользователь</th>
                                    <th>Email</th>
                                    <th>Роль</th>
                                    <th>Уровень админа</th>
                                    <th>Дата регистрации</th>
                                    <th>Активность</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="user in users" :key="user.id">
                                    <td class="user-id">#{{ user.id }}</td>
                                    <td class="user-info">
                                        <div class="user-avatar">
                                            <i class="fas fa-user"></i>
                                        </div>
                                        <div class="user-details">
                                            <strong>{{ user.username }}</strong>
                                            <div class="user-verified" v-if="user.is_verified">
                                                <i class="fas fa-check-circle"></i>
                                                <span>Верифицирован</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td>{{ user.email }}</td>
                                    <td>
                                        <span class="role-badge">{{ user.role }}</span>
                                    </td>
                                    <td>
                                        <span class="admin-level" :class="'level-' + user.admin_level">
                                            {{ getUserAdminLevelText(user.admin_level) }}
                                            <span v-if="user.is_super_admin" class="super-admin">★</span>
                                        </span>
                                    </td>
                                    <td>
                                        {{ formatDate(user.join_at) }}
                                    </td>
                                    <td>
                                        <div class="activity-stats">
                                            <div class="activity-item">
                                                <i class="fas fa-file-alt"></i>
                                                <span>{{ user.post_count || 0 }}</span>
                                            </div>
                                            <div class="activity-item">
                                                <i class="fas fa-shopping-cart"></i>
                                                <span>{{ user.product_count || 0 }}</span>
                                            </div>
                                            <div class="activity-item">
                                                <i class="fas fa-book"></i>
                                                <span>{{ user.manual_count || 0 }}</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="actions">
                                        <button 
                                            @click="editUser(user)" 
                                            class="btn-action btn-edit"
                                            title="Редактировать"
                                            :disabled="currentAdmin?.id === user.id"
                                        >
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button 
                                            @click="confirmDelete(user)" 
                                            class="btn-action btn-delete"
                                            title="Удалить"
                                            :disabled="currentAdmin?.id === user.id"
                                        >
                                            <i class="fas fa-trash"></i>
                                        </button>
                                        <button 
                                            @click="viewUserDetails(user)" 
                                            class="btn-action btn-view"
                                            title="Подробнее"
                                        >
                                            <i class="fas fa-eye"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <div v-if="!loading && users.length === 0" class="empty-state">
                            <i class="fas fa-users-slash"></i>
                            <h3>Пользователи не найдены</h3>
                            <p>Попробуйте изменить параметры поиска</p>
                        </div>
                    </div>
                    
                    <!-- Пагинация -->
                    <div class="pagination" v-if="totalPages > 1">
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
                            
                            <span v-if="showEllipsis" class="ellipsis">...</span>
                        </div>
                        
                        <button 
                            @click="goToPage(currentPage + 1)" 
                            :disabled="currentPage === totalPages"
                            class="pagination-btn"
                        >
                            <i class="fas fa-chevron-right"></i>
                        </button>
                        
                        <div class="pagination-info">
                            Страница {{ currentPage }} из {{ totalPages }}
                            <span class="total-info">({{ totalUsers }} всего)</span>
                        </div>
                    </div>
                </div>
            </main>
        </div>
        
        <!-- Модальные окна (общие для всей админки) -->
        
        <!-- Модальное окно удаления -->
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
            <div class="modal">
                <div class="modal-header">
                    <h3><i class="fas fa-exclamation-triangle"></i> Подтверждение удаления</h3>
                    <button @click="closeDeleteModal" class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <p>Вы уверены, что хотите удалить пользователя <strong>{{ userToDelete?.username }}</strong>?</p>
                    <p class="warning-text">
                        <i class="fas fa-exclamation-circle"></i>
                        Это действие невозможно отменить. Будут удалены все данные пользователя.
                    </p>
                    
                    <div class="user-delete-info" v-if="userToDelete">
                        <div class="info-item">
                            <span>ID:</span>
                            <strong>#{{ userToDelete.id }}</strong>
                        </div>
                        <div class="info-item">
                            <span>Email:</span>
                            <strong>{{ userToDelete.email }}</strong>
                        </div>
                        <div class="info-item">
                            <span>Создано постов:</span>
                            <strong>{{ userToDelete.post_count }}</strong>
                        </div>
                        <div class="info-item">
                            <span>Объявлений:</span>
                            <strong>{{ userToDelete.product_count }}</strong>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="closeDeleteModal" class="btn btn-outline">
                        Отмена
                    </button>
                    <button @click="deleteUser" class="btn btn-danger" :disabled="deleting">
                        <span v-if="deleting">
                            <i class="fas fa-spinner fa-spin"></i> Удаление...
                        </span>
                        <span v-else>
                            <i class="fas fa-trash"></i> Удалить пользователя
                        </span>
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Модальное окно редактирования -->
        <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
            <div class="modal modal-lg">
                <div class="modal-header">
                    <h3><i class="fas fa-edit"></i> Редактирование пользователя</h3>
                    <button @click="closeEditModal" class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="edit-form" v-if="userToEdit">
                        <div class="form-row">
                            <div class="form-group">
                                <label>Имя пользователя</label>
                                <input type="text" v-model="userToEdit.username" disabled>
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" v-model="userToEdit.email" disabled>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label>Уровень администратора</label>
                                <select v-model="userToEdit.admin_level">
                                    <option value="0">Пользователь (0)</option>
                                    <option value="1">Автор мануалов (1)</option>
                                    <option value="2">Модератор постов (2)</option>
                                    <option value="3">Модератор мануалов (3)</option>
                                    <option value="4">Супер-модератор (4)</option>
                                    <option value="5">Супервайзер (5)</option>
                                </select>
                                <p class="help-text">
                                    Уровень определяет права доступа в админ-панели
                                </p>
                            </div>
                            
                            <div class="form-group">
                                <label>Статус верификации</label>
                                <div class="checkbox-group">
                                    <label class="checkbox-label">
                                        <input type="checkbox" v-model="userToEdit.is_verified">
                                        <span class="checkbox-custom"></span>
                                        <span>Верифицированный пользователь</span>
                                    </label>
                                </div>
                                <p class="help-text">
                                    Верифицированные пользователи могут создавать мануалы
                                </p>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label class="checkbox-label">
                                <input type="checkbox" v-model="userToEdit.is_super_admin">
                                <span class="checkbox-custom"></span>
                                <span>Супер администратор</span>
                            </label>
                            <p class="help-text warning">
                                <i class="fas fa-exclamation-triangle"></i>
                                Супер администратор имеет полный доступ ко всем функциям
                            </p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="closeEditModal" class="btn btn-outline">
                        Отмена
                    </button>
                    <button @click="saveUserChanges" class="btn btn-primary" :disabled="saving">
                        <span v-if="saving">
                            <i class="fas fa-spinner fa-spin"></i> Сохранение...
                        </span>
                        <span v-else>
                            <i class="fas fa-save"></i> Сохранить изменения
                        </span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdminDashboard',
    data() {
        return {
            currentView: 'dashboard', // 'dashboard' или 'users'
            
            // Данные для дашборда
            stats: {
                total_users: 0,
                verified_users: 0,
                admin_users: 0,
                new_today: 0
            },
            recentUsers: [],
            currentAdmin: null,
            
            // Данные для управления пользователями
            users: [],
            loading: false,
            searchQuery: '',
            adminLevelFilter: '',
            currentPage: 1,
            perPage: 20,
            totalUsers: 0,
            totalPages: 0,
            
            // Модальные окна
            showDeleteModal: false,
            showEditModal: false,
            userToDelete: null,
            userToEdit: null,
            deleting: false,
            saving: false,
            
            searchTimeout: null
        }
    },
    
    computed: {
        // Для текущего администратора
        getCurrentAdminLevelText() {
            const levels = {
                0: 'Пользователь',
                1: 'Автор мануалов',
                2: 'Модератор постов',
                3: 'Модератор мануалов',
                4: 'Супер-модератор',
                5: 'Супервайзер'
            }
            return levels[this.currentAdmin?.admin_level] || 'Неизвестно'
        },
        
        getAdminBadgeClass() {
            const classes = {
                0: 'badge-user',
                1: 'badge-level-1',
                2: 'badge-level-2',
                3: 'badge-level-3',
                4: 'badge-level-4',
                5: 'badge-level-5'
            }
            return classes[this.currentAdmin?.admin_level] || 'badge-user'
        },
        
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
        },
        
        showEllipsis() {
            return this.totalPages > 5 && this.currentPage < this.totalPages - 2
        }
    },
    
    methods: {
        // Для других пользователей (в таблице)
        getUserAdminLevelText(level) {
            const levels = {
                0: 'Пользователь',
                1: 'Автор мануалов',
                2: 'Модератор постов',
                3: 'Модератор мануалов',
                4: 'Супер-модератор',
                5: 'Супервайзер'
            }
            return levels[level] || 'Неизвестно'
        },
        
        // Общие методы
        async checkAuthAndLoadData() {
            const user = JSON.parse(localStorage.getItem('user') || '{}')
            const token = localStorage.getItem('authToken')
            
            if (!token || !user.id) {
                this.$router.push('/login')
                return
            }

            if (user.admin_level === 0 && !user.is_super_admin) {
                alert('У вас нет прав для доступа к админ-панели')
                this.$router.push('/')
                return
            }

            try {
                await this.loadAdminData(token)
                this.currentAdmin = {
                    ...user,
                    ...this.currentAdmin
                }
            } catch (error) {
                console.error('Error loading admin data:', error)
                alert('Ошибка загрузки данных')
                this.$router.push('/login')
            } finally {
                this.loading = false
            }
        },
        
        async loadAdminData(token) {
            try {
                const statsResponse = await fetch('/api/admin/stats', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (!statsResponse.ok) {
                    throw new Error('Не удалось загрузить данные')
                }
                
                const responseData = await statsResponse.json()
                
                this.stats = responseData.stats
                this.currentAdmin = responseData.current_admin
                this.recentUsers = responseData.recent_users || []
                
            } catch (error) {
                console.error('Error loading admin data:', error)
                throw error
            }
        },
        
        refreshData() {
            if (this.currentView === 'dashboard') {
                this.checkAuthAndLoadData()
            } else {
                this.loadUsers()
            }
        },
        
        logout() {
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            this.$router.push('/login')
        },
        
        goToSite() {
            window.location.href = '/'
        },
        
        // Форматирование дат
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
        
        formatDateShort(dateString) {
            if (!dateString) return '-'
            try {
                const date = new Date(dateString)
                const now = new Date()
                const diff = now - date
                const days = Math.floor(diff / (1000 * 60 * 60 * 24))
                
                if (days === 0) {
                    return 'Сегодня'
                } else if (days === 1) {
                    return 'Вчера'
                } else if (days < 7) {
                    return `${days} дня назад`
                } else {
                    return date.toLocaleDateString('ru-RU', {
                        day: '2-digit',
                        month: '2-digit'
                    })
                }
            } catch (e) {
                return '-'
            }
        },
        
        // Методы для управления пользователями
        async loadUsers() {
            this.loading = true
            try {
                const token = localStorage.getItem('authToken')
                if (!token) {
                    this.$router.push('/login')
                    return
                }

                const params = new URLSearchParams({
                    page: this.currentPage,
                    per_page: this.perPage
                })

                if (this.searchQuery) {
                    params.append('search', this.searchQuery)
                }

                if (this.adminLevelFilter !== '') {
                    params.append('admin_level', this.adminLevelFilter)
                }

                const usersResponse = await fetch(`/api/admin/users?${params}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (!usersResponse.ok) {
                    throw new Error('Ошибка загрузки пользователей')
                }

                const data = await usersResponse.json()
                this.users = data.users
                this.totalUsers = data.total
                this.totalPages = data.pages
            } catch (error) {
                console.error('Error loading users: ', error)
                alert('Не удалось загрузить данные пользователей')
            } finally {
                this.loading = false
            }
        },
        
        debouncedSearch() {
            clearTimeout(this.searchTimeout)
            this.searchTimeout = setTimeout(() => {
                this.currentPage = 1
                this.loadUsers()
            }, 500)
        },
        
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page
                this.loadUsers()
                window.scrollTo(0, 0)
            }
        },
        
        // Методы для модальных окон
        confirmDelete(user) {
            if (this.currentAdmin?.id === user.id) {
                alert('Вы не можете удалить свой аккаунт')
                return
            }
            
            this.userToDelete = user
            this.showDeleteModal = true
        },
        
        closeDeleteModal() {
            this.showDeleteModal = false
            this.userToDelete = null
            this.deleting = false
        },

        async deleteUser() {
            if (!this.userToDelete) return

            this.deleting = true
            try {
                const token = localStorage.getItem('authToken')

                const response = await fetch(`/api/admin/users/${this.userToDelete.id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (!response.ok) {
                    const error = await response.json()
                    throw new Error(error.error || 'Ошибка удаления')
                }

                alert(`Пользователь ${this.userToDelete.username} удален`)

                this.loadUsers()
                this.closeDeleteModal()

            } catch (error) {
                console.error('Error deleting user: ', error)
                alert(error.message || 'Не удалось удалить пользователя')
            } finally {
                this.deleting = false
            }
        },

        editUser(user) {
            if (this.currentAdmin?.id === user.id) {
                alert('Вы не можете редактировать свой аккаунт')
                return
            }
            
            this.userToEdit = { ...user }
            this.showEditModal = true
        },

        closeEditModal() {
            this.showEditModal = false
            this.userToEdit = null
            this.saving = false
        },

        async saveUserChanges() {
            if (!this.userToEdit) return

            this.saving = true
            try {
                const token = localStorage.getItem('authToken')

                const response = await fetch(`/api/admin/users/${this.userToEdit.id}/admin-level`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        admin_level: parseInt(this.userToEdit.admin_level),
                        is_verified: this.userToEdit.is_verified,
                        is_super_admin: this.userToEdit.is_super_admin
                    })
                })

                if (!response.ok) {
                    const error = await response.json()
                    throw new Error(error.error || 'Ошибка сохранения')
                }

                alert('Изменения сохранены')

                this.loadUsers()
                this.closeEditModal()

            } catch (error) {
                console.error('Error saving user: ', error)
                alert(error.message || 'Не удалось сохранить изменения')
            } finally {
                this.saving = false
            }
        },

        viewUserDetails(user) {
            alert(`Ник: ${user.username}. E-mail: ${user.email}`)
        }
    },
    
    mounted() {
        this.checkAuthAndLoadData()
    },
    
    watch: {
        currentView(newView) {
            if (newView === 'users') {
                this.loadUsers()
            }
        }
    }
}
</script>

<style scoped>
/* Стили для дашборда */
.dashboard-content {
    padding: 20px;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
    margin-top: 30px;
}

.info-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.info-card-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
}

.info-card-header h3 {
    font-size: 18px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}

.info-card-body {
    padding: 25px;
}

.user-info-large {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
}

.user-avatar-large {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(255, 69, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    font-size: 32px;
}

.user-details-large h4 {
    font-size: 24px;
    color: var(--text);
    margin-bottom: 5px;
}

.user-details-large p {
    color: var(--text-secondary);
    margin-bottom: 15px;
}

.user-status {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.badge {
    padding: 5px;
    border-radius: 12px;
}

.badge-super {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.2));
    color: gold;
}

.badge-verified {
    background: rgba(50, 205, 50, 0.2);
    color: #32cd32;
}

.user-stats {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
}

.stat-item i {
    font-size: 20px;
    color: var(--primary);
}

.stat-item small {
    color: var(--text-secondary);
    font-size: 12px;
}

.stat-item p {
    color: var(--text);
    margin-top: 5px;
}

.users-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.user-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.user-item:hover {
    background: rgba(255, 255, 255, 0.05);
    transform: translateX(5px);
}

.user-item-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(74, 108, 247, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4a6cf7;
}

.user-item-info {
    flex: 1;
}

.user-item-info strong {
    color: var(--text);
    display: block;
    margin-bottom: 3px;
}

.user-item-info small {
    color: var(--text-secondary);
    font-size: 12px;
}

.user-item-date {
    color: var(--text-secondary);
    font-size: 12px;
    white-space: nowrap;
}

.empty-list {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-secondary);
}

.empty-list i {
    font-size: 48px;
    margin-bottom: 15px;
    opacity: 0.5;
}

.empty-list p {
    font-size: 16px;
}

.quick-actions {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
}

.quick-action {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 18px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: var(--text);
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
}

.quick-action:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary);
    transform: translateY(-2px);
}

.quick-action:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.quick-action i {
    font-size: 20px;
    color: var(--primary);
}

/* Общие стили админки (остаются без изменений) */
.admin-dashboard {
    min-height: 100vh;
    background: var(--bg-primary);
}

/* Навигация админки */
.admin-navbar {
    background: rgba(10, 10, 15, 0.98);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 15px 30px;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.admin-navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1600px;
    margin: 0 auto;
}

.admin-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 20px;
    font-weight: 700;
    color: var(--primary);
}

.admin-brand i {
    font-size: 24px;
}

.admin-user-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.admin-username {
    color: var(--text);
    font-weight: 500;
}

.admin-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-user {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
}

.badge-level-1 {
    background: rgba(74, 108, 247, 0.2);
    color: #4a6cf7;
}

.badge-level-2 {
    background: rgba(50, 205, 50, 0.2);
    color: #32cd32;
}

.badge-level-3 {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
}

.badge-level-4 {
    background: rgba(255, 69, 0, 0.2);
    color: #ff4500;
}

.badge-level-5 {
    background: linear-gradient(135deg, rgba(255, 69, 0, 0.2), rgba(255, 0, 0, 0.2));
    color: #ff0000;
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

/* Контейнер админки */
.admin-container {
    display: flex;
    min-height: calc(100vh - 70px);
    max-width: 1600px;
    margin: 0 auto;
}

/* Боковое меню */
.admin-sidebar {
    width: 250px;
    background: rgba(20, 20, 30, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding: 30px 0;
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 70px;
    height: calc(100vh - 70px);
}

.sidebar-header {
    padding: 0 25px 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
}

.sidebar-header h3 {
    font-size: 16px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}

.sidebar-header i {
    color: var(--primary);
}

.sidebar-menu {
    flex: 1;
    padding: 0 15px;
    overflow-y: auto;
}

.sidebar-section {
    margin-bottom: 30px;
}

.sidebar-section h4 {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
    padding: 0 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.sidebar-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 15px;
    color: var(--text-secondary);
    text-decoration: none;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
    position: relative;
    border: none;
    background: none;
    cursor: pointer;
    width: 100%;
    text-align: left;
}

.sidebar-item:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
}

.sidebar-item.active {
    background: rgba(255, 69, 0, 0.15);
    color: var(--primary);
    border-left: 3px solid var(--primary);
}

.sidebar-item i {
    font-size: 16px;
    width: 20px;
    text-align: center;
}

.sidebar-item span {
    flex: 1;
    font-size: 14px;
    font-weight: 500;
}

.sidebar-item .badge {
    background: rgba(255, 69, 0, 0.2);
    color: var(--primary);
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
}

.sidebar-item .badge-danger {
    background: rgba(255, 71, 87, 0.2);
    color: var(--danger);
}

.sidebar-footer {
    padding: 25px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: auto;
}

.system-status {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #32cd32;
    box-shadow: 0 0 10px #32cd32;
}

.status-indicator.active {
    background: #32cd32;
}

.status-indicator.inactive {
    background: var(--danger);
}

.system-status span {
    font-size: 12px;
    color: var(--text-secondary);
}

/* Основной контент */
.admin-main {
    flex: 1;
    padding: 30px;
    overflow-y: auto;
    background: rgba(10, 10, 15, 0.5);
}

/* Стили для страницы управления пользователями (из AdminUsers.vue) */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 20px;
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
    gap: 15px;
    align-items: center;
}

.search-box {
    position: relative;
    min-width: 300px;
}

.search-box i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
}

.search-box input {
    width: 100%;
    padding: 12px 15px 12px 45px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    color: var(--text);
    font-size: 14px;
}

.search-box input:focus {
    outline: none;
    border-color: var(--primary);
}

/* Статистика */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
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

.stat-info h3 {
    font-size: 32px;
    margin-bottom: 5px;
    color: var(--text);
}

.stat-info p {
    color: var(--text-secondary);
    font-size: 14px;
}

/* Фильтры */
.filters {
    display: flex;
    gap: 30px;
    margin-bottom: 25px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 200px;
}

.filter-group label {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 500;
}

.filter-group select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 10px 15px;
    color: var(--text);
    font-size: 14px;
}

.filter-group select:focus {
    outline: none;
    border-color: var(--primary);
}

/* Таблица */
.users-table-container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    overflow: hidden;
    position: relative;
    min-height: 400px;
}

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

.users-table {
    width: 100%;
    border-collapse: collapse;
}

.users-table th {
    background: rgba(255, 255, 255, 0.05);
    padding: 15px;
    text-align: left;
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.users-table td {
    padding: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.users-table tbody tr:hover {
    background: rgba(255, 255, 255, 0.03);
}

.user-id {
    color: var(--text-secondary);
    font-family: 'Consolas', monospace;
    font-size: 14px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 69, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
}

.user-details {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.user-details strong {
    color: var(--text);
}

.user-verified {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #32cd32;
    font-size: 12px;
}

.role-badge {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.admin-level {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.level-0 {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
}

.level-1 {
    background: rgba(74, 108, 247, 0.2);
    color: #4a6cf7;
}

.level-2 {
    background: rgba(50, 205, 50, 0.2);
    color: #32cd32;
}

.level-3 {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
}

.level-4 {
    background: rgba(255, 69, 0, 0.2);
    color: #ff4500;
}

.level-5 {
    background: linear-gradient(135deg, rgba(255, 69, 0, 0.2), rgba(255, 0, 0, 0.2));
    color: #ff0000;
}

.super-admin {
    color: gold;
    font-size: 14px;
}

.activity-stats {
    display: flex;
    gap: 15px;
}

.activity-item {
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--text-secondary);
    font-size: 12px;
}

.activity-item i {
    font-size: 14px;
}

.actions {
    display: flex;
    gap: 8px;
}

.btn-action {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.btn-action:hover:not(:disabled) {
    transform: translateY(-2px);
}

.btn-action:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-edit:hover:not(:disabled) {
    background: rgba(74, 108, 247, 0.2);
    color: #4a6cf7;
}

.btn-delete:hover:not(:disabled) {
    background: rgba(255, 71, 87, 0.2);
    color: var(--danger);
}

.btn-view:hover:not(:disabled) {
    background: rgba(50, 205, 50, 0.2);
    color: #32cd32;
}

/* Empty state */
.empty-state {
    padding: 60px 20px;
    text-align: center;
    color: var(--text-secondary);
}

.empty-state i {
    font-size: 60px;
    margin-bottom: 20px;
    opacity: 0.5;
}

.empty-state h3 {
    font-size: 24px;
    margin-bottom: 10px;
    color: var(--text);
}

/* Пагинация */
.pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.pagination-btn {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: transparent;
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
    border-radius: 8px;
    border: none;
    background: transparent;
    color: var(--text);
    cursor: pointer;
    transition: all 0.3s ease;
}

.page-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}

.page-btn.active {
    background: var(--primary);
    color: white;
}

.ellipsis {
    display: flex;
    align-items: center;
    padding: 0 10px;
    color: var(--text-secondary);
}

.pagination-info {
    margin-left: auto;
    color: var(--text-secondary);
    font-size: 14px;
}

.total-info {
    color: var(--text-secondary);
    font-size: 12px;
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
    border-radius: 8px;
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
}

.warning-text {
    color: var(--danger);
    background: rgba(255, 71, 87, 0.1);
    padding: 15px;
    border-radius: 10px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
}

.user-delete-info {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
}

.info-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.info-item span {
    color: var(--text-secondary);
}

.info-item strong {
    color: var(--text);
}

/* Форма редактирования */
.edit-form {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.form-group label {
    color: var(--text);
    font-weight: 500;
    font-size: 14px;
}

.form-group input,
.form-group select {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 14px;
}

.form-group input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.help-text {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 5px;
}

.help-text.warning {
    color: var(--danger);
    background: rgba(255, 71, 87, 0.1);
    padding: 10px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.checkbox-group {
    margin-top: 10px;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    color: var(--text);
    font-size: 14px;
}

.checkbox-label input[type="checkbox"] {
    display: none;
}

.checkbox-custom {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 5px;
    position: relative;
    transition: all 0.3s ease;
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom {
    background: var(--primary);
    border-color: var(--primary);
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom::after {
    content: '✓';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 12px;
}

.btn-danger {
    background: var(--danger);
    color: white;
    border: 1px solid var(--danger);
}

.btn-danger:hover:not(:disabled) {
    background: #ff2e43;
    box-shadow: 0 0 20px rgba(255, 71, 87, 0.3);
}

.btn-danger:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@media (max-width: 1200px) {
    .admin-container {
        flex-direction: column;
    }
    
    .admin-sidebar {
        width: 100%;
        height: auto;
        position: static;
        padding: 20px;
    }
    
    .sidebar-menu {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .sidebar-section {
        flex: 1;
        min-width: 200px;
    }
    
    .admin-main {
        padding: 20px;
    }
    
    .form-row {
        grid-template-columns: 1fr;
    }
    
    .info-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .admin-navbar-content {
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }
    
    .admin-user-info {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .sidebar-menu {
        flex-direction: column;
    }
    
    .page-header {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .header-actions {
        width: 100%;
        flex-direction: column;
    }
    
    .search-box {
        min-width: 100%;
    }
    
    .filters {
        flex-direction: column;
        gap: 15px;
    }
    
    .users-table {
        display: block;
        overflow-x: auto;
    }
    
    .pagination {
        flex-direction: column;
        gap: 15px;
    }
    
    .pagination-info {
        margin-left: 0;
    }
    
    .user-info-large {
        flex-direction: column;
        text-align: center;
    }
    
    .user-status {
        justify-content: center;
    }
}
</style>