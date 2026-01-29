<template>
    <section class="manual-viewer">
        <div v-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Загрузка мануала...</p>
        </div>

        <!-- Состояние ошибки -->
        <div v-else-if="error" class="error-state">
            <div class="error-icon">
                <i class="fas fa-exclamation-circle"></i>
            </div>
            <h3>Ошибка загрузки</h3>
            <p>{{ error }}</p>
            <button @click="loadManual" class="btn btn-primary">
                <i class="fas fa-redo"></i> Попробовать снова
            </button>
            <button @click="$router.push('/manuals')" class="btn btn-outline">
                <i class="fas fa-arrow-left"></i> Вернуться к списку
            </button>
        </div>

        <!-- Шапка мануала -->
        <div class="manual-header">
            <div class="manual-meta">
                <div class="manual-badge" :class="(manual.difficulty || 'Начинающий').toLowerCase()">
                    {{ manual.difficulty || 'Начинающий' }}
                </div>
                <div class="manual-title-section">
                    <h1>{{ manual.title }}</h1>
                    <div class="manual-subtitle">
                        <div class="meta-info">
                            <span class="moto-info">
                                <i class="fas fa-motorcycle"></i>
                                {{ manual.moto_type }}
                            </span>
                            <span class="category">
                                <i class="fas fa-tag"></i>
                                {{ manual.category }}
                            </span>
                            <span class="time-estimate" v-if="manual.estimated_time">
                                <i class="fas fa-clock"></i>
                                {{ manual.estimated_time }}
                            </span>
                        </div>
                    </div>
                    <div v-if="manual.description" class="manual-description">
                        <div class="description-label">
                            <i class="fas fa-file-alt"></i>
                            <h3>Описание мануала</h3>
                        </div>
                        <div class="description-text">
                            <p>{{ manual.description }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="manual-progress">
                <div class="progress-header">
                    <h3><i class="fas fa-tasks"></i> Прогресс выполнения</h3>
                    <span class="progress-value">{{ completedSteps }}/{{ totalSteps }} шагов</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
                </div>
                <div class="progress-actions">
                    <button @click="resetProgress" class="btn btn-outline">
                        <i class="fas fa-redo"></i> Начать заново
                    </button>
                    <button @click="completeAll" class="btn btn-primary" v-if="completedSteps < totalSteps">
                        <i class="fas fa-check-double"></i> Отметить все как выполнено
                    </button>
                </div>
            </div>
        </div>

        <div class="manual-actions">
            <button
                class="btn btn-outline"
                @click="deleteManual(manual)"
            >
                <i class="fas fa-trash"></i> Удалить
            </button>
            <button
                class="btn btn-outline"
                @click="editManual(manual)"
            >
                <i class="fas fa-edit"></i> Редактировать
            </button>
        </div>

        <!-- Предупреждения -->
        <div v-if="manual.warnings" class="warning-card">
            <div class="warning-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="warning-content">
                <h4>Внимание! Важные предупреждения</h4>
                <p>{{ manual.warnings }}</p>
            </div>
        </div>

        <!-- Инструменты и материалы -->
        <div class="resources-section">
            <div class="resources-card">
                <div class="card-header">
                    <i class="fas fa-tools"></i>
                    <h3>Необходимые инструменты</h3>
                </div>
                <div class="card-content">
                    <ul class="resources-list">
                        <li v-for="(tool, index) in manual.tools" :key="index">
                            <i class="fas fa-check-circle"></i>
                            {{ tool }}
                        </li>
                    </ul>
                </div>
            </div>

            <div class="resources-card">
                <div class="card-header">
                    <i class="fas fa-box-open"></i>
                    <h3>Необходимые материалы</h3>
                </div>
                <div class="card-content">
                    <ul class="resources-list">
                        <li v-for="(material, index) in manual.materials" :key="index">
                            <i class="fas fa-check-circle"></i>
                            {{ material }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Шаги мануала -->
        <div class="steps-section">
            <h2 class="section-title">
                <i class="fas fa-list-ol"></i>
                Пошаговая инструкция
            </h2>

            <div v-for="(step, index) in steps" :key="step.id" class="step-card" :class="{ 'completed': step.completed }">
                <div class="step-header" @click="toggleStep(index)">
                    <div class="step-number">
                        <span>{{ index + 1 }}</span>
                    </div>
                    <div class="step-title">
                        <h3>{{ step.title }}</h3>
                        <div class="step-status">
                            <span v-if="step.completed" class="status-completed">
                                <i class="fas fa-check-circle"></i> Выполнено
                            </span>
                            <span v-else class="status-pending">
                                <i class="fas fa-circle"></i> Не выполнено
                            </span>
                        </div>
                    </div>
                    <div class="step-toggle">
                        <i class="fas fa-chevron-down" :class="{ 'rotated': step.expanded }"></i>
                    </div>
                </div>

                <div class="step-content" :class="{ 'expanded': step.expanded }">
                    <div class="step-description">
                        <p>{{ step.description }}</p>
                    </div>

                    <div v-if="step.image_url" class="step-image">
                        <img :src="step.image_url" :alt="'Шаг ' + (index + 1)">
                        <div class="image-caption">Шаг {{ index + 1 }}</div>
                    </div>

                    <div v-if="step.video_url" class="step-video">
                        <div class="video-embed">
                            <a :href="step.video_url" target="_blank" class="video-link">
                                <div class="video-thumbnail">
                                    <i class="fas fa-play-circle"></i>
                                </div>
                                <div class="video-info">
                                    <h4>Видеоинструкция</h4>
                                    <p>Нажмите для просмотра видео по этому шагу</p>
                                </div>
                            </a>
                        </div>
                    </div>

                    <div class="step-actions">
                        <button @click.stop="toggleStepComplete(index)" class="btn" :class="step.completed ? 'btn-outline' : 'btn-primary'">
                            <i class="fas" :class="step.completed ? 'fa-times' : 'fa-check'"></i>
                            {{ step.completed ? 'Отметить как невыполненное' : 'Отметить как выполненное' }}
                        </button>
                        <div class="step-navigation">
                            <button @click.stop="goToStep(index - 1)" :disabled="index === 0" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Предыдущий шаг
                            </button>
                            <button @click.stop="goToStep(index + 1)" :disabled="index === steps.length - 1" class="btn btn-primary">
                                Следующий шаг <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Панель завершения -->
        <div v-if="completedSteps === totalSteps" class="completion-card">
            <div class="completion-icon">
                <i class="fas fa-trophy"></i>
            </div>
            <div class="completion-content">
                <h2>Отличная работа! 🎉</h2>
                <p>Вы успешно завершили все шаги мануала</p>
                <div class="completion-actions">
                    <button @click="rateManual" class="btn btn-primary">
                        <i class="fas fa-star"></i> Оценить мануал
                    </button>
                    <button @click="shareManual" class="btn btn-outline">
                        <i class="fas fa-share-alt"></i> Поделиться результатом
                    </button>
                    <button @click="findSimilar" class="btn btn-secondary">
                        <i class="fas fa-search"></i> Похожие мануалы
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
    name: 'ManualViewer',
    props: {
        manualId: String,
    },
    setup(props) {
        const route = useRoute()
        const manual = ref({})
        const user_verified = ref(false)
        const steps = ref([])
        const userProgress = ref({})
        const isLoading = ref(true)
        const error = ref(null)

        const manualId = computed(() => {
            const id = route.params.id
            return id
        })
        
        const completedSteps = computed(() => {
            return steps.value.filter(step => step.completed).length
        })

        const totalSteps = computed(() => {
            return steps.value.length
        })

        const progressPercentage = computed(() => {
            if (totalSteps.value === 0) return 0
            return (completedSteps.value / totalSteps.value) * 100
        })

        const loadManual = async () => {
            try {
                const token = localStorage.getItem('authToken')
                const currentId = manualId.value

                const response = await axios.get(`/api/manuals/get/${currentId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data) {
                    manual.value = response.data.manual
                    steps.value = response.data.steps.map(step => ({
                        ...step,
                        completed: false,
                        expanded: false
                    }))
                    user_verified.value = response.data.user_verified

                    await loadUserProgress()
                }
            } catch (error) {
                console.error('Ошибка загрузки мануала:', error)
            }
        }

        const loadUserProgress = async (id) => {
            try {
                const token = localStorage.getItem('authToken')
                const id = manualId.value
                
                const response = await axios.get(`/api/manuals/constructor/${id}/progress`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data && response.data.completed_steps) {
                    userProgress.value = response.data
                    steps.value.forEach(step => {
                        if (response.data.completed_steps.includes(step.id)) {
                            step.completed = true
                        }
                    })
                }
            } catch (error) {
                console.error('Ошибка загрузки прогресса:', error)
            }
        }

        const toggleStep = (index) => {
            steps.value[index].expanded = !steps.value[index].expanded
        }

        const toggleStepComplete = async (index) => {
            const step = steps.value[index]
            const newCompletedState = !step.completed

            try {
                const token = localStorage.getItem('authToken')
                const id = manualId.value

                await axios.post(`/api/manuals/constructor/${id}/progress`, {
                    step_id: step.id,
                    completed: newCompletedState
                }, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                step.completed = newCompletedState

            } catch (error) {
                console.error('Ошибка сохранения прогресса:', error)
            }
        }

        const goToStep = (index) => {
            if (index >= 0 && index < steps.value.length) {
                steps.value.forEach((step, i) => {
                    step.expanded = i === index
                })
                if (!steps.value[index].expanded) {
                    steps.value[index].expanded = true
                }

                const stepElements = document.querySelectorAll('.step-card')
                if (stepElements[index]) {
                    stepElements[index].scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    })
                }
            }
        }

        const resetProgress = async () => {
            if (confirm('Вы уверены, что хотите сбросить прогресс?')) {
                steps.value.forEach(step => {
                    step.completed = false
                    step.expanded = false
                })

                try {
                    const token = localStorage.getItem('authToken')
                    const id = manualId.value

                    await axios.delete(`/api/manuals/constructor/${id}/progress`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                } catch (error) {
                    console.error('Ошибка сброса прогресса:', error)
                }
            }
        }

        const completeAll = () => {
            steps.value.forEach(step => {
                step.completed = true
            })

            saveAllProgress()
        }

        const saveAllProgress = async () => {
            try {
                const token = localStorage.getItem('authToken')
                const id = manualId.value

                await axios.post(`/api/manuals/${id}/complete-all`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
            } catch (error) {
                console.error('Ошибка сохранения прогресса:', error)

                steps.value.forEach(step => {
                    step.completed = false
                })
            }
        }

        const rateManual = () => {
            console.log('Оценить мануал')
        }

        const shareManual = () => {
            const shareText = `Я выполнил мануал "${manual.value.title}" на ${progressPercentage.value}%!`
            if (navigator.share) {
                navigator.share({
                    title: manual.value.title,
                    text: shareText,
                    url: window.location.href
                })
            } else {
                navigator.clipboard.writeText(window.location.href)
                alert('Ссылка скопирована в буфер обмена!')
            }
        }

        const findSimilar = () => {
            window.location.href = `/manuals?category=${encodeURIComponent(category)}`
        }

        const editManual = async (manual) => {
            try {
                const token = localStorage.getItem('authToken')
                const id = manualId.value

                const response = await axios.get(`/api/manuals/constructor/${id}/edit`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data.can_edit) {
                    window.location.href = `/constructor/edit/${id}`
                } else {
                    alert('У вас нет прав для редактирования этого мануала')
                }
            } catch (error) {
                console.error('Ошибка при проверке прав на редактирование: ', error)
                if (error.response?.status === 403) {
                    alert(error.response.data.error || 'У вас нет прав на редактирование этого мануала')
                } else {
                    alert('Произошла ошибка при проверке прав')
                }
            }
        }

        const deleteManual = async (manual) => {
            if (!confirm(`Вы уверены, что хотите удалить мануал "${manual.title}"? Это действие нельзя отменить`)) {
                return
            }

            try {
                const token = localStorage.getItem('authToken')
                const id = manualId.value
                
                const response = await axios.delete(`/api/manuals/constructor/${id}/delete`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data.success) {
                    alert('Мануал успешно удален!')
                    window.location.href = '/manuals'
                }
            } catch (error) {
                console.error('Ошибка при удалении мануала: ', error)
                if (error.response?.data?.error) {
                    alert(error.response.data.error)
                } else {
                    alert('Не удалось удалить мануал')
                }
            }
        }

        onMounted(() => {
            loadManual()
        })

        return {
            manual,
            steps,
            completedSteps,
            totalSteps,
            progressPercentage,
            toggleStep,
            toggleStepComplete,
            goToStep,
            resetProgress,
            completeAll,
            rateManual,
            shareManual,
            findSimilar,
            editManual,
            deleteManual
        }
    }
}
</script>

<style scoped>
.manual-viewer {
    padding: 120px 5% 60px;
    max-width: 1000px;
    margin: 0 auto;
}

.manual-header {
    display: grid;
    grid-template-columns: 1fr;
    gap: 30px;
    margin-bottom: 40px;
}

@media (min-width: 992px) {
    .manual-header {
        grid-template-columns: 2fr 1fr;
    }
}

.manual-meta {
    margin-bottom: 20px;
}

.manual-badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 15px;
}

.manual-badge.начинающий {
    background: rgba(40, 167, 69, 0.2);
    color: #28a745;
    border: 1px solid rgba(40, 167, 69, 0.3);
}

.manual-badge.средний {
    background: rgba(255, 193, 7, 0.2);
    color: #ffc107;
    border: 1px solid rgba(255, 193, 7, 0.3);
}

.manual-badge.продвинутый {
    background: rgba(255, 69, 0, 0.2);
    color: var(--primary);
    border: 1px solid rgba(255, 69, 0, 0.3);
}

.manual-badge.эксперт {
    background: rgba(108, 117, 125, 0.2);
    color: #6c757d;
    border: 1px solid rgba(108, 117, 125, 0.3);
}

.manual-title-section h1 {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 15px;
    line-height: 1.3;
    color: var(--text);
}

.manual-subtitle {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    gap: 20px;
    color: var(--text-secondary);
    font-size: 1rem;
    margin-bottom: 15px;    
}

.manual-subtitle span {
    display: flex;
    align-items: center;
    gap: 8px;
}

.manual-description {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: 450px;
    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;
    hyphens: auto;
}

.manual-description p {
    margin: 0;
    line-height: 1.6;
    color: var(--text);
    font-size: 1.05rem;
}

.manual-description-compact {
    background: rgba(255, 69, 0, 0.05);
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
    border: 1px solid rgba(255, 69, 0, 0.1);
}

.manual-description-compact .description-content {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.manual-description-compact i {
    color: var(--primary);
    margin-top: 3px;
    flex-shrink: 0;
}

.manual-description-compact .description-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.manual-description-compact strong {
    color: var(--text);
    font-weight: 600;
}

.manual-description-compact span {
    color: var(--text);
    line-height: 1.5;
}

.manual-progress {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.progress-header h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.1rem;
    margin: 0;
    color: var(--text);
}

.progress-value {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--primary);
}

.progress-bar {
    height: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 20px;
}

.progress-fill {
    height: 100%;
    background: var(--primary);
    border-radius: 5px;
    transition: width 0.3s ease;
}

.progress-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.warning-card {
    background: rgba(220, 53, 69, 0.1);
    border: 1px solid rgba(220, 53, 69, 0.3);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    display: flex;
    gap: 15px;
}

.warning-icon {
    color: var(--danger);
    font-size: 1.5rem;
    flex-shrink: 0;
}

.warning-content h4 {
    margin: 0 0 10px 0;
    color: var(--danger);
}

.warning-content p {
    margin: 0;
    line-height: 1.6;
    color: var(--text);
}

.resources-section {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 40px;
}

@media (min-width: 768px) {
    .resources-section {
        grid-template-columns: 1fr 1fr;
    }
}

.resources-card {
    background: var(--dark-light);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px;
    background: rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header i {
    color: var(--primary);
    font-size: 1.2rem;
}

.card-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text);
}

.card-content {
    padding: 20px;
}

.resources-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.resources-list li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    color: var(--text);
}

.resources-list li i {
    color: var(--primary);
    font-size: 0.9rem;
}

.steps-section {
    margin-bottom: 50px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.8rem;
    margin-bottom: 30px;
    color: var(--text);
}

.section-title i {
    color: var(--primary);
}

.step-card {
    background: var(--dark-light);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.step-card.completed {
    border-color: rgba(40, 167, 69, 0.3);
    background: rgba(40, 167, 69, 0.05);
}

.step-header {
    display: flex;
    align-items: center;
    padding: 20px;
    cursor: pointer;
    user-select: none;
}

.step-number {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    margin-right: 15px;
    flex-shrink: 0;
}

.step-card.completed .step-number {
    background: #28a745;
}

.step-title {
    flex: 1;
}

.step-title h3 {
    margin: 0 0 5px 0;
    font-size: 1.2rem;
    color: var(--text);
}

.step-status {
    font-size: 0.9rem;
}

.status-completed {
    color: #28a745;
    display: flex;
    align-items: center;
    gap: 5px;
}

.status-pending {
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 5px;
}

.step-toggle {
    color: var(--text-secondary);
    transition: transform 0.3s ease;
}

.step-toggle .rotated {
    transform: rotate(180deg);
}

.step-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
}

.step-content.expanded {
    max-height: 2000px;
}

.step-description {
    padding: 0 20px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.step-description p {
    margin: 0;
    line-height: 1.6;
    white-space: pre-line;
}

.step-image {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.step-image img {
    width: 100%;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.image-caption {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-top: 10px;
}

.step-video {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.video-embed {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    overflow: hidden;
}

.video-link {
    display: flex;
    align-items: center;
    padding: 15px;
    text-decoration: none;
    color: var(--text);
    transition: background 0.3s ease;
}

.video-link:hover {
    background: rgba(255, 255, 255, 0.05);
}

.video-thumbnail {
    width: 60px;
    height: 60px;
    background: var(--primary);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    flex-shrink: 0;
}

.video-thumbnail i {
    font-size: 2rem;
    color: white;
}

.video-info h4 {
    margin: 0 0 5px 0;
    font-size: 1.1rem;
}

.video-info p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.step-actions {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.step-navigation {
    display: flex;
    gap: 10px;
}

.step-navigation .btn {
    flex: 1;
}

.completion-card {
    background: linear-gradient(135deg, var(--primary) 0%, #ff8c00 100%);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    color: white;
    margin-top: 40px;
}

.completion-icon {
    font-size: 4rem;
    margin-bottom: 20px;
}

.completion-content h2 {
    margin: 0 0 10px 0;
    font-size: 2rem;
}

.completion-content p {
    margin: 0 0 30px 0;
    font-size: 1.1rem;
    opacity: 0.9;
}

.completion-actions {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

@media (min-width: 768px) {
    .completion-actions {
        flex-direction: row;
        justify-content: center;
    }
}

.completion-actions .btn {
    min-width: 200px;
}

.completion-actions .btn-primary {
    background: white;
    color: var(--primary);
}

.completion-actions .btn-primary:hover {
    background: rgba(255, 255, 255, 0.9);
}

.completion-actions .btn-outline {
    background: transparent;
    border: 2px solid white;
    color: white;
}

.completion-actions .btn-outline:hover {
    background: rgba(255, 255, 255, 0.1);
}

.completion-actions .btn-secondary {
    background: rgba(255, 255, 255, 0.2);
    color: white;
}

.completion-actions .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Кнопки */
.btn {
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: var(--primary-dark);
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--primary);
}

.btn-outline {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--primary);
}

.btn-outline:hover:not(:disabled) {
    background: rgba(255, 69, 0, 0.1);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.loading-state,
.error-state,
.not-found-state {
    padding: 100px 20px;
    text-align: center;
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.loading-spinner {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    border-top-color: var(--primary);
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

.error-icon,
.not-found-icon {
    font-size: 80px;
    color: var(--danger);
    margin-bottom: 20px;
    opacity: 0.7;
}

.not-found-icon {
    color: var(--text-secondary);
}

.error-state h3,
.not-found-state h3 {
    font-size: 1.8rem;
    margin-bottom: 10px;
    color: var(--text);
}

.error-state p,
.not-found-state p {
    color: var(--text-secondary);
    margin-bottom: 30px;
    max-width: 500px;
    line-height: 1.6;
}

.error-state .btn,
.not-found-state .btn {
    margin: 5px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 768px) {
    .manual-viewer {
        padding: 100px 5% 40px;
    }
    
    .manual-title-section h1 {
        font-size: 1.8rem;
    }
    
    .manual-subtitle {
        flex-direction: column;
        gap: 10px;
    }
    
    .step-actions {
        flex-direction: column;
    }
    
    .step-navigation {
        flex-direction: column;
    }
    
    .completion-card {
        padding: 30px 20px;
    }
    
    .completion-content h2 {
        font-size: 1.5rem;
    }
}
</style>