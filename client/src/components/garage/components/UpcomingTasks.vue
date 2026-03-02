<template>
  <h2 class="section-title">Предстоящие работы</h2>
  <div class="recent-section" v-if="upcomingTasks.length > 0">
    <div class="activities-list">
      <div v-for="task in upcomingTasks" :key="task.id" class="activity-item" :class="task.is_overdue ? 'overdue' : ''">
        <div class="activity-icon">
          <i class="fas fa-wrench"></i>
        </div>
        <div class="activity-content">
          <div class="activity-title">{{ task.title }}</div>
          <div class="activity-meta">
            <span>
              <i class="fas fa-motorcycle"></i> {{ task.motorcycle.brand + ' ' + task.motorcycle.model }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="empty-state" v-else>
    <i class="fas fa-tasks"></i>
    <p>У вас нет предстоящих работ</p>
  </div>
</template>

<script>
export default {
    name: 'UpcomingTasks',

    props: {
        upcomingTasks: Array
    }
}
</script>

<style scoped>
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

.recent-section {
  margin-top: 40px;
}

.maintenance-until {
  text-align: center;
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

.activity-item.overdue {
  -webkit-box-shadow: 0px 0px 50px -5px rgba(150, 12, 12, 0.6) inset;
  -moz-box-shadow: 0px 0px 50px -5px rgba(150, 12, 12, 0.6) inset;
  box-shadow: 0px 0px 50px -5px rgba(150, 12, 12, 0.6) inset;
}

.activity-item:hover {
  border-color: var(--accent);
  transform: translateX(5px);
}

.activity-item.overdue:hover {
  border-color: rgb(150, 12, 12);
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

.activity-item.overdue .activity-icon {
  background: linear-gradient(135deg, var(--primary) 0%, #7c0707 100%);
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
</style>