<template>
    <div class="manual-preview">
        <div class="preview-header">
            <div class="preview-badge">{{ manual.difficulty }}</div>
            <h1 class="preview-title">{{ manual.title }}</h1>
            <div class="preview-meta">
                <span class="moto-type">{{ manual.moto_type }}</span>
                <span class="category">{{ manual.category }}</span>
                <span class="time">{{ manual.estimated_time }}</span>
            </div>
        </div>

        <div class="preview-description">
            <p>{{ manual.description }}</p>
        </div>

        <div v-if="manual.warnings" class="preview-warning">
            <div class="warning-header">
                <i class="fas fa-exclamation-triangle"></i>
                <h4>Важные предупреждения</h4>
            </div>
            <p>{{ manual.warnings }}</p>
        </div>

        <div class="preview-resources">
            <div class="resources-card">
                <h3><i class="fas fa-tools"></i> Инструменты</h3>
                <div class="tags-list">
                    <span v-for="(tool, index) in manual.tools" :key="index" class="tag">{{ tool }}</span>
                </div>
            </div>
            <div class="resources-card">
                <h3><i class="fas fa-box-open"></i> Материалы</h3>
                <div class="tags-list">
                    <span v-for="(material, index) in manual.materials" :key="index" class="tag">{{ material }}</span>
                </div>
            </div>
        </div>

        <div class="preview-steps">
            <h2>Пошаговая инструкция</h2>
            <div v-for="(step, index) in steps" :key="step.id" class="preview-step">
                <div class="step-number">
                    <span>{{ index + 1 }}</span>
                </div>
                <div class="step-content">
                    <h3>{{ step.title }}</h3>
                    <div class="step-description">
                        {{ step.description }}
                    </div>
                    <div v-if="step.image_url" class="step-media">
                        <img :src="step.image_url" alt="Шаг {{ index + 1 }}">
                    </div>
                    <div v-if="step.video_url" class="step-video">
                        <a :href="step.video_url" target="_blank" class="video-link">
                            <i class="fas fa-play-circle"></i> Видеоинструкция
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ManualPreview',
    props: {
        manual: Object,
        steps: Array
    }
}
</script>

<style scoped>
.manual-preview {
    color: var(--text);
}

.preview-header {
    margin-bottom: 30px;
}

.preview-badge {
    display: inline-block;
    padding: 6px 12px;
    background: var(--primary);
    color: white;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 15px;
}

.preview-title {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 15px;
    line-height: 1.3;
}

.preview-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.preview-meta span {
    display: flex;
    align-items: center;
    gap: 5px;
}

.preview-description {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 25px;
    line-height: 1.6;
}

.preview-warning {
    background: rgba(220, 53, 69, 0.1);
    border: 1px solid rgba(220, 53, 69, 0.3);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 25px;
}

.warning-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    color: var(--danger);
}

.warning-header i {
    font-size: 1.2rem;
}

.warning-header h4 {
    margin: 0;
    font-weight: 600;
}

.preview-resources {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
}

.resources-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
}

.resources-card h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    font-size: 1.1rem;
}

.resources-card h3 i {
    color: var(--primary);
}

.tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tag {
    background: rgba(255, 255, 255, 0.1);
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 0.9rem;
}

.preview-steps h2 {
    font-size: 1.5rem;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.preview-step {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.preview-step:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.step-number {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    font-weight: 600;
    color: white;
}

.step-content {
    flex: 1;
}

.step-content h3 {
    font-size: 1.2rem;
    margin-bottom: 10px;
    color: var(--text);
}

.step-description {
    line-height: 1.6;
    margin-bottom: 15px;
    white-space: pre-line;
}

.step-media {
    margin: 15px 0;
}

.step-media img {
    max-width: 100%;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.step-video {
    margin-top: 10px;
}

.video-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
}

.video-link:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .preview-resources {
        grid-template-columns: 1fr;
    }
    
    .preview-step {
        flex-direction: column;
    }
    
    .step-number {
        align-self: flex-start;
    }
}
</style>