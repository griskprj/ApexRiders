<template>
    <!-- Список мотоциклов -->
    <div class="motorcycles-section">
      <h2 class="section-title">Ваши мотоциклы</h2>
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Загрузка данных...</p>
      </div>
      <div v-else-if="motorcycles.length === 0" class="empty-state">
        <i class="fas fa-motorcycle"></i>
        <p>У вас пока нет мотоциклов</p>
        <BaseButton
          variant="primary"
          @click="openAddMotoModal"
        >
          Добавить первый мотоцикл
        </BaseButton>
      </div>
      <div v-else class="motorcycles-grid">
        <div
          v-for="bike in motorcycles"
          :key="bike.id"
          class="motorcycle-card"
        >
          <div class="card-header">
            <h3>{{ bike.brand }} {{ bike.model }}</h3>
            <span class="bike-year">{{ bike.year || '—' }}</span>
          </div>
          <div class="card-body">
            <div class="bike-detail">
              <i class="fas fa-tachometer-alt"></i>
              <span>Пробег: {{ bike.current_mileage || 0 }} км</span>
            </div>
            <div class="bike-detail">
              <i class="fas fa-motorcycle"></i>
              <span>Объём: {{ bike.engine_volume || '—' }} см³</span>
            </div>
            <div class="bike-detail">
              <i class="fas fa-palette"></i>
              <span>Цвет: {{ bike.color || '—' }}</span>
            </div>
            <div class="bike-detail">
              <i class="fas fa-file"></i>
              <span class="insuranse" :class="checkDate(bike.insurance_expiry) ? 'expiry' : ''">Страховка до: {{ formatDate(bike.insurance_expiry) || '—' }}</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="moto-action">
                <BaseButton
                  variant="outline"
                  @click="openEditMotoModal(bike)"
                >
                  <i class="fas fa-edit"></i>
                </BaseButton>
                <BaseButton
                  variant="outline"
                  @click="openDeleteMotoModal(bike.id)"
                >
                  <i class="fas fa-trash"></i>
                </BaseButton>
            </div>
            <router-link
              :to="`/garage/${bike.id}`"
              class="btn btn-small btn-primary"
              @click="goToGarage(bike.id)"
            >
              Подробнее
            </router-link>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import BaseButton from '../../ui/BaseButton.vue';

export default {
    name: 'MotorcyclesList',
    
    components: {
        BaseButton
    },

    props: {
        isLoading: Boolean,
        motorcycles: Array,
    },

    emits: ['add-motorcycle', 'edit-motorcycle', 'delete-motorcycle'],

    methods: {
        goToGarage(bikeId) {
            this.$router.push(`/garage/${bikeId}`)
        },

        openAddMotoModal() {
          this.$emit('add-motorcycle')
        },

        openEditMotoModal(bike) {
            this.$emit('edit-motorcycle', bike)
        },

        openDeleteMotoModal(bikeId) {
          this.$emit('delete-motorcycle', bikeId)
        },

        formatDate(dateString) {
            if (!dateString) return 'Не указано'
            
            const date = new Date(dateString)
            if (isNaN(date.getTime())) return 'Неверная дата'
            
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
        },
        

        checkDate(date) {
          const serverDate = new Date(date);
          const now = new Date();

          if (serverDate < now) {
              return true
          } else {
              return false
          }
        }
    },
}
</script>

<style scoped>
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
.motorcycles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
  margin-bottom: 50px;
}

.motorcycle-card {
  background: rgba(10, 10, 15, 0.7);
  backdrop-filter: blur(20px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.motorcycle-card:hover {
  transform: translateY(-8px);
  border-color: var(--primary);
  box-shadow: 0 15px 30px rgba(255, 69, 0, 0.3);
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

.bike-detail {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  color: var(--text-secondary);
}

.bike-detail i {
  width: 20px;
  color: var(--primary);
}

.moto-action {
    display: flex;
    flex-direction: row;
    gap: 15px;
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

.insuranse.expiry {
  color: var(--primary);
}


/* TODO: статусы для мото по кол-ву задач */
/* .status-none {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
}
.status-few {
  background: rgba(0, 191, 255, 0.2);
  color: var(--accent);
}
.status-many {
  background: rgba(255, 69, 0, 0.2);
  color: var(--primary);
} */

</style>