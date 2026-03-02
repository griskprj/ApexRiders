<template>
  <div class="decoration decoration-1"></div>
  <div class="decoration decoration-2"></div>

  <section class="dashboard">
    <div class="dashboard-header">
      <h1 class="dashboard-title">Мой гараж</h1>
      <div class="header-actions">
        <BaseButton
          @click="openAddMotoModal"
        >
          <i class="fas fa-plus-circle"></i> Добавить мотоцикл
        </BaseButton>

        <BaseButton
          :disabled="!hasMotorcycles"
          @click="openAddTaskModal"
        >
          <i class="fas fa-tools"></i> Добавить задачу ТО
        </BaseButton>
      </div>
    </div>

    <!-- Сводная статистика -->
    <StatsOverview
      :motorcycles="this.motorcycles"
      :upcomingTasks="this.upcomingTasks"
      :overdueTasks="this.overdueTasks"
      :isLoading="this.isLoading"
    />

    <!-- Список мотоциклов -->
    <MotorcyclesList
      :isLoading="this.isLoading"
      :motorcycles="this.motorcycles"
      @add-motorcycle="openAddMotoModal"
      @edit-motorcycle="handleEditMotorcycle"
      @delete-motorcycle="handleDeleteMotorcycle"
    />

    <!-- Предстоящие работы -->
    <UpcomingTasks
      :upcomingTasks="this.upcomingTasks"
    />

    <!-- Модальное окно добавления мотоцикла -->
    <AddMotoModal
      :is-open="showMotoModal"
      :motorcycle-to-edit="editingMotorcycle"
      @close="closeMotoModal"
      @save="onMotoSaved"
    />

    <DeleteMotoModal
      :isOpen="showDeleteMotoModal"
      :motoToDeleteId="deletingMotorcycle"
      @close="closeDeleteMotoModal"
      @delete="onMotoDeleted"
    />

    <!-- Модальное окно добавления задачи -->
    <AddTaskModal
      :isOpen="showTaskModal"
      :motorcycles="motorcycles"
      @close="closeTaskModal"
      @create="onTaskCreate"
    />
  </section>
</template>

<script>
import axios from 'axios'
import { authService } from '../../utils/checkAuth'
import BaseButton from '../../ui/BaseButton.vue';
import StatsOverview from './components/StatsOverview.vue'
import MotorcyclesList from './components./MotorcyclesList.vue';
import UpcomingTasks from './components./UpcomingTasks.vue';
import AddMotoModal from './components./AddMotoModal.vue';
import DeleteMotoModal from './components./DeleteMotoModal.vue';
import AddTaskModal from './components./AddTaskModal.vue';

export default {
    name: 'Garage',

    components: {
      BaseButton,
      StatsOverview,
      MotorcyclesList,
      UpcomingTasks,
      AddMotoModal,
      DeleteMotoModal,
      AddTaskModal
    },
    
    data() {
        return {
            motorcycles: [],
            upcomingTasks: [],
            overdueTasks: null,
            isLoading: true,
            showTaskModal: false,
            showMotoModal: false,
            showDeleteMotoModal: false,
            editingMotorcycle: null,
            deletingMotorcycle: null,
            newTask: {
                motorcycle_id: null,
                title: '',
                description: '',
                schedule_type: 'mileage',
                interval_value: null,
                interval_unit: 'months',
                last_maintenance_date: new Date().toISOString().split('T')[0],
                last_maintenance_mileage: null,
                priority: 'medium',
                is_recurring: true,
                notes: ''
            }
        }
    },

    computed: {
        hasMotorcycles() {
            return this.motorcycles.length > 0
        },
    },

    methods: {
      async fetchGarageData() {
        try {
          this.isLoading = true
          const token = authService.getToken()

          const response = await axios.get('/api/garage/overview', {
            headers: { 'Authorization': `Bearer ${token}`}
          })

          this.motorcycles = response.data.motorcycles || []
          this.upcomingTasks = response.data.upcoming_tasks || []
          this.overdueTasks = response.data.overdue_tasks || 0

        } catch (error) {
          console.error('Ошибка загрузки данных с сервера: ', error)
        } finally {
          this.isLoading = false
        }
      },
      
      handleEditMotorcycle(bike) {
        this.editingMotorcycle = { ...bike }
        this.showMotoModal = true
      },

      openAddMotoModal() {
        this.editingMotorcycle = null
        this.showMotoModal = true
      },

      closeMotoModal() {
        this.showMotoModal = false
        this.editingMotorcycle = null
      },

      async onMotoSaved() {
        await this.fetchGarageData()
        this.closeMotoModal()
      },


      handleDeleteMotorcycle(bikeId) {
        this.deletingMotorcycle = bikeId
        this.showDeleteMotoModal = true
      },

      closeDeleteMotoModal() {
        this.deletingMotorcycle = null
        this.showDeleteMotoModal = false
      },

      async onMotoDeleted() {
        await this.fetchGarageData()
        this.closeDeleteMotoModal()
      },


      openAddTaskModal() {
        this.showTaskModal = true
      },

      closeTaskModal() {
        this.showTaskModal = false
      },

      async onTaskCreate() {
        await this.fetchGarageData()
        this.closeTaskModal()
      },

      getTaskStatusClass(bike) {
        const count = bike.active_tasks_count || 0
        if (count === 0) return 'status-none'
        if (count <= 2) return 'status-few'
        return 'status-many'
      },

      getTaskCountForBike(bike) {
        return bike.active_tasks_count || 0
      },

      formatDate(dateString) {
        if (!dateString) return ''

        const date = new Date(dateString)
        return date.toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric'
        })
      }
    },
    
    mounted() {
      this.fetchGarageData()
    }
}
</script>

<style scoped>
.dashboard {
  padding: 120px 5% 60px;
  position: relative;
  min-height: calc(100vh - 80px);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 40px;
}

.dashboard-title {
  font-size: 2.5rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 15px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 25px;
  margin-bottom: 50px;
}

.stat-card {
  background: rgba(10, 10, 15, 0.7);
  backdrop-filter: blur(20px);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: var(--primary);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(255, 69, 0, 0.2);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text);
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 5px;
}

.section-title {
  font-size: 1.8rem;
  margin-bottom: 25px;
  color: var(--text);
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  border-radius: 3px;
}

.card-header {
  padding: 20px;
  background: rgba(20, 20, 30, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.3rem;
  color: var(--text);
}

.bike-year {
  color: var(--text-secondary);
  font-size: 0.9rem;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

.card-body {
  padding: 20px;
}


.card-footer {
  padding: 15px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);
}

.task-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}


.recent-section {
  margin-top: 40px;
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  background: rgba(10, 10, 15, 0.7);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  border-color: var(--accent);
  transform: translateX(5px);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent) 0%, #00bfff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: var(--text);
  margin-bottom: 5px;
}

.activity-meta {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.activity-meta i {
  margin-right: 5px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
  background: rgba(10, 10, 15, 0.5);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 1.2rem;
}

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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: rgba(10, 10, 15, 0.95);
  border-radius: 15px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-body {
  padding: 25px;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 500;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: var(--text);
  font-size: 1em;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.2);
}

@media (max-width: 768px) {
  .dashboard {
    padding: 100px 4% 40px;
  }
  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
  }
  .header-actions {
    flex-direction: column;
  }
  .stats-overview {
    grid-template-columns: 1fr;
  }
  .motorcycles-grid {
    grid-template-columns: 1fr;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .activity-meta {
    flex-direction: column;
    gap: 5px;
  }
}
</style>