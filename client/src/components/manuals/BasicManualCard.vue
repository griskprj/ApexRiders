<template>
    <div v-for="manual in limiterManuals" :key="manual.id" class="manual-card">
        <div class="manual-badge" :class="manual.difficulty">
            <i class="fas fa-fire"></i> {{ manual.difficulty }}
        </div>
        <div class="manual-image">
            <img src="/DefaultManualPhoto.png" alt="Yamaha R6">
        </div>
        <div class="manual-content">
            <div class="manual-category">{{ manual.category || manual.moto_type }}</div>
            <h3 class="manual-title">{{ manual.title }}</h3>
            <p class="manual-desc">{{ manual.description }}</p>
            
            <div class="manual-stats">
                <span>
                    <i class="fas fa-clock"></i> {{ manual.estimated_time }}
                </span>
                <span>
                    <i class="fas fa-eye"></i> {{ manual.views }}
                </span>
                <span>
                    <i class="fas fa-star"></i> {{ manual.rating }}
                </span>
            </div>
            
            <button @click="read(manual)" class="btn btn-primary btn-block">
                <i class="fas fa-book-open"></i> Открыть мануал
            </button>
        </div>
    </div>
</template> 

<script>
    export default {
        props: {
            limiterManuals: Array
        },

        methods: {
            read(manual) {
                if (!manual || !manual.id) {
                    console.error('Invalid manual object:', manual)
                    alert('Не удалось открыть мануал: ID не найден')
                    return
                }
                
                this.$router.push({ 
                    name: 'ManualViewer', 
                    params: { id: manual.id.toString() } 
                }).catch(err => {
                    console.error('Navigation error:', err)
                })
            }
        }
    }
</script>

<style scoped>
    .manuals-header {
        margin-bottom: 40px;
    }

    .manuals-title {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 2.8rem;
        font-weight: 300;
        margin-bottom: 15px;
        color: var(--text);
    }

    .manuals-title i {
        color: var(--primary);
        text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
    }

    .manuals-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 30px;
        max-width: 600px;
    }

    /* ===== КОНТЕНТ С ГРИДОМ ===== */
    .manuals-content {
        display: flex;
        flex-direction: column;
    }

    .manuals-content.no-content {
        min-height: 50vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .manuals-main {
        flex: 1;
    }

    /* ===== КАРТА МАНУАЛА ===== */
    .manual-card {
        background: var(--dark-light);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .manual-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary-dark);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
    }

    .manual-image {
        position: relative;
        height: 200px;
        overflow: hidden;
    }
    
    .manual-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .manual-card:hover .manual-image img {
        transform: scale(1.05);
    }

    .manual-content {
        padding: 25px;
    }

    .manual-badge {
        position: absolute;
        top: 15px;
        left: 15px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        z-index: 2;

        background: rgba(0, 255, 0, 0.2);
        color: limegreen;
        border: 1px solid rgba(0, 255, 0, 0.3);
    }

    .manual-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 12px;
        color: var(--text);
        line-height: 1.4;
    }

    .manual-category {
        color: var(--accent);
        font-size: 0.85rem;
        margin-bottom: 10px;
        font-weight: 500;
    }

    .manual-desc {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 20px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .manual-stats {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .manual-stats {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    .manual-stats i {
        font-size: 14px;
        color: var(--primary)
    }

    .stat {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
        color: var(--text-secondary);
    }

    .stat i {
        color: var(--primary);
    }
</style>