<template>
    <div class="stats-overview" v-if="!isLoading">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-motorcycle"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ motorcycles.length }}</span>
          <span class="stat-label">Мотоциклов</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-tasks"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ upcomingTasks.length }}</span>
          <span class="stat-label">Предстоящие задачи ТО</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-history"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ overdueTasks }}</span>
          <span class="stat-label">Просроченных задач</span>
        </div>
      </div>
    </div>
</template>

<script>
export default {
    name: 'StatsOverview',

    props: {
        motorcycles: Array,
        upcomingTasks: Array,
        overdueTasks: Number,
        isLoading: Boolean
    }
}
</script>

<style scoped>
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

@media (max-width: 768px) {
    .stats-overview {
        grid-template-columns: 1fr;
    }
}
</style>
