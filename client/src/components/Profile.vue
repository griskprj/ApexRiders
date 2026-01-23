<template>
    <div class="profile-page">
        <!-- Декоративные элементы -->
        <div class="decoration decoration-1"></div>
        <div class="decoration decoration-2"></div>
        
        <div class="profile-container">
            <!-- Заголовок -->
            <div class="profile-header">
                <h1><i class="fas fa-user"></i> Мой профиль</h1>
                <p>Управление вашей учетной записью</p>
            </div>

            <div v-if="isLoading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>Загрузка профиля...</p>
            </div>
            
            <!-- Основной контент -->
            <div class="profile-content">
                <!-- Левая колонка - Информация о пользователе -->
                <div class="profile-sidebar">
                    <!-- Карточка профиля -->
                    <div class="profile-card">
                        <div class="profile-avatar">
                            <div class="avatar-circle">
                                <i class="fas fa-motorcycle"></i>
                            </div>
                            <div class="profile-badge" v-if="user.role === 'admin'">
                                <i class="fas fa-crown"></i>
                                Администратор
                            </div>
                            <div class="profile-badge" v-else-if="user.role === 'moderator'">
                                <i class="fas fa-shield-alt"></i>
                                Модератор
                            </div>
                            <div class="profile-badge" v-else>
                                <i class="fas fa-user"></i>
                                Участник
                            </div>
                        </div>
                        
                        <div class="profile-info">
                            <h2>{{ user.username }}</h2>
                            <div class="profile-meta">
                                <div class="meta-item">
                                    <i class="fas fa-envelope"></i>
                                    <span>{{ user.email }}</span>
                                </div>
                                <div class="meta-item">
                                    <i class="fas fa-calendar-alt"></i>
                                    <span>Участник с {{ formatDate(user.join_at) }}</span>
                                </div>
                                <div class="meta-item">
                                    <i class="fas fa-badge-check"></i>
                                    <span v-if="user.is_verified" class="verified">✓ Подтвержден</span>
                                    <span v-else class="not-verified">Не подтвержден</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Статистика профиля -->
                    <div class="stats-card">
                        <h3><i class="fas fa-chart-line"></i> Статистика</h3>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value">{{ stats.manuals_count || 0 }}</div>
                                <div class="stat-label">Завершено мануалов</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{{ stats.lessons_count || 0 }}</div>
                                <div class="stat-label">Пройдено уроков</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{{ stats.posts_count || 0 }}</div>
                                <div class="stat-label">Создано постов</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{{ stats.product_active_count || 0 }}</div>
                                <div class="stat-label">Активных объявлений</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Правая колонка - Настройки и действия -->
                <div class="profile-main">
                    <!-- Мои мотоциклы -->
                    <div class="section-card">
                        <div class="section-header">
                            <h3><i class="fas fa-motorcycle"></i> Мои мотоциклы</h3>
                            <button class="btn btn-outline btn-sm" @click="showAddMotorcycleModal = true">
                                <i class="fas fa-plus"></i> Добавить
                            </button>
                        </div>
                        
                        <div v-if="motorcycles.length === 0" class="empty-state">
                            <i class="fas fa-motorcycle"></i>
                            <p>У вас пока нет добавленных мотоциклов</p>
                            <button class="btn btn-primary" @click="showAddMotorcycleModal = true">
                                Добавить первый мотоцикл
                            </button>
                        </div>
                        
                        <div v-else class="motorcycles-list">
                            <div v-for="moto in motorcycles" :key="moto.id" class="motorcycle-item">
                                <div class="moto-info">
                                    <div class="moto-brand">{{ moto.brand }}</div>
                                    <div class="moto-model">{{ moto.model }}</div>
                                    <div class="moto-details">
                                        <span class="moto-year">{{ moto.year }} год</span>
                                        <span class="moto-engine">{{ moto.engine_volume }}cc</span>
                                        <span class="moto-color">{{ moto.color }}</span>
                                    </div>
                                    <div class="moto-plate">{{ moto.license_plate }}</div>
                                </div>
                                <div class="moto-actions">
                                    <button class="btn-icon" @click="editMotorcycle(moto)">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="btn-icon btn-danger" @click="deleteMotorcycle(moto.id)">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                    <button class="btn btn-primary" @click="goToGarage(moto.id)">
                                        <i class="fas fa-search"></i> Гараж
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Настройки аккаунта -->
                    <div class="section-card">
                        <div class="section-header">
                            <h3><i class="fas fa-cog"></i> Настройки аккаунта</h3>
                        </div>
                        
                        <form @submit.prevent="updateProfile" class="settings-form">
                            <div class="form-group">
                                <label for="username">Имя пользователя</label>
                                <input
                                    type="text"
                                    id="username"
                                    v-model="editForm.username"
                                    required
                                >
                            </div>
                            
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    v-model="editForm.email"
                                    required
                                >
                            </div>
                            
                            <div class="form-actions">
                                <button type="submit" class="btn btn-primary" :disabled="isUpdating">
                                    <span v-if="isUpdating">
                                        <i class="fas fa-spinner fa-spin"></i> Сохранение...
                                    </span>
                                    <span v-else>Сохранить изменения</span>
                                </button>
                            </div>
                        </form>
                    </div>
                    
                    <!-- Смена пароля -->
                    <div class="section-card">
                        <div class="section-header">
                            <h3><i class="fas fa-key"></i> Смена пароля</h3>
                        </div>
                        
                        <form @submit.prevent="changePassword" class="settings-form">
                            <div class="form-group">
                                <label for="currentPassword">Текущий пароль</label>
                                <input
                                    type="password"
                                    id="currentPassword"
                                    v-model="passwordForm.currentPassword"
                                    required
                                >
                            </div>
                            
                            <div class="form-group">
                                <label for="newPassword">Новый пароль</label>
                                <input
                                    type="password"
                                    id="newPassword"
                                    v-model="passwordForm.newPassword"
                                    required
                                    minlength="6"
                                >
                            </div>
                            
                            <div class="form-group">
                                <label for="confirmPassword">Подтверждение пароля</label>
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    v-model="passwordForm.confirmPassword"
                                    required
                                >
                            </div>
                            
                            <div class="form-actions">
                                <button type="submit" class="btn btn-primary" :disabled="isChangingPassword">
                                    <span v-if="isChangingPassword">
                                        <i class="fas fa-spinner fa-spin"></i> Обновление...
                                    </span>
                                    <span v-else>Сменить пароль</span>
                                </button>
                            </div>
                        </form>
                    </div>
                    <div class="section-card danger-zone">
                        <div class="section-header">
                            <h3><i class="fas fa-exclamation-triangle"></i> Опасная зона</h3>
                        </div>
                        
                        <div class="danger-actions">
                            <p class="warning-text">
                                <i class="fas fa-exclamation-circle"></i>
                                Удаление аккаунта необратимо. Все ваши данные будут удалены.
                            </p>
                            
                            <button 
                                class="btn btn-danger" 
                                @click="showDeleteAccountModal = true"
                                :disabled="isDeletingAccount"
                            >
                                <i class="fas fa-trash-alt"></i>
                                <span v-if="isDeletingAccount">Удаление...</span>
                                <span v-else>Удалить аккаунт</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Модальное окно добавления/редактирования мотоцикла -->
        <div v-if="showAddMotorcycleModal" class="modal-overlay" @click.self="showAddMotorcycleModal = false">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>{{ editingMotorcycle ? 'Редактировать мотоцикл' : 'Добавить мотоцикл' }}</h3>
                    <button class="modal-close" @click="closeMotorcycleModal">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <form @submit.prevent="saveMotorcycle" class="modal-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="brand">Марка *</label>
                            <input
                                type="text"
                                id="brand"
                                v-model="motorcycleForm.brand"
                                required
                            >
                        </div>
                        
                        <div class="form-group">
                            <label for="model">Модель *</label>
                            <input
                                type="text"
                                id="model"
                                v-model="motorcycleForm.model"
                                required
                            >
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="year">Год выпуска</label>
                            <input
                                type="number"
                                id="year"
                                v-model="motorcycleForm.year"
                                min="1900"
                                :max="new Date().getFullYear()"
                            >
                        </div>
                        
                        <div class="form-group">
                            <label for="engineVolume">Объем двигателя (cc)</label>
                            <input
                                type="number"
                                id="engineVolume"
                                v-model="motorcycleForm.engine_volume"
                                min="50"
                                max="3000"
                            >
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="color">Цвет</label>
                            <input
                                type="text"
                                id="color"
                                v-model="motorcycleForm.color"
                            >
                        </div>
                        
                        <div class="form-group">
                            <label for="licensePlate">Госномер</label>
                            <input
                                type="text"
                                id="licensePlate"
                                v-model="motorcycleForm.license_plate"
                            >
                        </div>

                        <div class="form-group">
                            <label for="licensePlate">VIN-номер</label>
                            <input
                                type="text"
                                id="vin"
                                v-model="motorcycleForm.vin"
                            >
                        </div>

                        <div class="form-group">
                            <label for="licensePlate">Страховака до</label>
                            <input
                                type="date"
                                id="insurance_expiry"
                                v-model="motorcycleForm.insurance_expiry"
                            >
                        </div>
                    </div>
                    
                    <div class="modal-actions">
                        <button type="button" class="btn btn-outline" @click="closeMotorcycleModal">
                            Отмена
                        </button>
                        <button type="submit" class="btn btn-primary" :disabled="isSavingMotorcycle">
                            <span v-if="isSavingMotorcycle">
                                <i class="fas fa-spinner fa-spin"></i> Сохранение...
                            </span>
                            <span v-else>{{ editingMotorcycle ? 'Сохранить' : 'Добавить' }}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
        <div v-if="showDeleteAccountModal" class="modal-overlay" @click.self="showDeleteAccountModal = false">
            <div class="modal-content delete-account-modal">
                <div class="modal-header">
                    <h3><i class="fas fa-exclamation-triangle"></i> Удаление аккаунта</h3>
                    <button class="modal-close" @click="showDeleteAccountModal = false">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <div class="modal-body">
                    <div class="warning-icon">
                        <i class="fas fa-exclamation-circle"></i>
                    </div>
                    
                    <h4>Вы уверены, что хотите удалить свой аккаунт?</h4>
                    
                    <div class="warning-list">
                        <p><i class="fas fa-times-circle"></i> Все ваши посты будут удалены</p>
                        <p><i class="fas fa-times-circle"></i> Все ваши мотоциклы будут удалены</p>
                        <p><i class="fas fa-times-circle"></i> Все ваши комментарии и лайки будут удалены</p>
                        <p><i class="fas fa-times-circle"></i> Ваша статистика будет сброшена</p>
                        <p><i class="fas fa-times-circle"></i> Это действие нельзя отменить</p>
                    </div>
                    
                    <div class="confirmation-input">
                        <label for="confirmText">
                            Для подтверждения введите: <strong>УДАЛИТЬ АККАУНТ</strong>
                        </label>
                        <input
                            type="text"
                            id="confirmText"
                            v-model="deleteConfirmationText"
                            placeholder="УДАЛИТЬ АККАУНТ"
                        >
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button 
                        type="button" 
                        class="btn btn-outline" 
                        @click="showDeleteAccountModal = false"
                        :disabled="isDeletingAccount"
                    >
                        Отмена
                    </button>
                    <button 
                        type="button" 
                        class="btn btn-danger" 
                        @click="deleteAccount"
                        :disabled="isDeletingAccount || deleteConfirmationText !== 'УДАЛИТЬ АККАУНТ'"
                    >
                        <span v-if="isDeletingAccount">
                            <i class="fas fa-spinner fa-spin"></i> Удаление...
                        </span>
                        <span v-else>
                            <i class="fas fa-trash-alt"></i> Да, удалить аккаунт
                        </span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
import { authService } from '../utils/checkAuth'
import { useRouter } from 'vue-router'

const router = useRouter()

const user = ref({})
const motorcycles = ref([])
const stats = ref({})
const isLoading = ref(true)

const showAddMotorcycleModal = ref(false)
const editingMotorcycle = ref(null)
const isSavingMotorcycle = ref(false)
const isUpdating = ref(false)
const isChangingPassword = ref(false)

const showDeleteAccountModal = ref(false)
const isDeletingAccount = ref(false)
const deleteConfirmationText = ref('')

const motorcycleForm = reactive({
    brand: '',
    model: '',
    engine_volume: null,
    color: '',
    license_plate: '',
    vin: '',
    insurance_expiry: ''
})

const editForm = reactive({
    username: '',
    email: ''
})

const passwordForm = reactive({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
})

const formatDate = (dateString) => {
    if (!dateString) return 'неизвестно'
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    })
}

const fetchProfileData = async () => {
    try {
        const token = authService.getToken()
        
        if (!token) {
            throw new Error('No authentication token found')
        }

        const profileResponse = await axios.get('/api/auth/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        })

        user.value = profileResponse.data

        const motorcycleResponse = await axios.get('/api/motorcycle', {
            headers: { 'Authorization': `Bearer ${token}` }
        })

        motorcycles.value = motorcycleResponse.data?.motorcycles || motorcycleResponse.data || []

        const statsResponse = await axios.get('/api/statistic/dashboard', {
            headers: { 'Authorization': `Bearer ${token}` }
        })

        stats.value = statsResponse.data || {}

        editForm.username = user.value.username
        editForm.email = user.value.email
    } catch (error) {
        console.error('Ошибка при загрузке профиля: ', error)

        if (error.response?.status === 401) {
            authService.clearAuth()
        }
    } finally {
        isLoading.value = false
    }
}

const updateProfile = async () => {
    try {
        isUpdating.value = true

        const  token = authService.getToken()
        const response = await axios.put('/api/auth/profile', editForm, {
            headers: { 'Authorization': `Bearer ${token}`}
        })

        user.value = response.data
        alert('Профиль успешно обновлен!')
    } catch (error) {
        console.error('Ошибка при обновлении профиля: ', error)
        alert(error.response?.data?.error || 'Ошибка при обновлении профиля')
    } finally {
        isUpdating.value = false
    }
}

const changePassword = async () => {
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
        alert('Новый пароль и подтверждение не совпадают')
        return
    }

    if (passwordForm.newPassword.length < 6) {
        alert('Пароль должен содержать минимум 6 символов')
        return
    }

    try {
        isChangingPassword.value = true

        const token = authService.getToken()
        await axios.post('/api/auth/change-password', {
            current_password: passwordForm.currentPassword,
            new_password: passwordForm.newPassword
        }, {
            headers: { 'Authorization': `Bearer ${token}` }
        })

        alert('Пароль успешно изменен')
        passwordForm.currentPassword = ''
        passwordForm.newPassword = ''
        passwordForm.confirmPassword = ''
    } catch (error) {
        console.error('Ошибка при смене пароля: ', error)
        alert(error.response?.data?.error || 'Ошибка при смене пароля')
    } finally {
        isChangingPassword.value = false
    }
}

const deleteAccount = async () => {
    if (deleteConfirmationText.value !== 'УДАЛИТЬ АККАУНТ') {
        alert('Пожалуйста, правильно введите текст подтверждения')
        return
    }
    
    if (!confirm('Вы уверены? Это действие нельзя отменить!')) {
        return
    }
    
    try {
        isDeletingAccount.value = true
        
        const token = authService.getToken()
        await axios.delete('/api/auth/delete-account', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        
        authService.clearAuth()
        
        alert('Ваш аккаунт был успешно удален. Вы будете перенаправлены на главную страницу.')
        
        router.push('/')
        
    } catch (error) {
        console.error('Ошибка при удалении аккаунта:', error)
        alert(error.response?.data?.error || 'Ошибка при удалении аккаунта')
        isDeletingAccount.value = false
    }
}

const closeDeleteModal = () => {
    showDeleteAccountModal.value = false
    deleteConfirmationText.value = ''
}

const editMotorcycle = (moto) => {
    editingMotorcycle.value = moto
    Object.assign(motorcycleForm, moto)
    showAddMotorcycleModal.value = true
}

const saveMotorcycle = async () => {
    try {
        isSavingMotorcycle.value = true

        const token = authService.getToken()
        let response

        if (editingMotorcycle.value) {
            response = await axios.put(`/api/motorcycle/${editingMotorcycle.value.id}`, motorcycleForm,{
                headers: { 'Authorization': `Bearer ${token}` }
            })

            const index = motorcycles.value.findIndex(m => m.id === editingMotorcycle.value.id)
            if (index !== -1) {
                motorcycles.value[index] = response.data
            }
        } else {
            response = await axios.post('/api/motorcycle', motorcycleForm, {
                headers: { 'Authorization': `Bearer ${token}` }
            })

            const newMotorcycle = response.data?.motorcycle || response.data
            if (newMotorcycle) {
                motorcycles.value.push(newMotorcycle)
            }
        }

        closeMotorcycleModal()
        alert('Мотоцикл успешно сохранен!')
    } catch (error) {
        console.error('Ошибка при сохранении мотоцикла: ', error)
        alert(error.response?.data?.error || 'Ошибка при сохранении мотоцикла')
    } finally {
        isSavingMotorcycle.value = false
    }
}

const deleteMotorcycle = async (id) => {
    if (!confirm('Вы уверены, что хотите удалить этот мотоцикл?')) {
        return
    }

    try {
        const token = authService.getToken()
        await axios.delete(`/api/motorcycle/${id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })

        motorcycles.value = motorcycles.value.filter(m => m.id !== id)
        alert('Мотоцикл успешно удален!')
    } catch (error) {
        console.error('Ошибка при удалении мотоцикла:', error)
        alert(error.response?.data?.error || 'Ошибка при удалении мотоцикла')
    }
}

const closeMotorcycleModal = () => {
    showAddMotorcycleModal.value = false
    editingMotorcycle.value = null
    Object.keys(motorcycleForm).forEach(key => {
        if (typeof motorcycleForm[key] === 'number') {
            motorcycleForm[key] = null
        } else {
            motorcycleForm[key] = ''
        }
    })
}

const goToGarage = (id) => {
    router.push(`/garage/${id}`)
}

onMounted(() => {
    fetchProfileData()
})
</script>

<style scoped>
/* Основные стили страницы профиля */
.profile-page {
    min-height: 100vh;
    padding: 120px 5% 60px;
    position: relative;
}

.profile-container {
    max-width: 1200px;
    margin: 0 auto;
}

.profile-header {
    margin-bottom: 40px;
    text-align: center;
}

.profile-header h1 {
    font-size: 2.5rem;
    color: var(--text);
    margin-bottom: 10px;
}

.profile-header p {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

.profile-content {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 30px;
}

/* Сайдбар профиля */
.profile-sidebar {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.profile-card {
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
}

.profile-avatar {
    position: relative;
    margin-bottom: 20px;
}

.avatar-circle {
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 15px;
    font-size: 50px;
    color: white;
}

.profile-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50px;
    font-size: 0.9rem;
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.profile-badge i {
    color: var(--primary);
}

.profile-info h2 {
    font-size: 1.8rem;
    margin-bottom: 15px;
    color: var(--text);
}

.profile-meta {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.meta-item i {
    color: var(--primary);
    width: 20px;
}

.verified {
    color: #4CAF50;
    font-weight: 500;
}

.not-verified {
    color: #ff9800;
    font-weight: 500;
}

/* Карточка статистики */
.stats-card {
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 25px;
}

.stats-card h3 {
    font-size: 1.3rem;
    margin-bottom: 20px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.stat-item {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* Основной контент профиля */
.profile-main {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.section-card {
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 25px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-header h3 {
    font-size: 1.3rem;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}

.btn-sm {
    padding: 8px 16px;
    font-size: 0.9rem;
}

/* Список мотоциклов */
.empty-state {
    text-align: center;
    padding: 40px 20px;
}

.empty-state i {
    font-size: 60px;
    color: var(--primary);
    margin-bottom: 20px;
    opacity: 0.7;
}

.empty-state p {
    color: var(--text-secondary);
    margin-bottom: 20px;
}

.motorcycles-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.motorcycle-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

.motorcycle-item:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
}

.moto-info {
    flex: 1;
}

.moto-brand {
    font-weight: 700;
    color: var(--text);
    font-size: 1.1rem;
}

.moto-model {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-bottom: 5px;
}

.moto-details {
    display: flex;
    gap: 15px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.moto-plate {
    background: var(--primary-light);
    color: var(--primary);
    padding: 4px 12px;
    border-radius: 6px;
    font-family: monospace;
    font-weight: 600;
    margin-top: 5px;
    display: inline-block;
}

.moto-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.btn-icon {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    color: var(--text);
}

.btn-icon:hover {
    background: var(--primary-light);
    border-color: var(--primary);
    color: var(--primary);
}

.btn-danger:hover {
    background: rgba(255, 69, 0, 0.2);
    border-color: #ff4500;
    color: #ff4500;
}

/* Формы */
.settings-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    color: var(--text);
    font-weight: 500;
    font-size: 0.95rem;
}

.form-group input {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

.form-actions {
    padding-top: 10px;
}

/* Модальное окно */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.modal-content {
    background: var(--dark-light);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 25px 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    font-size: 1.4rem;
    color: var(--text);
}

.modal-close {
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.5rem;
    cursor: pointer;
    padding: 5px;
    transition: all 0.3s ease;
}

.modal-close:hover {
    color: var(--text);
}

.modal-form {
    padding: 25px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.danger-zone {
    border-color: #ff4444;
    background: rgba(255, 68, 68, 0.05);
}

.danger-zone .section-header h3 {
    color: #ff4444;
}

.danger-actions {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.warning-text {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #ff9800;
    background: rgba(255, 152, 0, 0.1);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255, 152, 0, 0.3);
}

.warning-text i {
    color: #ff9800;
}

.btn-danger {
    background: #ff4444;
    border-color: #ff4444;
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background: #ff0000;
    border-color: #ff0000;
}

.btn-danger:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Стили для модального окна удаления аккаунта */
.delete-account-modal {
    max-width: 500px;
}

.modal-body {
    padding: 25px;
}

.delete-account-modal .modal-actions {
    justify-content: center;
    padding: 20px;
}

.warning-icon {
    text-align: center;
    margin-bottom: 20px;
}

.warning-icon i {
    font-size: 60px;
    color: #ff4444;
}

.modal-body h4 {
    text-align: center;
    color: var(--text);
    margin-bottom: 25px;
    font-size: 1.3rem;
}

.warning-list {
    background: rgba(255, 68, 68, 0.05);
    border: 1px solid rgba(255, 68, 68, 0.2);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 25px;
}

.warning-list p {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    color: var(--text);
}

.warning-list p:last-child {
    margin-bottom: 0;
}

.warning-list i {
    color: #ff4444;
    min-width: 20px;
}

.confirmation-input {
    margin-top: 20px;
}

.confirmation-input label {
    display: block;
    margin-bottom: 10px;
    color: var(--text);
    font-size: 0.95rem;
}

.confirmation-input input {
    width: 100%;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 68, 68, 0.3);
    border-radius: 8px;
    padding: 12px 15px;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.confirmation-input input:focus {
    outline: none;
    border-color: #ff4444;
    box-shadow: 0 0 0 2px rgba(255, 68, 68, 0.2);
}

.confirmation-input strong {
    color: #ff4444;
}

/* Адаптивность */
@media (max-width: 480px) {
    .delete-account-modal {
        margin: 10px;
    }
    
    .modal-body {
        padding: 15px;
    }
    
    .warning-icon i {
        font-size: 50px;
    }
    
    .modal-body h4 {
        font-size: 1.1rem;
    }
}

/* Загрузка */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    background: var(--dark-light);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.loading-spinner {
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

/* Декоративные элементы */
.decoration {
    position: fixed;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.1;
    z-index: -1;
}

.decoration-1 {
    background: var(--primary);
    top: 10%;
    left: 5%;
}

.decoration-2 {
    background: var(--accent);
    bottom: 10%;
    right: 5%;
}

/* Адаптивность */
@media (max-width: 992px) {
    .profile-content {
        grid-template-columns: 1fr;
    }
    
    .profile-sidebar {
        order: 2;
    }
}

@media (max-width: 768px) {
    .profile-page {
        padding: 100px 5% 40px;
    }
    
    .profile-header h1 {
        font-size: 2rem;
    }
    
    .form-row {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .motorcycle-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .moto-actions {
        align-self: flex-end;
    }
}

@media (max-width: 480px) {
    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .section-header h3 {
        font-size: 1.1rem;
    }
    
    .modal-content {
        margin: 10px;
        padding: 15px;
    }
    
    .modal-form {
        padding: 15px;
    }
}
</style>