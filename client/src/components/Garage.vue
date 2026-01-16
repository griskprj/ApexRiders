<template>
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>
    
    <section class="garage-page">
        <GarageHeader :motorcycle="selectedMotorcycle" @update-mileage="showMileageModal = true" />
        
        <div class="garage-layout">
            <!-- Основная информация о мотоцикле -->
            <MotorcycleCard 
                :motorcycle="selectedMotorcycle"
                @edit="showEditModal = true"
                @delete="confirmDelete"
            />
            
            <!-- Статистика и быстрые действия -->
            <div class="quick-stats-section">
                <MaintenanceStats :stats="maintenanceStats" />
                <QuickActions 
                    @add-maintenance="showMaintenanceModal = true"
                    @add-note="showNoteModal = true"
                />
            </div>
            
            <!-- Планировщик ТО -->
            <MaintenancePlanner 
                :tasks="maintenanceTasks"
                :upcoming-tasks="upcomingMaintenance"
                @task-click="handleTaskClick"
                @add-task="showMaintenanceModal = true"
                @complete-task="completeTask"
            />
            
            <!-- Заметки -->
            <NotesSection 
                :notes="notes"
                :recent-notes="recentNotes"
                @note-click="handleNoteClick"
                @add-note="showNoteModal = true"
                @edit-note="editNote"
            />
        </div>
        
        <!-- Модальные окна -->
        <MileageModal 
            v-if="showMileageModal"
            :current-mileage="selectedMotorcycle.current_mileage"
            @save="updateMileage"
            @close="showMileageModal = false"
        />
        
        <MaintenanceModal 
            v-if="showMaintenanceModal"
            :motorcycle-id="selectedMotorcycle.id"
            :task="editingTask"
            @save="saveMaintenanceTask"
            @close="closeMaintenanceModal"
        />
        
        <NoteModal 
            v-if="showNoteModal"
            :motorcycle-id="selectedMotorcycle.id"
            :note="editingNote"
            @save="saveNote"
            @close="closeNoteModal"
        />
        
        <MotorcycleModal 
            v-if="showEditModal"
            :motorcycle="selectedMotorcycle"
            mode="edit"
            @save="updateMotorcycle"
            @close="showEditModal = false"
        />
        
        <!-- Загрузка -->
        <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
        </div>
    </section>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { authService } from '../utils/checkAuth'

// Компоненты
import GarageHeader from './garage/GarageHeader.vue'
import MotorcycleCard from './garage/MotorcycleCard.vue'
import MaintenanceStats from './garage/MaintenanceStats.vue'
import QuickActions from './garage/QuickActions.vue'
import MaintenancePlanner from './garage/MaintenancePlanner.vue'
import NotesSection from './garage/NotesSection.vue'
import MileageModal from './garage/MileageModal.vue'
import MaintenanceModal from './garage/MaintenanceModal.vue'
import NoteModal from './garage/NoteModal.vue'
import MotorcycleModal from './garage/MotorcycleModal.vue'

export default {
    name: 'GaragePage',
    
    components: {
        GarageHeader,
        MotorcycleCard,
        MaintenanceStats,
        QuickActions,
        MaintenancePlanner,
        NotesSection,
        MileageModal,
        MaintenanceModal,
        NoteModal,
        MotorcycleModal
    },
    
    setup() {
        const route = useRoute()
        const router = useRouter()
        
        const isLoading = ref(true)
        const selectedMotorcycle = ref({
            id: null,
            brand: '',
            model: '',
            year: '',
            engine_volume: '',
            color: '',
            license_plate: '',
            current_mileage: 0,
            image_url: null,
            vin: '',
            insurance_expiry: null,
            registration_expiry: null,
            created_at: null
        })
        
        const maintenanceTasks = ref([])
        const upcomingMaintenance = ref([])
        const notes = ref([])
        const recentNotes = ref([])
        const maintenanceStats = ref({
            total_tasks: 0,
            completed: 0,
            pending: 0,
            overdue: 0,
            completion_rate: 0
        })
        
        // Модальные окна
        const showMileageModal = ref(false)
        const showMaintenanceModal = ref(false)
        const showNoteModal = ref(false)
        const showEditModal = ref(false)
        
        // Редактируемые элементы
        const editingTask = ref(null)
        const editingNote = ref(null)
        
        // Получить данные мотоцикла
        const fetchMotorcycleData = async () => {
            try {
                const token = authService.getToken()
                if (!token) {
                    throw new Error('No authentication token')
                }
                
                const motoId = route.params.id
                const response = await axios.get(`/api/garage/motorcycle/${motoId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                const data = response.data
                selectedMotorcycle.value = data.motorcycle
                maintenanceTasks.value = data.maintenance_tasks || []
                notes.value = data.notes || []
                recentNotes.value = data.recent_notes || []
                upcomingMaintenance.value = data.upcoming_maintenance || []
                maintenanceStats.value = data.stats || {}
                
            } catch (error) {
                console.error('Ошибка загрузки данных мотоцикла:', error)
                if (error.response?.status === 404) {
                    router.push('/garage')
                }
            } finally {
                isLoading.value = false
            }
        }
        
        // Обновить пробег
        const updateMileage = async (newMileage) => {
            try {
                const token = authService.getToken()
                const response = await axios.put(
                    `/api/garage/motorcycle/${selectedMotorcycle.value.id}/mileage`,
                    { mileage: newMileage },
                    { headers: { 'Authorization': `Bearer ${token}` } }
                )
                
                selectedMotorcycle.value.current_mileage = newMileage
                showMileageModal.value = false
                
                // Обновляем список задач
                await fetchMotorcycleData()
                
            } catch (error) {
                console.error('Ошибка обновления пробега:', error)
            }
        }
        
        // Сохранить задачу ТО
        const saveMaintenanceTask = async (taskData) => {
            try {
                const token = authService.getToken()
                const url = editingTask.value 
                    ? `/api/garage/maintenance/${editingTask.value.id}`
                    : '/api/garage/maintenance'
                
                const method = editingTask.value ? 'PUT' : 'POST'
                
                const response = await axios({
                    method,
                    url,
                    data: taskData,
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                
                closeMaintenanceModal()
                await fetchMotorcycleData()
                
            } catch (error) {
                console.error('Ошибка сохранения задачи:', error)
            }
        }
        
        // Сохранить заметку
        const saveNote = async (noteData) => {
            try {
                const token = authService.getToken()
                const url = editingNote.value 
                    ? `/api/garage/notes/${editingNote.value.id}`
                    : '/api/garage/notes'
                
                const method = editingNote.value ? 'PUT' : 'POST'
                
                const response = await axios({
                    method,
                    url,
                    data: noteData,
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                
                closeNoteModal()
                await fetchMotorcycleData()
                
            } catch (error) {
                console.error('Ошибка сохранения заметки:', error)
            }
        }
        
        // Обновить мотоцикл
        const updateMotorcycle = async (motorcycleData) => {
            try {
                const token = authService.getToken()
                const response = await axios.put(
                    `/api/motorcycle/${selectedMotorcycle.value.id}`,
                    motorcycleData,
                    { headers: { 'Authorization': `Bearer ${token}` } }
                )
                
                selectedMotorcycle.value = { ...selectedMotorcycle.value, ...motorcycleData }
                showEditModal.value = false
                
            } catch (error) {
                console.error('Ошибка обновления мотоцикла:', error)
            }
        }
        
        // Завершить задачу ТО
        const completeTask = async (taskId) => {
            try {
                const token = authService.getToken()
                const response = await axios.put(
                    `/api/garage/maintenance/${taskId}`,
                    { status: 'completed' },
                    { headers: { 'Authorization': `Bearer ${token}` } }
                )
                
                await fetchMotorcycleData()
                
            } catch (error) {
                console.error('Ошибка завершения задачи:', error)
            }
        }
        
        // Обработчики кликов
        const handleTaskClick = (task) => {
            editingTask.value = task
            showMaintenanceModal.value = true
        }
        
        const handleNoteClick = (note) => {
            editingNote.value = note
            showNoteModal.value = true
        }
        
        const editNote = (note) => {
            editingNote.value = note
            showNoteModal.value = true
        }
        
        // Закрыть модалки
        const closeMaintenanceModal = () => {
            editingTask.value = null
            showMaintenanceModal.value = false
        }
        
        const closeNoteModal = () => {
            editingNote.value = null
            showNoteModal.value = false
        }
        
        // Подтверждение удаления
        const confirmDelete = () => {
            if (confirm('Вы уверены, что хотите удалить этот мотоцикл?')) {
                deleteMotorcycle()
            }
        }
        
        // Удалить мотоцикл
        const deleteMotorcycle = async () => {
            try {
                const token = authService.getToken()
                await axios.delete(`/api/motorcycle/${selectedMotorcycle.value.id}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                
                router.push('/garage')
                
            } catch (error) {
                console.error('Ошибка удаления мотоцикла:', error)
            }
        }
        
        onMounted(() => {
            fetchMotorcycleData()
        })
        
        return {
            isLoading,
            selectedMotorcycle,
            maintenanceTasks,
            upcomingMaintenance,
            notes,
            recentNotes,
            maintenanceStats,
            showMileageModal,
            showMaintenanceModal,
            showNoteModal,
            showEditModal,
            editingTask,
            editingNote,
            updateMileage,
            saveMaintenanceTask,
            saveNote,
            updateMotorcycle,
            completeTask,
            handleTaskClick,
            handleNoteClick,
            editNote,
            closeMaintenanceModal,
            closeNoteModal,
            confirmDelete
        }
    }
}
</script>

<style scoped>
.garage-page {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

.garage-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 25px;
    margin-top: 30px;
}

.quick-stats-section {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

/* Декоративные элементы */
.decoration {
    position: fixed;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    z-index: -1;
}

.decoration-1 {
    background: var(--primary);
    top: 10%;
    right: 5%;
}

.decoration-2 {
    background: var(--accent);
    bottom: 10%;
    left: 5%;
}

/* Загрузка */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.loading-spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 1200px) {
    .garage-layout {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .garage-page {
        padding: 100px 5% 40px;
    }
    
    .quick-stats-section {
        flex-direction: column;
    }
}
</style>