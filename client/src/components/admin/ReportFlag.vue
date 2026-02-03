<template>
    <button 
        class="report-flag"
        :title="title || 'Пожаловаться'"
        @click.stop="openReportModal"
        :class="{ 'reported': hasReported }"
    >
        <i class="fas fa-flag" :class="iconClass"></i>
        <span v-if="showText && text" class="flag-text">{{ text }}</span>
    </button>
</template>

<script>
export default {
    name: 'ReportFlag',
    
    props: {
        // Обязательные параметры
        targetId: {
            type: [Number, String],
            required: true
        },
        targetType: {
            type: String,
            required: true,
            validator: (value) => ['post', 'comment', 'product', 'manual'].includes(value)
        },
        targetOwnerId: {
            type: [Number, String],
            required: true
        },
        
        // Опциональные параметры
        title: {
            type: String,
            default: 'Пожаловаться'
        },
        text: {
            type: String,
            default: 'Пожаловаться'
        },
        showText: {
            type: Boolean,
            default: false
        },
        size: {
            type: String,
            default: 'medium',
            validator: (value) => ['small', 'medium', 'large'].includes(value)
        },
        color: {
            type: String,
            default: 'default'
        },
        showReportCount: {
            type: Boolean,
            default: false
        }
    },
    
    data() {
        return {
            hasReported: false,
            reportCount: 0,
            loading: false
        }
    },
    
    computed: {
        iconClass() {
            const classes = []
            
            if (this.hasReported) {
                classes.push('text-danger')
            } else {
                classes.push('text-secondary')
            }
            
            if (this.size === 'small') classes.push('fa-sm')
            if (this.size === 'large') classes.push('fa-lg')
            
            return classes
        }
    },
    
    methods: {
        openReportModal() {
            this.$emit('open-report', {
                targetId: this.targetId,
                targetType: this.targetType,
                targetOwnerId: this.targetOwnerId
            })
        },
        
        async checkUserReport() {
            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(`/api/reports/check?target_id=${this.targetId}&target_type=${this.targetType}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                
                if (response.ok) {
                    const data = await response.json()
                    this.hasReported = data.has_reported || false
                }
            } catch (error) {
                console.error('Error checking report:', error)
            }
        },
        
        async getReportCount() {
            if (!this.showReportCount) return
            
            try {
                const response = await fetch(`/api/reports/count?target_id=${this.targetId}&target_type=${this.targetType}`)
                
                if (response.ok) {
                    const data = await response.json()
                    this.reportCount = data.count || 0
                }
            } catch (error) {
                console.error('Error getting report count:', error)
            }
        }
    },
    
    mounted() {
        this.checkUserReport()
        this.getReportCount()
    }
}
</script>

<style scoped>
.report-flag {
    background: none;
    border: none;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.3s ease;
    color: var(--text-secondary);
    font-size: 14px;
}

.report-flag:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
}

.report-flag.reported {
    color: var(--danger);
}

.report-flag.reported:hover {
    background: rgba(220, 53, 69, 0.1);
}

.report-flag:active {
    transform: scale(0.95);
}

.flag-text {
    font-size: 0.9em;
}

.report-flag.small {
    padding: 4px 8px;
}

.report-flag.large {
    padding: 8px 16px;
    font-size: 16px;
}

.report-count {
    margin-left: 4px;
    font-size: 0.8em;
    opacity: 0.7;
}
</style>