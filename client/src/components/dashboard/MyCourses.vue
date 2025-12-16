<template>
    <div class="dashboard-card courses-card">
        <div class="card-header">
            <h3><i class="fas fa-graduation-cap"></i> Мои курсы</h3>
            <a href="/courses" class="card-link">Все курсы →</a>
        </div>
        <div v-if="courses.length === 0" class="no-courses">
            <i class="fas fa-graduation-cap"></i>
            <p>У вас пока нет активных курсов</p>
        </div>
        <div v-else class="courses-list">
            <div v-for="course in limitedCourses" :key="course.id" class="course-item">
                <div class="course-progress">
                    <div class="progress-circle" data-progress="{{ course.all_lessons / course.end_lessons }}">
                        <span>{{ course.all_lessons / course.end_lessons }} %</span>
                    </div>
                </div>
                <div class="course-info">
                    <div class="course-title">{{ course.title }}</div>
                    <div class="course-desc">{{ course.description }}</div>
                    <div class="course-stats">
                        <span><i class="fas fa-play-circle"></i> {{ course.end_lessons }}/{{ course.all_lessons }} уроков</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            courses: Array
        }
    }
</script>

<style scoped>
    .dashboard-card {
        background: var(--dark-light);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary-dark);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .card-header h3 {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.4rem;
        font-weight: 600;
    }

    .card-header i {
        color: var(--primary);
    }

    .card-badge {
        background: var(--primary);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .card-link {
        color: var(--primary);
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .card-link:hover {
        gap: 5px;
    }

    /* ===== КУРСЫ ===== */
    .courses-list {
        display: flex;
        flex-direction: column;
        gap: 25px;
    }

    .course-item {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
    }

    .progress-circle {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: conic-gradient(var(--primary) 65%, rgba(255, 255, 255, 0.1) 0);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .progress-circle::before {
        content: '';
        position: absolute;
        width: 55px;
        height: 55px;
        background: var(--dark-light);
        border-radius: 50%;
    }

    .progress-circle span {
        position: relative;
        z-index: 1;
        font-weight: 600;
        font-size: 1rem;
    }

    .course-info {
        flex: 1;
    }

    .course-title {
        font-weight: 600;
        margin-bottom: 5px;
    }

    .course-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 10px;
    }

    .course-stats {
        font-size: 0.85rem;
        color: var(--primary);
    }

    .course-stats i {
        margin-right: 5px;
    }

    .course-loading, .no-courses {
        text-align: center;
        padding: 40px 20px;
        color: var(--text-secondary);
    }

    .no-courses i {
        font-size: 48px;
        color: var(--text-secondary);
        margin-bottom: 15px;
        opacity: 0.5;
    }

    .no-courses p {
        margin-bottom: 20px;
    }
</style>