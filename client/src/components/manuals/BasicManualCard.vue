<template>
    <div v-for="manual in limiterManuals" :key="manual.id" class="manual-card">
        <div class="manual-badge popular">
            <i class="fas fa-fire"></i> {{ manual.difficulty }}
        </div>
        <div class="manual-image">
            <img src="/DefaultListingPhoto.png" alt="Yamaha R6" style="object-fit: cover; width: 150px; height: 100px;">
        </div>
        <div class="manual-content">
            <div class="manual-category">{{ manual.moto_type }}</div>
            <h3 class="manual-title">{{ manual.title }}</h3>
            <p class="manual-desc">{{ manual.description }}</p>
            
            <div class="manual-stats">
                <div class="stat">
                    <i class="fas fa-clock"></i>
                    <span>{{ manual.estimated_time }}</span>
                </div>
                <div class="stat">
                    <i class="fas fa-eye"></i>
                    <span>{{ manual.views }}</span>
                </div>
                <div class="stat">
                    <i class="fas fa-star"></i>
                    <span>{{ manual.rating }}</span>
                </div>
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

        created() {
            console.log('BasicManualCard props:', this.limiterManuals)
            if (this.limiterManuals && this.limiterManuals.length > 0) {
                console.log('First manual object:', this.limiterManuals[0])
                console.log('First manual id:', this.limiterManuals[0].id)
            }
        },

        methods: {
            read(manual) {
                console.log('read() called with manual:', manual)
                console.log('manual.id:', manual.id)
                
                if (!manual || !manual.id) {
                    console.error('Invalid manual object:', manual)
                    alert('Не удалось открыть мануал: ID не найден')
                    return
                }
                
                console.log('Navigating to manual with ID:', manual.id)
                
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
</style>